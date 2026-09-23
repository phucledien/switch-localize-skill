# Contributing

Keep contributions useful across games: format-detection guidance, bounded rebuild checks, typography improvements and original synthetic demonstrations.

- Use fabricated fixtures and original artwork. No commercial game files, extracted assets, dialogue dumps, keys, firmware, tickets or device data.
- Preserve the distinction between a draft, a reviewed translation, a rebuilt file and a tested console result.
- Document the source and license of new material. Do not copy private case studies or proprietary fonts.
- Report issues using minimal synthetic reproductions and redacted logs. Never post a key value or console backup.
- Keep runtime dependencies out of the generic helpers unless there is a concrete need.

Run from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 tools/audit_public.py
```

Review the actual staged files before committing. The audit is a useful guard, not a guarantee that every secret or rights issue can be detected. It intentionally restricts file types and image locations. Any newly allowed binary must receive explicit human review and provenance documentation.

For a suspected secret exposure, do not reproduce the value in a public issue. If GitHub private vulnerability reporting is enabled for this repository, use it; otherwise contact the maintainer privately using a contact channel they publish.
