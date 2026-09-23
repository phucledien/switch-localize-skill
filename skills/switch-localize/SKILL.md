---
name: switch-localize
description: Research and build Nintendo Switch game translation patches for Vietnamese or another target language, including dialogue, fonts, menus, HUD, image-based text, validation, and installation on a user's mod-capable console. Use for fan-localization projects and translation-patch fixes; inspect each game's formats before choosing an implementation.
---

# Switch game localization

Deliver a reproducible, source-validated localization patch for the requested game, version and language. This is an engineering and editorial workflow, not a universal game converter. Vietnamese is a supported workflow, not an assumed target when the user requests another language.

## Establish the project

Recover existing project notes and authorization before starting over. Identify the game, application title ID, region, installed version, source/target language, language slot to replace, engine/runtime, available extracted files, and console/mod environment. Ask only for consequential missing facts; inspect accessible files first. Treat archive filenames as hints, not authoritative title IDs.

Record a project configuration and source manifest using [project structure](references/project-structure.md). Keep originals immutable and keep work-in-progress, reviewed translation and release folders separate. If extraction is needed, read [private inputs and extraction](references/private-inputs.md), then use the user's own available game dump and local tools appropriate to its format. Keep keys and console-unique data outside reports, logs, skills and release archives; request paths rather than key contents. A RomFS-only project may be enough until executable analysis is actually needed.

Optional read-only inventory helper:

Bundled helpers require Python 3.9+ and only its standard library. Commands below are relative to this skill's directory; resolve the script path there and pass the actual project paths, rather than changing or guessing the project's root.

```sh
python3 scripts/inventory_assets.py /path/to/extracted/romfs --output /path/to/project/research/inventory.json
```

Add `--hash` when a complete input hash inventory is useful. This recognizes signatures and extensions as clues, not proof of the engine or active language assets. For new tool/firmware combinations, consult current official upstream documentation rather than assuming this project's historical versions still apply.

## Choose the format path

Inspect real assets and establish a lossless unchanged round trip before translating. Trace active language/resource loading: duplicate JP/SC/TC/PC/Switch assets can coexist. Classify dialogue, choices, runtime strings, speaker names, baked labels, startup screens and bonus/gallery content separately. Read [engine and asset mechanics](references/engine-assets.md) for Unity, script and native-code pitfalls. Use its Unity guidance only if inspection supports that engine.

Prove a narrow vertical slice when needed: one changed dialogue, target-language glyphs, a choice/name substitution, and a menu button. Existing successful tests should be reused. Agree on test cadence from the user's instructions; a user-requested final-only test does not justify repeatedly pausing for intermediate console checks. Continue offline checks and report the untested hardware boundary accurately.

## Translate and build

Use [translation and typography](references/translation-typography.md) for scene context, terminology, Vietnamese pronouns, other language requirements, font selection and layout. Never promote a filled machine-draft cache into reviewed coverage. Preserve immutable source identity and protected syntax; edit only demonstrated display fields. Review recurring lines against speaker, context and chronology before reusing them.

Audit image-based buttons and every interaction state, including controller guides, route filters, new/completed badges, name entry, save/load, bonus screens, startup notices and ending captions. A translated runtime literal does not prove a duplicate texture caption is translated. Use available image-editing capabilities for raster text; preserve the original geometry and non-target art. Read [image-text localization](references/image-text.md) for discovery, exact-text prompts, atlas registration and reopened visual review. Read the environment's image-generation skill when available. Do not claim image-generation capability when no suitable tool is available.

Build from reviewed inputs, pinning original hashes. Reopen serialized outputs and verify intended object changes, protected data and asset integrity checks. Native fixes are a last-resort, build-specific component; never reuse an address or hook from another version by analogy.

## Finish and deliver

Follow [validation and release](references/validation-release.md). Distinguish authored/reviewed coverage, locally validated coverage and hardware-tested coverage. Keep translation counts separate from repeated texture cells or interaction states. State preserved content such as audio/video/branding and any known missing surfaces or deliberate non-literal adaptations.

The manifest helper verifies file identity only, not translation quality or game compatibility:

```sh
python3 scripts/payload_manifest.py create /path/to/title-payload \
  --output /path/to/release/manifest.json --title-id 0123456789ABCDEF \
  --game-version 1.0 --language vi
python3 scripts/payload_manifest.py verify /path/to/title-payload \
  --manifest /path/to/release/manifest.json
```

`title-payload` is a deliberately assembled folder containing `romfs/` and, only if needed, `exefs/`; do not point it at an extracted game, entire SD card or key directory. Supply the actual verified title ID. Verification is strict about extra files by default; `--allow-extra` is available for an installed directory with known generated cache files, and reports extras.

Install only within the user's authorized scope, after creating a concrete verified package and rollback plan. A missing card does not block translation or packaging. Do not create scheduled continuations, public uploads or new tasks unless requested. Finish the authorized work directly and carry forward durable progress notes across sessions.

This public skill includes no game files, keys, fonts, translation corpus or executable patches. Read [publication boundaries](references/publication-boundaries.md) before sharing project material. This repository’s synthetic demos illustrate the workflow, not game compatibility.
