# LinkedIn Connection Removal Candidate Generator

A data-driven toolkit for analyzing LinkedIn connections and generating scored lists of removal candidates to improve engagement rates.

## 📋 Overview

This project provides Python tools to systematically identify LinkedIn connections that may be reducing your engagement rate. By analyzing connection age, engagement history, and strategic value, you can make informed decisions about network optimization.

**Key Benefits:**
- Increase your post engagement rate (target: >4%)
- Improve LinkedIn algorithm visibility
- Focus on high-quality professional relationships
- Data-driven decision making

## 🎯 The Problem

LinkedIn's 2025 algorithm heavily favors **quality over quantity**:
- Average engagement rate: 3.85%
- Algorithm prioritizes active, engaged connections
- Large networks with inactive connections hurt content visibility
- One-sided relationships drag down engagement metrics

**Solution**: Strategic network pruning based on multi-factor scoring.

## 🛠️ Tools Included

### 1. `connection_analyzer.py`
Main analysis tool that scores all your connections based on:
- **Activity Score** (40 pts): Time since connection
- **Engagement Score** (30 pts): Interaction with your posts
- **Relevance Score** (15 pts): Industry/company alignment
- **Strategic Value** (15 pts): Position/role importance

**Output**: Scored, tiered list of removal candidates (0-100 scale)

### 2. `engagement_tracker.py`
Combines multiple post engagement CSV files into a master engagement list.

**Use Case**: If you've scraped engagement data from multiple posts using Phantombuster/Evaboot, this consolidates them.

### 3. `RESEARCH_FINDINGS.md`
Comprehensive research documentation covering:
- LinkedIn algorithm behavior (2025)
- Engagement metrics and benchmarks
- Data export capabilities
- Removal best practices and safety limits
- Third-party tools and methods

## 📥 Data Requirements

### Required: Connections Export

**How to get it:**
1. Go to LinkedIn → Settings & Privacy
2. Navigate to: Data Privacy → Get a copy of your data
3. Select: "Connections" only (faster download)
4. Request archive
5. Download and extract `Connections.csv`

**Expected format:**
```csv
First Name,Last Name,Email Address,Company,Position,Connected On
John,Doe,john@email.com,TechCorp,Engineer,15 Jan 2023
```

### Optional: Engagement Data

**Option A - Manual Tracking:**
Track who engages with your posts over 2-4 weeks manually.

**Option B - Scraping Tools:**
Use third-party tools to export post engagers:
- **Phantombuster** ($59/mo) - LinkedIn Post Commenter and Liker Scraper
- **Evaboot** ($49/mo) - Export post likers & commenters
- **TexAu** ($55/mo) - Extract likers from LinkedIn posts

**Expected format:**
```csv
Name,First Name,Last Name,Company,Position
Sarah Johnson,Sarah,Johnson,DataCo,Data Scientist
```

## 🚀 Quick Start

### Installation

```bash
# Clone or download this repository
cd LinkedIn-User-Analysis

# No additional dependencies required - uses Python 3 standard library
python3 --version  # Ensure Python 3.6+ is installed
```

### Basic Usage

**1. Analyze connections without engagement data:**

```bash
python connection_analyzer.py --connections Connections.csv
```

This will score connections based on connection age and profile completeness (proxy metrics).

**2. Analyze with engagement data:**

```bash
python connection_analyzer.py \
    --connections Connections.csv \
    --engagement master_engagement.csv \
    --output removal_candidates.csv
```

**3. Filter by target industries/companies:**

```bash
python connection_analyzer.py \
    --connections Connections.csv \
    --engagement master_engagement.csv \
    --industries Software Technology "Data Science" \
    --companies Google Microsoft Amazon Meta \
    --output removal_candidates.csv
```

**4. Combine engagement from multiple posts:**

```bash
python engagement_tracker.py \
    --posts post1_likers.csv post2_likers.csv post3_likers.csv \
    --output master_engagement.csv
```

## 📊 Understanding the Output

### Removal Tiers

The analyzer generates 4 tiers:

#### **Tier 1 - High Confidence (0-30 points)**
- Strong removal candidates
- Typically: inactive >24 months, zero engagement, incomplete profiles
- **Action**: Start removing these (10-30/day limit)

#### **Tier 2 - Medium Confidence (31-50 points)**
- Consider removal
- Typically: inactive 12-24 months, minimal engagement
- **Action**: Review and remove if misaligned with goals

