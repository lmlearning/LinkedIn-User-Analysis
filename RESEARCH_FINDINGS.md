# LinkedIn Connection Removal Strategy - Research Findings

## Executive Summary

This document synthesizes comprehensive research on generating candidate lists of LinkedIn connections to remove for increased engagement. Research was conducted systematically across multiple domains including LinkedIn algorithm behavior, engagement metrics, network analysis, and data export capabilities.

**Key Finding**: Quality connections > Quantity is the dominant 2025 LinkedIn strategy. Strategically removing inactive or low-engagement connections can improve your engagement rate and content visibility.

---

## 1. LinkedIn Algorithm & Engagement (2025)

### Current State
- **Average engagement rate**: 3.85% (44% YoY increase)
- **Target "good" engagement rate**: >4%
- **Algorithm priorities**: Quality engagement over quantity
- **Top engagement signal**: Meaningful comments > reactions

### Algorithm Behavior
- LinkedIn favors **active connections** in content distribution
- Tightly curated networks get better post visibility
- Meaningful conversations outperform passive reactions
- Connection quality directly impacts content reach

### Sources
- AuthoredUp, Hootsuite, Buffer, Miracamp (2025 LinkedIn Algorithm Analysis)
- Socialinsider (Engagement rate benchmarks)

---

## 2. Connection Removal Benefits

### Why Remove Connections

1. **Improved Engagement Rates**
   - Smaller, engaged audience = higher percentage engagement
   - Algorithm rewards active networks
   - Better content distribution

2. **Reduced Noise**
   - Cleaner feed with relevant content
   - Focus on high-value relationships
   - Easier relationship management

3. **Strategic Alignment**
   - Network reflects current professional goals
   - Better recruiter/employer impression
   - Aligned with current industry focus

### Safe Removal Limits
- **10-30 removals/day**: Safe limit
- **50+ removals/day**: Risk LinkedIn restrictions
- **LinkedIn DOES NOT notify** users when removed
- Slow, steady cleanup preferred over bulk removal

### Sources
- DowSocial, Cleverly, PhantomBuster (Connection removal strategies)
- Community consensus from multiple LinkedIn expert blogs

---

## 3. Identifying Inactive Connections

### Activity Indicators

**Active User Signals:**
- Green circle (solid) = currently online
- Green/white circle = offline with push notifications
- Recent posts/comments visible
- Updated profile information

**Dormant/Inactive Signals:**
- No status indicator (or yellow dot)
- No activity section (hidden after 360 days)
- Outdated job titles/companies
- No visible posts/comments in months
- No profile updates in 12+ months

### Manual Identification Methods
- Check "Contact info" for connection date
- Review activity section on profile
- Sort connections by industry/company filters
- Look for stale profile information

### Sources
- LinkedIn Help Documentation
- Madhawks, LeadDelta (Inactive account filtering)

---

## 4. Engagement Metrics Available

### Native LinkedIn Analytics (Exportable)

**Post-Level Metrics:**
- Impressions (total views)
- Unique views (signed-in members)
- Reactions (Like, Celebrate, Support, Love, Insightful, Curious, Funny)
- Comments count
- Shares/reposts count
- Clicks (links, profile views)

**Demographics (Aggregated):**
- Job titles of viewers
- Companies of viewers
- Industries represented
- Geographic locations
- Seniority levels
- Company sizes

**Export Location:**
- Creator Analytics: linkedin.com/analytics/creator/content/
- Export button (top right)
- Format: CSV/Excel (.xlsx)
- Time range: Up to 1 year

**Requirement**: Creator Mode must be enabled

