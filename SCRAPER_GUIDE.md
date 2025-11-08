# DIY LinkedIn Engagement Scraper Guide

## Why DIY Scraping is Better

❌ **Paid Tools** ($50-100/month):
- Phantombuster, Evaboot, TexAu
- Third-party access to your account
- Monthly subscription costs
- Privacy concerns

✅ **Your Own Scraper** (FREE):
- Your data stays with you
- No third-party access
- Completely free
- Same results
- Ethical (it's YOUR data from YOUR account)

---

## 🚀 Quick Start

### Option 1: Playwright (RECOMMENDED)

**More modern, more reliable, better maintained**

```bash
# Install Playwright
pip install playwright

# Install browser
playwright install chromium

# Run scraper
python linkedin_scraper_playwright.py --posts 20 --output my_engagement.csv
```

### Option 2: Selenium

**Older but widely used, more documentation available**

```bash
# Install Selenium
pip install selenium

# Note: Chrome browser must be installed on your system
# ChromeDriver will be auto-downloaded by Selenium

# Run scraper
python linkedin_scraper_selenium.py --posts 20 --output my_engagement.csv
```

---

## 📖 Detailed Setup

### Prerequisites

1. **Python 3.7+** installed
2. **Chrome browser** installed (for Selenium) OR let Playwright install Chromium

### Installation

#### Playwright Setup (Recommended)

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Playwright
pip install playwright

# Install browser binary
playwright install chromium

# Test it
python linkedin_scraper_playwright.py --posts 5
```

#### Selenium Setup

```bash
# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Selenium
pip install selenium

# Make sure Chrome is installed on your system
# Selenium will auto-download ChromeDriver

# Test it
python linkedin_scraper_selenium.py --posts 5
```

---

## 💻 Usage

### First Run (Manual Login Required)

The first time you run the scraper, a browser will open:

```bash
python linkedin_scraper_playwright.py --posts 10
```

**What happens:**
1. Browser opens to LinkedIn
2. You'll see a message: "🔐 MANUAL LOGIN REQUIRED"
3. Log in to LinkedIn manually in the browser
4. Once logged in, your session is saved
5. Scraping begins automatically

**Future runs:** No login needed! Your session is saved.

### Command-Line Options

```bash
# Scrape last 20 posts
python linkedin_scraper_playwright.py --posts 20

# Custom output file
python linkedin_scraper_playwright.py --posts 15 --output engagement_data.csv

# Headless mode (no browser window, after first login)
python linkedin_scraper_playwright.py --posts 10 --headless

# Full example
python linkedin_scraper_playwright.py \
    --posts 25 \
    --output my_posts_engagement.csv \
    --headless
```

---

## 📊 What Gets Scraped

### From Each Post:

✅ **Reactions (Likes)**
- All people who reacted to your post
- Any reaction type (Like, Celebrate, Support, Love, etc.)

✅ **Comments**
- All people who commented
- Top-level comments (not nested replies by default)

### Output Files

**1. Detailed Log** (`my_engagement.csv`):
```csv
Name,Type,Post URL,Date
Sarah Johnson,Reaction,https://linkedin.com/posts/...,2025-11-08T10:30:00
John Doe,Comment,https://linkedin.com/posts/...,2025-11-08T10:30:05
Sarah Johnson,Reaction,https://linkedin.com/posts/...,2025-11-08T10:31:00
```

**2. Summary** (`my_engagement_summary.csv`):
```csv
Name,Total Engagements
Sarah Johnson,15
John Doe,8
Emily Brown,5
```

Use the **summary file** with `connection_analyzer.py`:

```bash
python connection_analyzer.py \
    --connections Connections.csv \
    --engagement my_engagement_summary.csv
```

---

## 🔧 How It Works

### Step-by-Step Process

1. **Login Check**
   - Opens LinkedIn
   - Checks if you're logged in
   - Saves session for future runs

2. **Find Your Posts**
   - Navigates to your activity page
   - Scrolls to find recent posts
   - Collects post URLs

3. **Scrape Each Post**
   - Opens each post
   - Clicks "reactions" to see who liked
   - Scrolls through reactions modal
   - Extracts names from reactions
   - Extracts names from comments
   - Saves to CSV

4. **Rate Limiting**
   - Waits 3 seconds between posts
   - Prevents LinkedIn from flagging as suspicious
   - Small scale = safe

### Session Management

**Playwright:**
- Saves session to `linkedin_state.json`
- Delete this file to force re-login

**Selenium:**
- Saves session to `./linkedin_profile/` directory
- Delete this directory to force re-login

---

## ⚠️ Important Notes

### LinkedIn's Terms of Service

**Is this allowed?**

This is a gray area:
- ✅ **It's YOUR data** - you're accessing your own posts
- ✅ **Small scale** - not mass scraping
- ✅ **No automation of interactions** - just reading data
- ⚠️ **Technically against TOS** - LinkedIn discourages scraping

**Our take:** You're accessing your own data at small scale. This is more ethical than:
- Giving third-party tools full account access
- Paying for data that's already yours
- Mass scraping other people's data

**Use responsibly:**
- Keep it small scale (10-30 posts max)
- Don't run this constantly (once per month is plenty)
- Don't share this tool for mass scraping
- Use at your own discretion

### Rate Limiting & Safety

The scripts include built-in safety features:

✅ **3-second delays** between posts
✅ **Realistic scrolling** behavior
✅ **Small scale** by default (10 posts)
✅ **Session persistence** (no repeated logins)

**Don't:**
- ❌ Scrape hundreds of posts at once
- ❌ Run this multiple times per day
- ❌ Modify to remove rate limiting
- ❌ Use for mass data collection

**Do:**
- ✅ Scrape 10-30 posts max
- ✅ Run once per month
- ✅ Use for personal analytics only

### Privacy

- Your LinkedIn credentials stay local
- No data sent to third parties
- Session files stored locally
- CSV outputs stay on your machine

---

## 🐛 Troubleshooting

### "Browser not found"

**Playwright:**
```bash
# Install browser
playwright install chromium

# If that fails, install all browsers
playwright install
```

**Selenium:**
- Make sure Chrome is installed
- Selenium will auto-download ChromeDriver
- If issues persist: `pip install --upgrade selenium`

### "Can't find post elements"

LinkedIn changes their HTML structure frequently. If scraping fails:

1. Check if you have recent posts
2. Try reducing `--posts` count
3. LinkedIn may have changed selectors (open GitHub issue)

### "Login not working"

- Delete session files and try again:
  - Playwright: `rm linkedin_state.json`
  - Selenium: `rm -rf linkedin_profile/`
- Check if LinkedIn requires 2FA (handle manually)
- Try non-headless mode first

### "No engagements found"

- Check if your posts actually have likes/comments
- LinkedIn may have changed modal structure
- Try with a different post URL manually

### "Script runs but CSV is empty"

- Check terminal output for errors
- LinkedIn's HTML may have changed
- Open a post manually and inspect the reactions modal
- Selectors may need updating

---

## 🔄 Complete Workflow

### 1. Scrape Your Posts (Monthly)

```bash
# Run scraper
python linkedin_scraper_playwright.py --posts 20 --output monthly_engagement.csv

# Output:
#   monthly_engagement.csv (detailed)
#   monthly_engagement_summary.csv (for analysis)
```

### 2. Export LinkedIn Connections (Quarterly)

1. LinkedIn → Settings → Get a copy of your data
2. Select "Connections"
3. Download `Connections.csv`

### 3. Analyze & Generate Removal Candidates

```bash
python connection_analyzer.py \
    --connections Connections.csv \
    --engagement monthly_engagement_summary.csv \
    --output removal_candidates.csv
```

### 4. Review & Remove

1. Open `removal_candidates.csv`
2. Sort by "Total Score" (ascending)
3. Review Tier 1 candidates
4. Remove 10-30 per day via LinkedIn

### 5. Measure Impact

- Wait 2-4 weeks
- Check engagement rate improvement
- Repeat quarterly

---

## 📈 Expected Results

### Scraping Performance

**From 20 posts:**
- Scraping time: 5-10 minutes
- Expected engagements: 100-500 (depends on your network)
- Unique engagers: 50-200

### Analysis Results

**From 850 connections + 20 posts scraped:**

```
Zero Engagement: 595 (70%)
Tier 1 Removal Candidates: 315 (37%)
Tier 2: 280 (33%)
```

**After cleanup:**
- Remove ~300 connections over 2-4 weeks
- Expected engagement rate increase: +0.5% to +2%
- Better post visibility
- More targeted network

---

## 🆚 Comparison: DIY vs Paid Tools

| Feature | DIY Scraper | Phantombuster | Evaboot |
|---------|-------------|---------------|---------|
| **Cost** | FREE | $59/mo | $49/mo |
| **Privacy** | Stays local | Third-party access | Third-party access |
| **Data** | Your account only | Any public data | Any public data |
| **Reliability** | Good (may break on LinkedIn updates) | Good | Good |
| **Setup** | 5 minutes | 10 minutes | 10 minutes |
| **Maintenance** | Update selectors if broken | Handled by vendor | Handled by vendor |
| **Ethics** | Your data only | Can scrape others | Can scrape others |
| **Scale** | Small (10-30 posts) | Large | Large |

**Verdict:** For personal connection analysis, DIY is perfect. For business/large-scale, paid tools may be worth it.

---

## 🎓 Tips & Best Practices

### For Best Results

1. **Run after posting** - Scrape 1-2 days after your last post to capture engagement
2. **Combine multiple runs** - Scrape monthly and combine data:
   ```bash
   python engagement_tracker.py \
       --posts jan_engagement.csv feb_engagement.csv mar_engagement.csv \
       --output quarterly_engagement.csv
   ```
3. **Quality over quantity** - 10 highly-engaged posts > 100 posts with no engagement
4. **Regular cadence** - Monthly scraping shows engagement trends

### Optimizing Scraping

**If scraping fails frequently:**

1. Increase wait times in code:
   ```python
   # Change from 3 to 5 seconds
   await asyncio.sleep(5)
   ```

2. Run in non-headless mode to see what's happening:
   ```bash
   python linkedin_scraper_playwright.py --posts 10
   # (remove --headless flag)
   ```

3. Test with a single post first:
   ```bash
   python linkedin_scraper_playwright.py --posts 1
   ```

### Data Hygiene

- Keep engagement CSVs organized by date:
  - `engagement_2025_01.csv`
  - `engagement_2025_02.csv`
- Backup your data
- Don't commit CSVs to git (already in .gitignore)

---

## 🔮 Future Improvements

Possible enhancements you could add:

- [ ] Scrape post text/content for analysis
- [ ] Track engagement over time (daily snapshots)
- [ ] Identify top engagers per industry
- [ ] Export as JSON for easier processing
- [ ] Add profile information scraping (company, title)
- [ ] Visualizations (engagement heatmaps)
- [ ] Integration with LinkedIn API (if/when available)

---

## 📞 Support

**If the scraper breaks:**

1. Check if LinkedIn updated their UI
2. Inspect element selectors in browser DevTools
3. Update selectors in the Python file
4. Open a GitHub issue with error details

**Common fixes:**

- Update to latest version: `pip install --upgrade playwright selenium`
- Clear session and re-login
- Try the alternative scraper (Selenium vs Playwright)

---

## ⚖️ Disclaimer

This tool is for **personal analytics only**.

**Acceptable use:**
- ✅ Scraping YOUR OWN posts
- ✅ Analyzing YOUR OWN engagement
- ✅ Small scale (10-30 posts)
- ✅ Personal network optimization

**NOT acceptable:**
- ❌ Scraping other people's posts at scale
- ❌ Mass data collection
- ❌ Commercial use without permission
- ❌ Violating LinkedIn TOS intentionally

Use responsibly and ethically. You assume all risk.

---

**Ready to scrape? Start here:**

```bash
pip install playwright
playwright install chromium
python linkedin_scraper_playwright.py --posts 10
```

🚀 **Let's optimize your LinkedIn network!**
