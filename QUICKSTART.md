# Quick Start — 3 Steps

## Step 1: Fill in your competitors

Open `competitors.csv` in any spreadsheet app or text editor.

For each competitor, add whatever URLs you can find:
- website_url → their homepage
- facebook_url → their Facebook page  
- instagram_handle → their Instagram (no @ sign)

Don't stress about getting every URL for every competitor. 
Fill in what you can now, add more later.

**Tip:** The fastest way to find these is to Google each competitor 
name + "facebook" or "instagram" and grab the URLs.


## Step 2: Open Claude Code and paste the prompt

1. Go to Claude Code in your browser
2. Copy the ENTIRE contents of `CLAUDE_CODE_PROMPT.md`
3. Paste it as your first message
4. Claude Code will read your competitors.csv and build everything

Wait for it to finish. It will create all the scrapers, 
the dashboard, and test with sample data.


## Step 3: Run it

Claude Code will tell you the exact commands, but generally:

```
pip install -r requirements.txt
python run_all.py          # scrape everything once
python dashboard/app.py    # launch the dashboard
```

Open http://localhost:5000 and you're in business.


## After that

- Run `python run_all.py` daily or weekly to build up trend data
- Claude Code can help you set up automatic scheduling
- Add new competitors anytime by editing competitors.csv