### What's NOT Available Natively
- Individual names who viewed (only aggregated demographics)
- List of specific connections who engaged vs. didn't
- Non-engagement tracking (who saw but didn't react)

### Sources
- LinkedIn Help, Sprout Social, Hootsuite (Analytics guides)
- PostLine, OutXAI, Ordinal (Export tutorials)

---

## 5. Third-Party Engagement Scraping

### Available Tools (2025)

**Primary Tools:**
1. **Phantombuster** - LinkedIn Post Commenter and Liker Scraper
2. **Evaboot** - Export post likers & commenters
3. **TexAu** - Extract likers from LinkedIn posts
4. **Bardeen** - Scrape post likes and comments
5. **Captain Data** - Extract LinkedIn post engagers
6. **Apify** - LinkedIn post reactions scraper

### How They Work
1. User provides LinkedIn cookies via browser extension
2. Input post URL(s) to analyze
3. Tool scrapes publicly visible engagement
4. Export as CSV with: names, profiles, job titles, companies

### Data You Can Get
- Complete list of people who liked each post
- Complete list of people who commented
- Profile information of engagers
- Timestamps of engagement
- Ability to cross-reference with your connections

### Important Considerations
- **Terms of Service**: Technically against LinkedIn TOS
- **Privacy**: Only scrapes publicly visible data
- **Widely Used**: Industry standard practice despite TOS
- **Cost**: $50-100/month for full automation
- **Free Tiers**: Most tools offer limited free usage

### Sources
- Evaboot, Phantombuster, ColdIQ, Bardeen documentation
- Multiple scraping tool comparison articles

---

## 6. Network Analysis Approaches

### Downloadable Data

**LinkedIn Data Export:**
- Navigate: Settings & Privacy → Data Privacy → Get a copy of your data
- Select: "Connections"
- Format: CSV file
- Contents: First Name, Last Name, Email, Company, Position, Connected On

### Analysis Metrics

**Network Value Metrics:**
1. **Betweenness Centrality** - Connection acts as bridge between others
2. **PageRank Score** - Overall network influence
3. **Network Density** - How interconnected your network is
4. **Mutual Connection Overlap** - Redundancy between connections

**Demographic Analysis:**
- Companies represented
- Industries distribution
- Geographic locations
- Seniority levels
- Connection growth over time

### Tools for Analysis
- **Python**: Pandas, NetworkX, Pyvis
- **Excel**: Pivot tables, filtering
- **Visualization**: Network graphs, distribution charts

### Historical Tools (No Longer Available)
- Socilab (LinkedIn API closure affected this)

### Sources
- Medium articles by Kamil Matejuk, Richard Cornelius Suwandi
- GitHub: linkedin-network-analysis repositories
- BooleanBlackBelt (Network value analysis)

---

## 7. Reciprocity & Relationship Quality

### Connection Types

**Two-Way (Connections):**
- Mutual, agreed-upon relationship
- Can direct message
- See each other's posts
- Share network access

**One-Way (Follows):**
- No mutual agreement required
- Can see posts but limited interaction
- No direct messaging
- Limited value for engagement

### Reciprocity Principles
- Give before you expect to receive
- Active engagement creates two-way value
- Non-reciprocal connections provide limited benefit
- One-sided relationships drain engagement rate

### Quality Indicators
- Regular mutual engagement
- Relevant professional overlap
- Active conversations/comments
- Network bridge value (mutual connections)

### Sources
- LiSeller, LeadIn, Octopus CRM (Reciprocity guides)
- LinkedIn business blog (Relationship building)

---

## 8. Removal Criteria (Evidence-Based)

### Primary Removal Candidates

**Tier 1 - High Confidence:**
- Obvious spam accounts (>10K connections, no real activity)
- Inactive >24 months with zero engagement ever
- Completely irrelevant industries/roles (career pivot)
- Dormant accounts (no activity in 360+ days)

**Tier 2 - Medium Confidence:**
- Inactive 12-24 months
- Low engagement (<2 interactions ever with your content)
- Career pivot misalignment (past industry)
- Geographic mismatch with no remote relevance

**Tier 3 - Low Confidence (Consider):**
- Inactive 6-12 months but previously engaged
- Relevant industry but no recent interaction
- Connection collectors (high count, low personal engagement)
- Redundant connections (>80% mutual connection overlap)

**Tier 4 - KEEP:**
- Any activity in last 6 months
- Regular engagement with your content
- Strategic connections (recruiters, mentors, influencers)
- High network centrality scores (valuable bridges)
- Target companies/industries for your goals

### Alternative: Unfollow Instead
- Maintains connection (preserves network size)
- Removes their content from your feed
- Useful when relationship has potential future value
- No notification to the other person

### Sources
- DowSocial, Cleverly, Medium articles (Multiple experts)
- CLRN, Moondas (Strategic disconnection guides)

---

## 9. Data Export Capabilities Summary

### What You Can Export From LinkedIn

**Connections Data:**
- ✅ Full connection list with names, companies, positions
- ✅ Connection dates
- ✅ Contact information (if available)
- ❌ Last activity date per connection
- ❌ Engagement history per connection

**Post Analytics:**
- ✅ Aggregate metrics (impressions, reactions, comments, shares)
- ✅ Demographic data (aggregated viewer info)
- ✅ Post performance over time
- ✅ Click data, profile views generated
- ❌ Individual viewer names
- ❌ Which connections viewed/engaged vs. didn't

**Profile Analytics:**
- ✅ Total profile views
- ✅ Search appearances
- ✅ Follower growth
- ✅ Visitor demographics
- ❌ Individual visitor names (only with Premium)

### Third-Party Requirements

To get individual engagement data (who liked/commented), you need:
- Scraping tools (Phantombuster, Evaboot, etc.)
- Your LinkedIn cookies
- Post URLs to analyze
- Acceptance of TOS risk

### Sources
- LinkedIn Help documentation
- Coefficient, Postline, ViewMetrics (Export guides)

---

## 10. 2025 API Improvements

### New Member Post Analytics API

**What's New in 2025:**
- Direct API access to post-level engagement data
- Available through 11+ approved third-party platforms
- Includes: impressions, reach, reactions, comments, reposts
- Granular metrics for member-generated content

**Approved Platforms:**
- Hootsuite
- Buffer
- Sprinklr
- Other social media management tools

**How to Access:**
- Free through simple approval process
- Requires business/professional account
- Better than web scraping (official, compliant)

**Limitations:**
- Privacy thresholds (minimum engagement required to show data)
- Still doesn't provide individual user-level names
- Focused on aggregate metrics

### Sources
- Microsoft Learn (LinkedIn API documentation)
- ContentGrip, Data365 (API updates)
- LinkedIn official announcements

---

## 11. Recommended Implementation Strategy

### Phase 1: Data Collection (Week 1)

1. **Export your connections**
   - Settings → Get a copy of your data → Connections
   - Save as `connections.csv`

2. **Enable Creator Mode & export analytics**
   - Turn on Creator Mode
   - Analytics → Export last 6-12 months
   - Save as `post_analytics.csv`

3. **Track engagement for 2-4 weeks** (Optional but recommended)
   - Screenshot "Who viewed this" for each new post
   - Note who engages (reactions/comments)
   - Build engagement tracking spreadsheet

4. **Optional: Scrape detailed engagement**
   - Use Phantombuster/Evaboot free tier
   - Scrape last 10-20 posts
   - Export engagers list as `engagers.csv`

### Phase 2: Analysis (Week 2)

1. **Build scoring database**
   - Import connections.csv
   - Cross-reference with engagers.csv (if available)
   - Calculate activity score per connection

2. **Apply scoring algorithm** (see next section)

3. **Generate tiered candidate lists**
   - Tier 1: High confidence removals
   - Tier 2: Medium confidence
   - Tier 3: Consider/review manually

### Phase 3: Execution (Week 3+)

1. **Baseline measurement**
   - Document current engagement rate
   - Average reactions/comments per post
   - Total connections count

2. **Start with Tier 1**
   - Remove 10-30 per day (stay within safe limits)
   - Track removals in spreadsheet

3. **Monitor impact**
   - Measure engagement rate changes
   - Track algorithm improvements
   - Note any issues

4. **Iterate to Tier 2** (if results positive)
   - Continue cautious removal
   - Adjust criteria based on learnings

### Phase 4: Optimization (Ongoing)

1. **Quarterly reviews**
   - Re-export connections
   - Re-analyze engagement
   - Generate new candidate list

2. **Refinement**
   - Adjust scoring weights
   - Update criteria based on career changes
   - Maintain high-quality network

---

## 12. Scoring Algorithm

### Activity-Based Scoring System

```
TOTAL SCORE (0-100 points):

Component 1: Last Activity Date (0-40 points)
├── 0-3 months: 40 points
├── 3-6 months: 30 points
├── 6-12 months: 15 points
├── 12-24 months: 5 points
└── 24+ months: 0 points

Component 2: Engagement Reciprocity (0-30 points)
├── Regular engagement (5+ interactions): 30 points
├── Occasional engagement (2-4 interactions): 15 points
├── Minimal engagement (1 interaction): 5 points
└── Never engages: 0 points

Component 3: Profile Quality/Relevance (0-15 points)
├── Complete, updated, current industry: 15 points
├── Complete but outdated or adjacent industry: 8 points
├── Incomplete or past industry: 3 points
└── Minimal info or spam account: 0 points

Component 4: Strategic Value (0-15 points)
├── High value (recruiter, influencer, target company): 15 points
├── Medium value (same industry, good network): 10 points
├── Low value (general connection): 5 points
└── No clear value: 0 points

REMOVAL THRESHOLDS:
├── 0-30 points: Strong removal candidate (Tier 1)
├── 31-50 points: Consider removal (Tier 2)
├── 51-70 points: Review manually (Tier 3)
└── 71-100 points: Keep
```

### Behavioral Pattern Filter

```
AUTO-REMOVE IF ALL TRUE:
✓ Zero interactions in last 12 months
✓ No profile visits (either direction)
✓ <3 mutual connections OR connection collector (>5000 connections)
✓ Account shows dormancy (no green indicator tested over 7 days)
✓ Connected >12 months (sufficient time to engage)
```

---

## 13. Key Insights & Takeaways

### Top 10 Insights

1. **Quality > Quantity is proven**: 2025 algorithm heavily rewards engaged networks
2. **Safe limits exist**: 10-30 removals/day, no notifications sent
3. **Data is partially accessible**: Connections export yes, engagement details via scraping
4. **Creator Mode required**: Must enable for analytics export
5. **API improvements coming**: 2025 brings better official data access
6. **Unfollow is alternative**: Keeps network size while cleaning feed
7. **Privacy thresholds**: LinkedIn hides low-engagement metrics
8. **Reciprocity matters**: One-sided connections drag down engagement
9. **Quarterly maintenance**: Network pruning should be regular, not one-time
10. **Career alignment critical**: Network should reflect current goals, not past

### Common Mistakes to Avoid

1. **Over-pruning**: Don't remove valuable quiet connections
2. **Ignoring context**: Some connections are strategic despite low engagement
3. **Bulk removal**: Triggers LinkedIn restrictions
4. **No documentation**: Can't reverse easily, track what you remove
5. **One-time cleanup**: Should be ongoing quarterly process
6. **Ignoring alternatives**: Unfollow often better than removal
7. **No baseline measurement**: Can't prove impact without before/after data

---

## 14. Tools & Resources

### Free Tools
- LinkedIn native exports (connections, analytics)
- Python + Pandas for analysis
- Excel for basic scoring

### Paid Tools ($50-100/month)
- Phantombuster (scraping)
- Evaboot (engagement export)
- TexAu (automation)
- LeadDelta (CRM + bulk removal)

### Analysis Libraries
- Python: pandas, networkx, pyvis
- Visualization: matplotlib, seaborn, plotly

### Official Resources
- LinkedIn Creator Analytics
- LinkedIn Help Documentation
- Microsoft Learn (API docs)

---

## 15. Conclusion

Generating an effective LinkedIn connection removal candidate list requires:

1. **Clear data collection**: Connections export + engagement tracking
2. **Systematic scoring**: Multi-factor algorithm considering activity, engagement, relevance
3. **Tiered approach**: High/medium/low confidence removal candidates
4. **Safe execution**: Respect platform limits (10-30/day)
5. **Impact measurement**: Track engagement rate improvements
6. **Ongoing maintenance**: Quarterly reviews and updates

**The bottom line**: You CAN use exported post analytics combined with connection data to judge engagement, but you'll need either:
- Manual tracking of who engages over time, OR
- Third-party scraping tools to get individual engagement data

The most practical approach is a **hybrid**: Use native LinkedIn exports for aggregate data and scoring, supplement with limited scraping for validation, and maintain a systematic scoring system that prioritizes inactive, non-engaging, and misaligned connections for removal.

---

## Research Methodology

This document synthesizes findings from:
- **15 web searches** across multiple domains
- **50+ source articles** from LinkedIn experts, analytics platforms, and official documentation
- Focus on **2025-current** information to ensure relevance
- Systematic coverage of: algorithm behavior, metrics, tools, methods, best practices

**Research Date**: November 8, 2025
**Last Updated**: November 8, 2025
