#!/usr/bin/env python3
"""
LinkedIn Connection Removal Candidate Analyzer

This script analyzes LinkedIn connections data and generates a scored list
of removal candidates based on multiple factors including activity, engagement,
and strategic value.

Usage:
    python connection_analyzer.py --connections connections.csv [--engagement engagers.csv]
"""

import argparse
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import sys
from collections import defaultdict


class Connection:
    """Represents a LinkedIn connection with scoring attributes."""

    def __init__(self, first_name: str, last_name: str, email: str,
                 company: str, position: str, connected_on: str):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = f"{first_name} {last_name}"
        self.email = email
        self.company = company
        self.position = position
        self.connected_on = connected_on

        # Scoring components
        self.activity_score = 0
        self.engagement_score = 0
        self.relevance_score = 0
        self.strategic_score = 0
        self.total_score = 0

        # Metadata
        self.engagement_count = 0
        self.days_connected = self._calculate_days_connected()
        self.removal_tier = ""
        self.notes = []

    def _calculate_days_connected(self) -> int:
        """Calculate days since connection was made."""
        try:
            # LinkedIn format: "DD MMM YYYY" or "DD Mon YYYY"
            connected_date = datetime.strptime(self.connected_on, "%d %b %Y")
            return (datetime.now() - connected_date).days
        except ValueError:
            try:
                # Try alternative format
                connected_date = datetime.strptime(self.connected_on, "%m/%d/%Y")
                return (datetime.now() - connected_date).days
            except ValueError:
                # If parsing fails, assume old connection
                return 1000

    def calculate_activity_score(self, last_activity_days: Optional[int] = None) -> int:
        """
        Calculate activity score (0-40 points) based on last activity date.
        If last_activity_days not available, use days_connected as proxy.
        """
        # If we don't have actual activity data, penalize old connections
        if last_activity_days is None:
            last_activity_days = self.days_connected

        if last_activity_days <= 90:  # 0-3 months
            self.activity_score = 40
        elif last_activity_days <= 180:  # 3-6 months
            self.activity_score = 30
        elif last_activity_days <= 365:  # 6-12 months
            self.activity_score = 15
        elif last_activity_days <= 730:  # 12-24 months
            self.activity_score = 5
        else:  # 24+ months
            self.activity_score = 0

        return self.activity_score

    def calculate_engagement_score(self, engagement_count: int) -> int:
        """
        Calculate engagement score (0-30 points) based on interaction count.
        """
        self.engagement_count = engagement_count

        if engagement_count >= 5:  # Regular engagement
            self.engagement_score = 30
        elif engagement_count >= 2:  # Occasional engagement
            self.engagement_score = 15
        elif engagement_count == 1:  # Minimal engagement
            self.engagement_score = 5
        else:  # Never engages
            self.engagement_score = 0

        return self.engagement_score

    def calculate_relevance_score(self, target_industries: List[str] = None,
                                  target_companies: List[str] = None) -> int:
        """
        Calculate relevance score (0-15 points) based on industry/company alignment.
        This is a simplified version - in practice, you'd customize this.
        """
        score = 0

        # Check if company/position has content (profile completeness proxy)
        if self.company and self.position:
            score += 5  # Has complete info

            # Check industry alignment
            if target_industries:
                for industry in target_industries:
                    if industry.lower() in self.position.lower() or \
                       industry.lower() in self.company.lower():
                        score += 10
                        break
            else:
                # Default scoring if no targets specified
                score += 5

            # Check company alignment
            if target_companies:
                for company in target_companies:
                    if company.lower() in self.company.lower():
                        score += 5  # Bonus for target company
                        break
        else:
            score = 0  # Incomplete profile

        self.relevance_score = min(score, 15)  # Cap at 15
        return self.relevance_score

    def calculate_strategic_score(self, strategic_keywords: List[str] = None) -> int:
        """
        Calculate strategic value score (0-15 points).
        Based on position keywords like 'recruiter', 'founder', 'CEO', etc.
        """
        if strategic_keywords is None:
            strategic_keywords = [
                'recruiter', 'hiring', 'talent', 'ceo', 'founder',
                'cto', 'vp', 'director', 'head of', 'chief', 'partner'
            ]

        score = 5  # Base score for any connection

        position_lower = self.position.lower() if self.position else ""

        for keyword in strategic_keywords:
            if keyword.lower() in position_lower:
                score = 15  # High strategic value
                break

        self.strategic_score = score
        return self.strategic_score

    def calculate_total_score(self) -> int:
        """Sum all component scores."""
        self.total_score = (self.activity_score + self.engagement_score +
                           self.relevance_score + self.strategic_score)

        # Assign removal tier
        if self.total_score <= 30:
            self.removal_tier = "Tier 1 - High Confidence"
            self.notes.append("Strong removal candidate")
        elif self.total_score <= 50:
            self.removal_tier = "Tier 2 - Medium Confidence"
            self.notes.append("Consider removal")
        elif self.total_score <= 70:
            self.removal_tier = "Tier 3 - Low Confidence"
            self.notes.append("Review manually")
        else:
            self.removal_tier = "Keep"
            self.notes.append("Valuable connection")

        # Add specific notes
        if self.engagement_count == 0 and self.days_connected > 365:
            self.notes.append("Zero engagement over 1+ years")
        if self.activity_score == 0:
            self.notes.append("Likely inactive >24 months")
        if not self.company or not self.position:
            self.notes.append("Incomplete profile")

        return self.total_score

    def to_dict(self) -> Dict:
        """Convert connection to dictionary for CSV export."""
        return {
            'Full Name': self.full_name,
            'First Name': self.first_name,
            'Last Name': self.last_name,
            'Email': self.email,
            'Company': self.company,
            'Position': self.position,
            'Connected On': self.connected_on,
            'Days Connected': self.days_connected,
            'Engagement Count': self.engagement_count,
            'Activity Score': self.activity_score,
            'Engagement Score': self.engagement_score,
            'Relevance Score': self.relevance_score,
            'Strategic Score': self.strategic_score,
            'Total Score': self.total_score,
            'Removal Tier': self.removal_tier,
            'Notes': '; '.join(self.notes)
        }


