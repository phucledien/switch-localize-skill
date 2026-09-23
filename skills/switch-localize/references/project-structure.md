# Project structure and state

Use the game's existing project conventions when present. Otherwise separate:

- `original/` or `extracted/`: immutable user-provided sources, not release inputs by default.
- `research/`: source hashes, asset inventory, active-language mapping, parse/round-trip reports, progress and verification evidence.
- `translations/`: editable reviewed catalog, terminology, scene files and editorial notes.
- `tools/`: game/version-specific parsers, builders and validators.
- `build/drafts/`, `build/work-in-progress/`, `build/release/`: distinct quality stages. Never merge a pilot over the final story.

Keep sensitive extraction material outside these distributable folders. Do not copy a previous project's extracted data or binaries into a skill.

A project configuration should record, with unknown fields explicitly null:

```json
{
  "game": "User-specified title",
  "application_id": null,
  "game_version": null,
  "region": null,
  "executable_build_id": null,
  "source_locale": "zh-Hant",
  "target_locale": "vi",
  "replaced_language_slot": null,
  "engine": null,
  "source_manifest": "research/source-manifest.json",
  "scope": ["story", "choices", "display_names", "menus", "hud", "baked_ui"],
  "preserved_content": [],
  "test_cadence": null
}
```

Do not infer one language's register, writing system or typography requirements from its locale code alone. Configure requested tone, regional spelling, romanization and name handling separately.

## Catalog design

Choose a schema appropriate to the observed format. A useful record has stable ID (`relative file + record/field identity`), immutable source text and hash, source location or byte span, speaker key, scene/branch context, field kind, target text, review state and provenance. File path alone or text hash alone cannot distinguish repeated dialogue.

Example states: `untranslated`, `machine-draft`, `context-reviewed`, `validated`. Define their meaning in the project. Store review evidence at scene level when that matches how the work was performed. A validator cannot award editorial review by checking that text is nonempty.

Protect commands, labels, offsets, parameter syntax, control-code order, placeholders and speaker lookup identifiers. If a parser relies on source offsets, enforce its original file hash before applying replacements. Independently verify an unchanged parse/rebuild equals the exact original bytes, including BOM/newlines/encoding. Recheck protected tokens on changed builds.

Export visible choices and script-dialog arguments as well as ordinary dialogue. Some languages require longer lines; this does not authorize altering branch syntax or truncating meaning.

## Durable checkpoint

Maintain a concise current checkpoint containing:

- User's intended scope and current test/approval preferences.
- Verified game/version/language, current source and artifact hashes.
- Reviewed counts, remaining scenes/UI surfaces and actual validation results.
- Last completed scene/POV and terminology decisions.
- Active processes, their IDs and durable output paths; no fictional background work.
- Exact next useful action and blockers, if any.

Clearly label old checkpoints as historical. Resumption should not restart drafting, overwrite accepted fixes or repeat a request the user already answered.
