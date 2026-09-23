# Translation and typography

## Context and quality

Translate coherent scenes with source speaker, POV, relationships, route/branch, chronology and preceding/following exchanges. Preserve ambiguity until the story reveals it. Do not rewrite an earlier mistaken belief using knowledge from a later route.

Maintain a glossary for verified names, titles, places, fictional terms, repeated UI actions and character-specific address. Distinguish official spellings from editorial romanizations. Repeated dialogue can reuse reviewed text only after source, speaker, field kind and context match; a bonus scene retelling an event from another POV usually needs new narration and pronouns.

Machine translation can provide drafts if useful and permitted by the project's privacy/licensing constraints. Save its model/provider provenance, but keep drafts separate from approved records. Translation coverage means actual source-context review, not rows filled, elapsed runtime or cache hits. Do not send private corpora to a new service without task authorization.

Document deliberate non-literal adaptations and source corrections. Do not present them as literal or silently count omitted text as translated. Handle content restrictions under the current governing instructions and preserve a clear record of the scope of any safe adaptation; do not import another game's scene-specific edits into this project.

## Vietnamese

- Establish speaker-pair address and narrative voice by route and timeline: tôi/mình, tôi/ngài, ta/cô, ta/nàng, anh/em, chị/em, cậu/tớ, huynh/đệ, and court titles are context decisions, not find-and-replace rules.
- Track when forms of address change after recognition, confession, marriage, role-playing or a POV shift. Childhood memories can use a different register from the present scene.
- Preserve Vietnamese accents; normalize authored text to NFC where the engine supports it and test both display and serialization. Removing diacritics is not an acceptable font fix unless the user explicitly chooses that tradeoff.
- Test the full target corpus, including Đ/đ and stacked tone/vowel marks, not only a short alphabet sample. A font can contain a character yet clip its upper/lower marks at the game's line height.
- Prefer an existing compatible font face when it covers the target corpus and preserves layout. If importing one, verify license/distribution rights and engine compatibility. Fallback-only changes may mix faces or fail to select the expected glyph; inspect primary/fallback relationships and actual rendering.
- Render representative names and long dialogue using real game sizes. Include variables with both default and a realistic long custom name, for example “Nguyễn Hoàng Anh”. Preserve the variable token itself in translations.

## Other target languages

Ask or infer the requested locale and style without assuming Vietnamese rules. Evaluate actual script needs: Cyrillic/Greek coverage, Arabic/Hebrew directionality and shaping, Indic conjuncts/reordering, Thai segmentation, CJK glyph variants and line breaking, or language-specific plural/gender formatting. Adding a font is insufficient when the text renderer cannot shape or reorder the script. Establish support with a small proof before promising a complete implementation.

Use the project's native internationalization/plural system when available. Do not reverse RTL strings manually or bake story text into images as an unexamined workaround. If renderer work is required, treat it as a separately validated engine change.

## Layout and protected syntax

Use measured glyph advances at the actual game font, size, scale, spacing and available field width, including a practical margin. Character counts only help triage. Validate visible line count and height as well as width. Test name variants, formatting substitutions, optional branches, combining marks, punctuation and longest buttons/dialogs.

Extract protected tokens with a parser specific to the format. Preserve both content and order, including start-of-line rules when present. A `.tat` control such as `#T` or `#P` is not ordinary prose; a `${FirstName}` or indexed formatting placeholder must survive unchanged. Choice/dialog delimiters and literal `\n` may differ from real newlines. Never impose one game's syntax on another format without inspection.

Resolve overflow by faithful rephrasing, wrapping permitted by the format, or deliberate UI layout changes. Do not silently truncate text. Distinguish measured local fit from on-console evidence, especially with fallback fonts or complex shaping.
