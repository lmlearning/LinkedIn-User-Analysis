#!/usr/bin/env python3
"""
LinkedIn Engagement Cross-Reference Tool

This script helps you track which of your connections have engaged with your posts.
It can combine multiple scraped engagement CSV files and generate a master engagement list.

Usage:
    python engagement_tracker.py --posts post1_engagers.csv post2_engagers.csv post3_engagers.csv --output master_engagement.csv
"""

import argparse
import csv
from collections import defaultdict
from typing import Dict, List, Set
import os


class EngagementTracker:
    """Track and analyze engagement across multiple LinkedIn posts."""

    def __init__(self):
        self.engagers: Dict[str, Dict] = {}  # name -> {count, posts_engaged}
        self.total_posts = 0
        self.total_engagements = 0

    def load_post_engagers(self, filepath: str, post_name: str = None) -> int:
        """
        Load engagers from a single post CSV.
        Expected columns: Name or (First Name + Last Name)
        Returns count of engagers loaded.
        """
        if post_name is None:
            post_name = os.path.basename(filepath).replace('.csv', '')

        engagers_count = 0

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    # Extract name
                    name = row.get('Name', row.get('Full Name', ''))

                    if not name:
                        first = row.get('First Name', '')
                        last = row.get('Last Name', '')
                        name = f"{first} {last}".strip()

                    if name:
                        if name not in self.engagers:
                            self.engagers[name] = {
                                'count': 0,
                                'posts': set(),
                                'first_name': row.get('First Name', name.split()[0] if ' ' in name else name),
                                'last_name': row.get('Last Name', name.split()[-1] if ' ' in name else ''),
                                'company': row.get('Company', ''),
                                'position': row.get('Position', '')
                            }

                        self.engagers[name]['count'] += 1
                        self.engagers[name]['posts'].add(post_name)
                        engagers_count += 1
                        self.total_engagements += 1

            self.total_posts += 1
            print(f"✓ Loaded {engagers_count} engagements from {post_name}")
            return engagers_count

        except FileNotFoundError:
            print(f"✗ Error: File '{filepath}' not found")
            return 0
        except Exception as e:
            print(f"✗ Error loading {filepath}: {e}")
            return 0

    def get_engagement_stats(self) -> Dict:
        """Calculate engagement statistics."""
        unique_engagers = len(self.engagers)

        engagement_distribution = defaultdict(int)
        for name, data in self.engagers.items():
            engagement_distribution[data['count']] += 1

        # Find top engagers
        sorted_engagers = sorted(
            self.engagers.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )

        return {
            'total_posts': self.total_posts,
            'total_engagements': self.total_engagements,
            'unique_engagers': unique_engagers,
            'avg_engagements_per_post': self.total_engagements / self.total_posts if self.total_posts > 0 else 0,
            'avg_engagements_per_person': self.total_engagements / unique_engagers if unique_engagers > 0 else 0,
            'top_engagers': sorted_engagers[:10],
            'engagement_distribution': dict(engagement_distribution)
        }

    def export_master_list(self, output_filepath: str) -> None:
        """Export master engagement list to CSV."""
        fieldnames = [
            'Name',
            'First Name',
            'Last Name',
            'Company',
            'Position',
            'Total Engagements',
            'Posts Engaged',
            'Engagement Rate %'
        ]

        # Sort by engagement count (highest first)
        sorted_engagers = sorted(
            self.engagers.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )

        try:
            with open(output_filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for name, data in sorted_engagers:
                    engagement_rate = (len(data['posts']) / self.total_posts * 100) if self.total_posts > 0 else 0

                    writer.writerow({
                        'Name': name,
                        'First Name': data['first_name'],
                        'Last Name': data['last_name'],
                        'Company': data['company'],
                        'Position': data['position'],
                        'Total Engagements': data['count'],
                        'Posts Engaged': len(data['posts']),
                        'Engagement Rate %': f"{engagement_rate:.1f}"
                    })

            print(f"✓ Master engagement list exported to {output_filepath}")

        except Exception as e:
            print(f"✗ Error exporting master list: {e}")

    def print_stats(self, stats: Dict) -> None:
        """Print engagement statistics to console."""
        print("\n" + "="*60)
        print("ENGAGEMENT ANALYSIS SUMMARY")
        print("="*60)
        print(f"\nTotal Posts Analyzed: {stats['total_posts']}")
        print(f"Total Engagements: {stats['total_engagements']}")
        print(f"Unique Engagers: {stats['unique_engagers']}")
        print(f"Avg Engagements per Post: {stats['avg_engagements_per_post']:.1f}")
        print(f"Avg Engagements per Person: {stats['avg_engagements_per_person']:.1f}")

        print("\n" + "-"*60)
        print("TOP 10 ENGAGERS")
        print("-"*60)
        print(f"{'Name':<30} {'Engagements':<15} {'Posts'}")
        print("-"*60)

        for name, data in stats['top_engagers']:
            posts_count = len(data['posts'])
            print(f"{name:<30} {data['count']:<15} {posts_count}")

        print("\n" + "-"*60)
        print("ENGAGEMENT DISTRIBUTION")
        print("-"*60)
        print(f"{'Engagement Count':<20} {'# of People'}")
        print("-"*60)

        for count in sorted(stats['engagement_distribution'].keys(), reverse=True):
            people = stats['engagement_distribution'][count]
            print(f"{count:<20} {people}")

        print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Track and analyze LinkedIn post engagement'
    )
    parser.add_argument(
        '--posts',
        nargs='+',
        required=True,
        help='Paths to post engagers CSV files'
    )
    parser.add_argument(
        '--output',
        default='master_engagement.csv',
        help='Output filepath for master engagement list (default: master_engagement.csv)'
    )

    args = parser.parse_args()

    # Initialize tracker
    tracker = EngagementTracker()

    # Load all post files
    print(f"\n📊 Loading engagement data from {len(args.posts)} posts...\n")
    for filepath in args.posts:
        tracker.load_post_engagers(filepath)

    # Calculate and print stats
    stats = tracker.get_engagement_stats()
    tracker.print_stats(stats)

    # Export master list
    tracker.export_master_list(args.output)

    print(f"\n✅ Analysis complete! Use this file with connection_analyzer.py:")
    print(f"   python connection_analyzer.py --connections Connections.csv --engagement {args.output}\n")


if __name__ == '__main__':
    main()
