# Contributing

Thanks for helping make this better for every creator.

## Principles

1. **Niche-neutral.** No built-in personas, niches or channel data. Examples
   should vary across niches and languages. Creator-specific context belongs in
   their own `channel-profile.md`.
2. **One implementation.** Every API call goes through `scripts/ytkit/`
   (`client.call` for quota + errors, `data.py` for fetchers). Don't add a second
   auth flow or HTTP client.
3. **Writes are always safe.** Any command that changes a channel must dry-run by
   default, require `--confirm`, back up before writing, and be reversible
   where the API allows.
4. **Data, not guesses.** Scripts return numbers; workflows tell the agent how to
   interpret them and how to label inference.
5. **Quota-aware.** Prefer uploads playlists and batched `list` calls over
   `search.list`. Add new methods to `ytkit/quota.py`.
6. **Lean context.** Scripts save full data to files and print compact summaries.

## Layout rules

- `SKILL.md` stays under ~250 lines and routes to `workflows/`.
- Workflows are step-by-step playbooks; references hold background knowledge;
  templates are output skeletons.
- Scripts: argparse CLI, JSON output, `--help` documents every command, PEP 723
  dependency header so `uv run` works.

## Tests

```bash
python -m unittest discover tests -v
```

Add tests for pure logic in `ytkit/` (analysis, parsing, linting, quota). Don't
add tests that need real credentials or network access.