#### **Tier 3 - Low Confidence (51-70 points)**
- Manual review needed
- Typically: some activity or engagement, but limited
- **Action**: Keep unless specific reason to remove

#### **Keep (71-100 points)**
- Valuable connections
- Active, engaged, or strategically important
- **Action**: Maintain relationships

### Sample Output

```
CONNECTION ANALYSIS SUMMARY
============================================================

Total Connections: 850
Average Score: 45.3/100

Removal Tier                   Count      Percentage
------------------------------------------------------------
Tier 1 - High Confidence       315        37.1%
Tier 2 - Medium Confidence     280        32.9%
Tier 3 - Low Confidence        155        18.2%
Keep                           100        11.8%
------------------------------------------------------------

Zero Engagement: 595 (70.0%)

============================================================

💡 Recommendations:
  • Start removing Tier 1 connections (315 candidates)
  • Safe removal rate: 10-30 per day
  • Estimated cleanup time: 11 - 32 days
============================================================
```

### CSV Output Columns

The generated `removal_candidates.csv` includes:

| Column | Description |
|--------|-------------|
| Full Name | Connection's full name |
| Email | Email address (if available) |
| Company | Current company |
| Position | Current position |
| Connected On | Date connection was made |
| Days Connected | Days since connection |
| Engagement Count | Times they engaged with your posts |
| Activity Score | 0-40 points |
| Engagement Score | 0-30 points |
| Relevance Score | 0-15 points |
| Strategic Score | 0-15 points |
| **Total Score** | **0-100 points** |
| **Removal Tier** | **Tier 1/2/3 or Keep** |
| Notes | Additional context |

## ⚠️ Important Safety Guidelines

### LinkedIn Limits
- **Safe removal rate**: 10-30 connections per day
- **Risk threshold**: 50+ removals per day may trigger restrictions
- LinkedIn **does NOT notify** users when removed

### Best Practices

