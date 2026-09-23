# Validation, release and installation

## Local release gate

Require evidence relevant to the changes, not a large generic test suite:

1. Verified source/version identity and unchanged round-trip for edited formats.
2. Zero missing or unreviewed records within the declared story scope. Rebuild final outputs from the current catalog; stale report counts are insufficient.
3. Protected commands, branch IDs, lookup keys, placeholder order and non-display metadata preserved.
4. Target corpus glyph coverage and meaningful measured layout checks. Inspect rebuilt raster text and all changed interaction states.
5. Reopened serialized outputs match the intended objects/fields; unrelated objects and external references remain intact. Bundle/catalog checksums and sizes agree.
6. Build-specific native checks where code changed, with explicit limitations of mocks/emulation.
7. Final payload assembled from the right components; an old font pilot must not overwrite the full story or expanded metadata. Every copied payload's hash matches its validated input.

Report distinct measures: script files, visible text records, runtime literals, display names, textures and edited rectangles/states. Repeated rectangles are not distinct translated phrases. Record known exclusions and any remaining untested surfaces. “Complete local build” does not mean “fully played through on hardware.”

## Artifact

Package only the intended mod payload, installation/removal/rollback instructions, source and output hashes, target title/version/build/language, validation summary, known limitations and material editorial adaptations. Keep keys, console backups, game images, model caches, and unrelated extracted data out. A private local rebuilt-assets mod is not automatically suitable for public distribution. If public sharing is requested, separately determine a distributable patch format and asset/license constraints before publishing.

Use `scripts/payload_manifest.py` for file-size/hash integrity of an already selected title payload. It does not choose files, prove compatibility, assess translation quality or authorize deployment. Keep its manifest outside the payload root to avoid self-inclusion. Reverify source/version assumptions separately; user-supplied manifest metadata is a claim, not measured proof.

## Card installation

Respect current task authorization; creating/using this skill does not authorize arbitrary mounted-volume writes. When installation is already authorized, prepare and validate the complete package before any final approval step required by the environment.

- Identify the actual mounted card and application folder; never hardcode a previous device path. Record enough device/volume information to avoid another drive.
- Check free space, file-size/filesystem constraints, the expected existing mod and any other contents. Do not merge over unknown mods. Resolve conflicts or build a bounded coexistence plan.
- Preserve the old title folder outside the active `atmosphere/contents` tree with a unique backup path. Do not delete existing backups or save data to make room.
- Stage the new payload outside the active title folder on the same filesystem, verify all hashes from the card, then activate. Where supported, rename old to backup and staged to active, with restoration if activation fails.
- Do not copy stale generated overlay caches from the old mod into the new payload. Determine cache handling for the installed Atmosphère version from evidence/documentation.
- Sync writes and verify the activated payload. Keep a durable installation receipt with actual destination, backup and hashes. Do not claim installation after a partial copy or failed verification.

Stop on changed mount identity, unexpected target contents, source/build mismatch, insufficient space, verification failure or ambiguous activation. Preserve original/live data and explain the concrete blocker. Do not retry an uncertain activation blindly. A failed experiment is not permission to reset/reformat the card or alter the console's boot configuration.

If no card is available, finish the local package and provide exact installation steps. The user can insert the card into a fully powered-off console after safely ejecting it. Final testing should cover boot, the chosen language slot, representative dialogue/choices/names, navigation states, backlog, spare-slot save/load and unlocked galleries/bonus screens. Tailor the sequence to actual changed surfaces and the agreed test cadence.
