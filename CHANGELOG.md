# Changelog

## 1.0.0 - 2026-11-19

First release.

- Single skill `ultimate-youtube` with a routing `SKILL.md`, 16 workflows,
  12 references and 11 templates.
- Shared Python core `ytkit`: API key + separate read/write OAuth tokens, local
  three-bucket quota tracker, retrying API client, ID parsing, network-free
  analysis, transcript engine with library, metadata linter.
- Scripts: `yt_auth`, `yt_publish`, `yt_analytics`, `yt_reporting`,
  `yt_competitors`, `yt_transcripts`, `yt_comments`, `yt_trends`, `yt_seo`.
- Publishing safety: dry run by default, `--confirm` to write, backups,
  `revert`, top-performer warning before retitling.
- Competitor intelligence: neighbour-median outlier detection per format,
  cadence, title-pattern lift, winning terms, length buckets, video evidence
  packs, cross-channel outliers, watchlist with early-breakout detection.