1. **Start Small**: Begin with 10-20 obvious candidates
2. **Monitor Impact**: Track engagement rate before/after
3. **Document Removals**: Keep records (can't easily undo)
4. **Consider Unfollow**: Alternative that maintains connection while cleaning feed
5. **Quarterly Reviews**: Make this an ongoing process, not one-time

### Don't Over-Prune

❌ **Don't remove:**
- Strategic connections (even if quiet)
- Recent connections (<3 months)
- Valuable industry contacts (even without direct engagement)
- Potential future opportunities

✅ **Do remove:**
- Obvious spam accounts
- Career-misaligned connections (old industries)
- Inactive >24 months with zero engagement
- Connection collectors with no relationship

## 📈 Measuring Success

### Before You Start
1. Document current engagement rate:
   - Go to: linkedin.com/analytics/creator/content/
   - Calculate: (Reactions + Comments + Shares) / Impressions × 100
   - Record your baseline

2. Note connection count

### After Cleanup
1. Wait 2-4 weeks for algorithm adjustment
2. Recalculate engagement rate
3. Compare post performance metrics

**Success Indicators:**
- Engagement rate increase >0.5%
- More comments (higher quality engagement)
- Better post visibility (impressions relative to follower count)
- More profile views from posts

## 🔄 Complete Workflow

### Phase 1: Data Collection (Week 1)

1. ✅ Export LinkedIn connections
2. ✅ Enable Creator Mode
3. ✅ Export post analytics (6-12 months)
4. ⚡ Optional: Scrape engagement data from recent posts (10-20 posts)
5. ✅ Document baseline engagement rate

### Phase 2: Analysis (Week 2)

1. ✅ Run `engagement_tracker.py` (if using scraped data)
2. ✅ Run `connection_analyzer.py` with your parameters
3. ✅ Review `removal_candidates.csv`
4. ✅ Manually review Tier 1 candidates (sanity check)
5. ✅ Create removal plan (10-30/day schedule)

### Phase 3: Execution (Weeks 3-6)

1. ✅ Start with Tier 1 removals
2. ✅ Remove 10-30 per day consistently
3. ✅ Track removals in spreadsheet
4. ✅ Monitor for any LinkedIn warnings

### Phase 4: Measurement (Weeks 7-8)

1. ✅ Wait 2 weeks after last removal
2. ✅ Measure new engagement rate
3. ✅ Compare post performance
4. ✅ Decide if continuing to Tier 2

### Phase 5: Maintenance (Quarterly)

1. ✅ Re-export connections (every 3 months)
2. ✅ Re-run analysis
3. ✅ Remove new inactive/misaligned connections
4. ✅ Maintain high-quality network

## 🔧 Advanced Customization

### Customize Scoring Weights

Edit `connection_analyzer.py` to adjust scoring:

```python
# In Connection class methods, modify point allocations:

def calculate_activity_score(self):
    if last_activity_days <= 90:
        self.activity_score = 40  # ← Adjust these values
    elif last_activity_days <= 180:
        self.activity_score = 30  # ← Based on your preferences
    # ...
```

### Add Custom Strategic Keywords

```python
# In calculate_strategic_score(), customize keywords:
strategic_keywords = [
    'recruiter', 'hiring',  # Recruiting
    'founder', 'ceo', 'cto',  # Leadership
    'investor', 'vc',  # Funding
    'your_target_role'  # Add your specific targets
]
```

### Industry-Specific Filtering

For career pivots, explicitly exclude old industries:

```python
# Add penalty scoring for unwanted industries
if 'old_industry' in self.company.lower():
    self.relevance_score -= 10  # Penalty
```

## 📚 Additional Resources

### Research Documentation
- Read `RESEARCH_FINDINGS.md` for comprehensive background research
- Covers LinkedIn algorithm, engagement metrics, data sources, and methodology

### Third-Party Tools

**Engagement Scraping:**
- [Phantombuster](https://phantombuster.com/) - LinkedIn post scraper
- [Evaboot](https://evaboot.com/) - Post likers export
- [TexAu](https://texau.com/) - Automation platform

**Network Management:**
- [LeadDelta](https://leaddelta.com/) - LinkedIn CRM with bulk removal
- LinkedIn Creator Analytics (native)

**Data Analysis:**
- Python + Pandas (included in our tools)
- Excel/Google Sheets (for manual analysis)

## 🤝 Contributing

This toolkit was created based on systematic research of LinkedIn best practices (2025). Contributions welcome:

- Additional scoring algorithms
- Integration with LinkedIn API (when available)
- Visualization tools
- Success metrics tracking

## ⚖️ Disclaimer

This tool is for educational and analytical purposes. Users are responsible for:
- Complying with LinkedIn's Terms of Service
- Making ethical decisions about connection management
- Using third-party scraping tools at their own risk

**Note**: While connection removal itself is permitted, web scraping may violate LinkedIn TOS. Use judgment and understand the risks.

## 📝 License

Open source - use, modify, and distribute freely.

---

## 🎓 Examples

### Example 1: Basic Analysis

```bash
# Just downloaded Connections.csv from LinkedIn
python connection_analyzer.py --connections Connections.csv
```

**Output**: Scored list based on connection age and profile completeness.

### Example 2: With Engagement Data

```bash
# Scraped engagement from 15 recent posts, combined into master list
python engagement_tracker.py \
    --posts post_*.csv \
    --output my_engagement.csv

# Now analyze with engagement data
python connection_analyzer.py \
    --connections Connections.csv \
    --engagement my_engagement.csv \
    --output candidates.csv
```

**Output**: More accurate scoring including actual engagement behavior.

### Example 3: Career Pivot (Software Engineer → Data Science)

```bash
# Prioritize data science industry, penalize old connections
python connection_analyzer.py \
    --connections Connections.csv \
    --engagement my_engagement.csv \
    --industries "Data Science" "Machine Learning" "AI" \
    --companies "Google" "Meta" "DeepMind" "OpenAI" \
    --output pivot_candidates.csv
```

**Output**: Optimized for career transition, keeps relevant new industry connections.

---

## 🆘 Troubleshooting

**Q: "No module named pandas"**
A: This toolkit uses only Python standard library - no pandas needed. Ensure Python 3.6+.

**Q: "Error loading connections"**
A: Check CSV format matches LinkedIn export. Expected columns: "First Name", "Last Name", "Connected On", etc.

**Q: "All engagement scores are 0"**
A: Normal if you didn't provide `--engagement` file. Tool will use connection age as primary scoring factor.

**Q: "Too many Tier 1 candidates"**
A: This is common! Start with most obvious removals. You don't have to remove everyone in Tier 1.

**Q: "Engagement rate didn't improve"**
A: Wait 2-4 weeks for algorithm adjustment. Also check if you're creating engaging content - removal alone won't fix poor content.

---

## 📞 Need Help?

1. Check `RESEARCH_FINDINGS.md` for detailed methodology
2. Review example CSVs in `examples/` directory
3. Run tools with `--help` flag for usage info
4. Open an issue on GitHub

---

**Built with research-driven methodology. Start optimizing your LinkedIn network today!** 🚀
