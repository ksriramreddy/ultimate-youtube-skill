# Notices and attribution

Ultimate YouTube is an original, consolidated implementation. Its design was
informed by four open-source projects. No repository was copied wholesale; the
ideas below were studied, combined and re-implemented in a single shared
codebase (`skills/ultimate-youtube/scripts/ytkit/`). Where an approach or
heuristic was adapted, the original project is credited here, and its license
notice is reproduced as its license requires.

| Project | License | What informed this skill |
|---|---|---|
| [AgriciDaniel/claude-youtube](https://github.com/AgriciDaniel/claude-youtube) | MIT | Orchestrator + sub-skill routing pattern, channel size tiers, quota tracker concept, yt-dlp VTT parsing approach, quality gates, optional DataForSEO integration |
| [TubeLabHQ/youtube-research-skills](https://github.com/TubeLabHQ/youtube-research-skills) | MIT | Outlier thinking ("beats its neighbours" median comparison), formula extraction (title slots, thumbnail parts, hook beat orders), beat taxonomy for script breakdowns, evidence-and-links reporting style, niche watchlist deltas |
| [nevaaron/youtube-skill](https://github.com/nevaaron/youtube-skill) | Apache-2.0 | youtube-transcript-api based transcript retrieval, local transcript library with timestamped deep-link search, analytics command set (overview, top videos, demographics, traffic, geography) |
| [nikhilbhansali/youtube-data-skills](https://github.com/nikhilbhansali/youtube-data-skills) | MIT | Separate read-only and write OAuth tokens, preview -> approve -> backup -> revert safety model for metadata writes, "don't retitle a winner" guard, comment category heuristics, retention reading guide |

## Reproduced license notices

### MIT-licensed projects

- claude-youtube: Copyright (c) 2025 Daniel Agrici
- youtube-research-skills: Copyright (c) 2026 TubeLab
- youtube-data-skills: Copyright (c) 2025 Nikhil Bhansali

Each is distributed under the following terms:

```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### youtube-skill

Licensed under the Apache License, Version 2.0
(http://www.apache.org/licenses/LICENSE-2.0). No source files from this project
are included; its approach to transcripts and analytics commands informed the
independent implementation here.

## Third-party services

This skill calls Google's YouTube Data API v3, YouTube Analytics API and
YouTube Reporting API under the user's own credentials, subject to the
[YouTube API Services Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service).
Transcript retrieval uses the open-source `youtube-transcript-api` and,
optionally, `yt-dlp`. Keyword suggestions use Google's public autocomplete
endpoint. Users are responsible for complying with YouTube's terms and
policies.
