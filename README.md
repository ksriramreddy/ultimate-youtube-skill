# Ultimate YouTube - a Claude Code skill for any YouTube creator

One installable skill that lets Claude **publish**, **analyze**, **research
competitors** and **plan content** for any YouTube channel, in any niche and
any language. Real data comes from the official YouTube APIs and public
transcripts; workflow guides tell Claude how to turn that data into decisions.

```
"Upload video.mp4 as a private video scheduled for Friday 6pm"
"Why did my views drop this month?"
"Scan @somechannel and tell me which videos broke out and why"
"Break down this video's hook and structure: <url>"
"Give me 10 video ideas backed by data"
"Write the script, titles, thumbnail brief and upload package for idea #2"
"Run my daily competitor check"
```

## What's inside

| Job | Capabilities |
|---|---|
| **Publish** (Data API v3, write token) | resumable upload, scheduling, edit title/description/tags/privacy, thumbnails, playlists, captions, translated titles/descriptions, delete. Every change is a dry run first, needs explicit approval, is backed up, and can be reverted. |
| **Analyze** (Analytics + Reporting APIs) | overview vs previous period, daily trends, top videos, retention curves with drop-off points, traffic sources, search terms, suggesting videos, external sites, audience, geography, devices, revenue, impressions and CTR, saved reports |
| **Research** (public data, any channel) | competitor discovery, channel scans with outlier detection, cross-channel outliers, "why did this video work" evidence packs, watchlist with early-breakout alerts, transcripts (any public video, any language) with a searchable library, comment mining, autocomplete keywords, search and trending research, SEO audits |
| **Create** (workflows) | onboarding/channel profile, idea scoring, hooks and scripts, titles and thumbnails, upload packages, Shorts, content calendars, audits, strategy and monetization |

### Layout

```
skills/ultimate-youtube/          <- the skill (copy this folder to install)
├── SKILL.md                      master router + rules Claude follows
├── requirements.txt
├── scripts/
│   ├── ytkit/                    shared core: auth, quota, API client, analysis, transcripts, SEO
│   ├── yt_auth.py                setup, doctor, login (read/write tokens), quota
│   ├── yt_publish.py             upload/update/revert/delete/thumbnail/localize/captions/playlists
│   ├── yt_analytics.py           private channel analytics
│   ├── yt_reporting.py           impressions + CTR (Reporting API)
│   ├── yt_competitors.py         scan/compare/outliers/video breakdown/discover/watchlist
│   ├── yt_transcripts.py         transcripts + library search
│   ├── yt_comments.py            comment mining
│   ├── yt_trends.py              autocomplete, search, trending
│   └── yt_seo.py                 metadata linting and audits
├── workflows/                    16 step-by-step playbooks Claude loads on demand
├── references/                   12 knowledge guides (API, algorithm, hooks, packaging, SEO/GEO, ...)
└── templates/                    11 report and planning templates
tests/                            network-free unit tests
```

No niche or persona is built in. Each creator's details live in a
`channel-profile.md` in **their own project**, created by the onboarding workflow.

## Install

Requires Python 3.10+ and Claude Code.

### Option 1: plugin (recommended)

```bash
claude plugin marketplace add ksriramreddy/ultimate-youtube-skill
claude plugin install ultimate-youtube@ultimate-youtube-skill
```

Then ask Claude to "set up the YouTube skill". Its first check installs the
Python dependencies from the skill's `requirements.txt` (or uses `uv run`).

### Option 2: install script

```bash
git clone https://github.com/ksriramreddy/ultimate-youtube-skill.git
cd ultimate-youtube-skill
./install.sh            # macOS / Linux
```

```powershell
.\install.ps1           # Windows PowerShell
```

The scripts copy `skills/ultimate-youtube` to `~/.claude/skills/ultimate-youtube`
and install the Python dependencies. For a single project only, copy the folder
to `<project>/.claude/skills/ultimate-youtube` instead.

### Option 3: uv (no install step for dependencies)

Every script declares its dependencies inline, so with [uv](https://docs.astral.sh/uv/)
you can skip `pip install` and run `uv run scripts/yt_auth.py doctor`.

## Set up credentials

Ask Claude: **"set up the YouTube skill"**. It runs `yt_auth.py doctor` and walks
you through only what you need (full guide: `skills/ultimate-youtube/workflows/setup.md`):

| You want | You need | Time |
|---|---|---|
| Transcripts and keyword suggestions | nothing | 0 min |
| Research any channel/video | a free YouTube Data API key | 5 min |
| Your private analytics | OAuth client + `yt_auth.py login` | 10 min |
| Uploading and editing | `yt_auth.py login --write` (separate token) | 2 min |
| Impressions and CTR | `yt_reporting.py setup`, then wait 24-48h | 1 min |

Credentials, cache, backups and the watchlist live in `~/.ultimate-youtube/`
(override with `YT_SKILL_HOME`), never inside the skill or your repo. Reports go
to `./youtube-reports/` (override with `YT_REPORTS_DIR`).

## Safety

- Research and analytics tokens are **read-only**. Writing uses a separate token
  with only the `youtube.force-ssl` scope; delete `token_write.json` to remove it.
- Every write command is a dry run unless `--confirm` is passed, and Claude is
  instructed to pass it only after you approve that specific preview.
- Updates are backed up and reversible (`yt_publish.py revert`). Uploads default
  to private. Deletion asks twice and suggests making the video private instead.
- A local quota tracker warns before a workflow burns the daily API quota.

## Using the scripts directly

Every script works on its own and prints JSON:

```bash
cd ~/.claude/skills/ultimate-youtube
python scripts/yt_auth.py doctor
python scripts/yt_competitors.py scan @somechannel --max 100 --tz 5.5
python scripts/yt_competitors.py video https://youtu.be/VIDEO_ID --lang en
python scripts/yt_transcripts.py hook https://youtu.be/VIDEO_ID --seconds 45
python scripts/yt_trends.py suggest "home workout" --expand
python scripts/yt_analytics.py overview --days 28
python scripts/yt_publish.py upload video.mp4 --title "..." --not-made-for-kids   # dry run
```

Run `python scripts/<script> --help` for every command and option.

## Development

```bash
python -m unittest discover tests -v
```

Contributions welcome: keep the skill niche-neutral, keep every API call in
`ytkit/`, add tests for pure logic, and never let a write path skip the
dry-run/confirm step. See `CONTRIBUTING.md`.

## Credits and license

MIT licensed (see `LICENSE`). Built by studying and consolidating ideas from
claude-youtube (AgriciDaniel), youtube-research-skills (TubeLab), youtube-skill
(nevaaron) and youtube-data-skills (Nikhil Bhansali); see `NOTICE.md` for what
came from where.

Not affiliated with or endorsed by YouTube or Google. Use within the
[YouTube API Services Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service).
