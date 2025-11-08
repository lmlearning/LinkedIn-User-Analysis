# Quick Start Guide - 5 Minutes to Your First Analysis

## Step 1: Get Your LinkedIn Connections (2 minutes)

1. Go to [LinkedIn Settings](https://www.linkedin.com/mypreferences/d/download-my-data)
2. Select "Want something in particular? Select the data files you're most interested in"
3. Check only "Connections"
4. Click "Request archive"
5. Wait for email (usually < 5 minutes)
6. Download and extract `Connections.csv`

## Step 2: Run the Analyzer (1 minute)

```bash
cd LinkedIn-User-Analysis

python connection_analyzer.py --connections /path/to/Connections.csv
```

**Replace** `/path/to/Connections.csv` with your actual file path.

## Step 3: Review Results (2 minutes)

The tool outputs:
1. **Summary stats** in terminal
2. **Detailed CSV** file: `removal_candidates.csv`

Open `removal_candidates.csv` in Excel/Google Sheets and sort by "Total Score" (ascending).

## What to Do Next

### Tier 1 Candidates (Score 0-30)
✅ **Safe to remove** - Start here

**How to remove:**
1. Go to [LinkedIn Connections](https://www.linkedin.com/mynetwork/invite-connect/connections/)
2. Search for the person's name
3. Click the three dots (•••) next to "Message"
4. Select "Remove connection"

**Limit**: 10-30 per day to avoid LinkedIn restrictions

### Tier 2 Candidates (Score 31-50)
⚠️ **Consider removing** - Review first

### Tier 3+ (Score 51+)
❌ **Keep** - These are valuable connections

## Measuring Success

**Before cleanup:**
- Go to [Creator Analytics](https://www.linkedin.com/analytics/creator/content/)
- Note your average engagement rate (reactions + comments / impressions)

**After cleanup (2-4 weeks later):**
- Check if engagement rate increased
- Target: >4% is excellent

---

## Optional: Add Engagement Data

For more accurate analysis, track who actually engages with your posts.

### Free Method (Manual)
For your next 5-10 posts, note who likes/comments in a spreadsheet.

### Paid Method (Automated)
Use Phantombuster ($59/mo) to scrape post engagers:

```bash
# Combine scraped data
python engagement_tracker.py --posts post1.csv post2.csv --output engagement.csv

# Re-run analyzer with engagement data
python connection_analyzer.py \
    --connections Connections.csv \
    --engagement engagement.csv
```

---

## Example Output

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

💡 Recommendations:
  • Start removing Tier 1 connections (315 candidates)
  • Safe removal rate: 10-30 per day
  • Estimated cleanup time: 11 - 32 days
```

---

## FAQ

**Q: Will people know I removed them?**
A: No, LinkedIn does not notify users.

**Q: Can I undo a removal?**
A: You can re-send a connection request, but it requires their re-approval.

**Q: How often should I do this?**
A: Quarterly is recommended.

**Q: What if I don't have engagement data?**
A: The tool still works! It uses connection age and profile completeness as proxies.

---

**That's it! You're ready to optimize your LinkedIn network.** 🚀

For more details, see the full [README.md](README.md) or [RESEARCH_FINDINGS.md](RESEARCH_FINDINGS.md).