class ConnectionAnalyzer:
    """Main analyzer for LinkedIn connections."""

    def __init__(self):
        self.connections: List[Connection] = []
        self.engagement_data: Dict[str, int] = defaultdict(int)

    def load_connections(self, filepath: str) -> int:
        """
        Load connections from LinkedIn CSV export.
        Expected columns: First Name, Last Name, Email Address, Company, Position, Connected On
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    # Handle various column name formats
                    first_name = row.get('First Name', '')
                    last_name = row.get('Last Name', '')
                    email = row.get('Email Address', row.get('Email', ''))
                    company = row.get('Company', '')
                    position = row.get('Position', '')
                    connected_on = row.get('Connected On', '')

                    connection = Connection(
                        first_name, last_name, email,
                        company, position, connected_on
                    )
                    self.connections.append(connection)

            print(f"✓ Loaded {len(self.connections)} connections from {filepath}")
            return len(self.connections)

        except FileNotFoundError:
            print(f"✗ Error: File '{filepath}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"✗ Error loading connections: {e}")
            sys.exit(1)

    def load_engagement_data(self, filepath: str) -> int:
        """
        Load engagement data from scraped post engagers CSV.
        Expected columns: Name (or First Name + Last Name)
        Each row represents one engagement (like/comment).
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    # Try different name formats
                    name = row.get('Name', row.get('Full Name', ''))

                    if not name:
                        # Try combining first + last
                        first = row.get('First Name', '')
                        last = row.get('Last Name', '')
                        name = f"{first} {last}".strip()

                    if name:
                        self.engagement_data[name] += 1

            unique_engagers = len(self.engagement_data)
            total_engagements = sum(self.engagement_data.values())

            print(f"✓ Loaded {total_engagements} engagements from {unique_engagers} unique people")
            return unique_engagers

        except FileNotFoundError:
            print(f"⚠ Warning: Engagement file '{filepath}' not found")
            print("  Continuing with zero engagement scores for all connections")
            return 0
        except Exception as e:
            print(f"⚠ Warning: Error loading engagement data: {e}")
            print("  Continuing with zero engagement scores")
            return 0

    def analyze_connections(self,
                          target_industries: List[str] = None,
                          target_companies: List[str] = None,
                          strategic_keywords: List[str] = None) -> None:
        """
        Analyze all connections and calculate scores.
        """
        print(f"\n🔍 Analyzing {len(self.connections)} connections...")

        for connection in self.connections:
            # Get engagement count for this connection
            engagement_count = self.engagement_data.get(connection.full_name, 0)

            # Calculate all scores
            connection.calculate_activity_score()  # Using days_connected as proxy
            connection.calculate_engagement_score(engagement_count)
            connection.calculate_relevance_score(target_industries, target_companies)
            connection.calculate_strategic_score(strategic_keywords)
            connection.calculate_total_score()

        print("✓ Analysis complete!")

    def generate_report(self) -> Dict[str, any]:
        """Generate summary statistics."""
        total = len(self.connections)
        tier1 = sum(1 for c in self.connections if c.removal_tier == "Tier 1 - High Confidence")
        tier2 = sum(1 for c in self.connections if c.removal_tier == "Tier 2 - Medium Confidence")
        tier3 = sum(1 for c in self.connections if c.removal_tier == "Tier 3 - Low Confidence")
        keep = sum(1 for c in self.connections if c.removal_tier == "Keep")

        zero_engagement = sum(1 for c in self.connections if c.engagement_count == 0)

        avg_score = sum(c.total_score for c in self.connections) / total if total > 0 else 0

        return {
            'total_connections': total,
            'tier1_count': tier1,
            'tier2_count': tier2,
            'tier3_count': tier3,
            'keep_count': keep,
            'zero_engagement_count': zero_engagement,
            'average_score': avg_score,
            'tier1_percentage': (tier1 / total * 100) if total > 0 else 0,
            'tier2_percentage': (tier2 / total * 100) if total > 0 else 0,
            'zero_engagement_percentage': (zero_engagement / total * 100) if total > 0 else 0
        }

    def export_results(self, output_filepath: str) -> None:
        """Export analyzed connections to CSV."""
        # Sort by total score (lowest first - highest removal priority)
        sorted_connections = sorted(self.connections, key=lambda c: c.total_score)

        fieldnames = [
            'Full Name', 'First Name', 'Last Name', 'Email', 'Company', 'Position',
            'Connected On', 'Days Connected', 'Engagement Count',
            'Activity Score', 'Engagement Score', 'Relevance Score', 'Strategic Score',
            'Total Score', 'Removal Tier', 'Notes'
        ]

        try:
            with open(output_filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for connection in sorted_connections:
                    writer.writerow(connection.to_dict())

            print(f"✓ Results exported to {output_filepath}")

        except Exception as e:
            print(f"✗ Error exporting results: {e}")
            sys.exit(1)

    def print_summary(self, report: Dict) -> None:
        """Print summary statistics to console."""
        print("\n" + "="*60)
        print("CONNECTION ANALYSIS SUMMARY")
        print("="*60)
        print(f"\nTotal Connections: {report['total_connections']}")
        print(f"Average Score: {report['average_score']:.1f}/100")
        print(f"\n{'Removal Tier':<30} {'Count':<10} {'Percentage'}")
        print("-"*60)
        print(f"{'Tier 1 - High Confidence':<30} {report['tier1_count']:<10} {report['tier1_percentage']:.1f}%")
        print(f"{'Tier 2 - Medium Confidence':<30} {report['tier2_count']:<10} {report['tier2_percentage']:.1f}%")
        print(f"{'Tier 3 - Low Confidence':<30} {report['tier3_count']:<10}")
        print(f"{'Keep':<30} {report['keep_count']:<10}")
        print("-"*60)
        print(f"\nZero Engagement: {report['zero_engagement_count']} ({report['zero_engagement_percentage']:.1f}%)")
        print("\n" + "="*60)
        print("\n💡 Recommendations:")
        print(f"  • Start removing Tier 1 connections ({report['tier1_count']} candidates)")
        print(f"  • Safe removal rate: 10-30 per day")
        print(f"  • Estimated cleanup time: {max(1, report['tier1_count'] // 20)} - {max(1, report['tier1_count'] // 10)} days")
        print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze LinkedIn connections and generate removal candidates'
    )
    parser.add_argument(
        '--connections',
        required=True,
        help='Path to LinkedIn connections CSV file'
    )
    parser.add_argument(
        '--engagement',
        help='Path to engagement data CSV (optional, from scraped post data)'
    )
    parser.add_argument(
        '--output',
        default='removal_candidates.csv',
        help='Output filepath for results (default: removal_candidates.csv)'
    )
    parser.add_argument(
        '--industries',
        nargs='+',
        help='Target industries to keep (e.g., "Software" "Technology")'
    )
    parser.add_argument(
        '--companies',
        nargs='+',
        help='Target companies to prioritize (e.g., "Google" "Microsoft")'
    )

    args = parser.parse_args()

    # Initialize analyzer
    analyzer = ConnectionAnalyzer()

    # Load data
    analyzer.load_connections(args.connections)

    if args.engagement:
        analyzer.load_engagement_data(args.engagement)

    # Analyze
    analyzer.analyze_connections(
        target_industries=args.industries,
        target_companies=args.companies
    )

    # Generate report
    report = analyzer.generate_report()
    analyzer.print_summary(report)

    # Export results
    analyzer.export_results(args.output)

    print(f"\n✅ Analysis complete! Check {args.output} for detailed results.\n")


if __name__ == '__main__':
    main()
