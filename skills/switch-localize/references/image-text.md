# Find and translate text inside images

## Discover the actual surfaces

Inventory textures and sprite atlases from verified local sources. Inspect native-resolution images plus contact sheets. Use OCR to suggest candidates, then visually confirm: it misses stylized text, tiny stamps and text baked into scenery. Include title/startup screens, menus, HUD, name entry, save/load, galleries, tutorials, maps, calendars, item packaging, signs, stamps, ending cards and movie captions.

Trace normal/selected/pressed/disabled states, active language/platform variants, repeated atlas cells, standalone copies and nested archives. A translated outer resource does not update a byte-identical copy inside another archive. Record source resource/hash, page or object ID, rectangle, locale, text reading, target, active-use evidence and status. Keep unreadable text unresolved rather than inventing it; do not call an asset unused merely because its name looks old.

## Author with image generation when available

Inspect the local image before editing. Use the environment's available image-generation capability and its instructions. If unavailable, report the missing capability and continue other authorized work; do not silently substitute a paid API or claim a generated result exists.

Prefer an isolated exact-lettering master or clean plate when a full-image edit would change art. Give an explicit text list, input role and invariants. Example using an **original fictional test image**:

```text
Use case: text-localization
Edit target: the attached fictional paper card.
Replace only the red stamp lettering 採用 with ACCEPTED.
Keep the oval border, ink wear, angle, paper texture, lighting and all other art.
No extra words. Preserve the original canvas and alpha silhouette.
```

For a real game, use its verified source reading and appropriate translation. The same source word can mean different things in a hiring notice, a selected proposal or an accepted application. Do not infer meaning from a generic demo.

Record the exact prompt, tool/provider, input identity, generated output and review decision in the private project. Inspect generated spelling, punctuation and diacritics. A prompt's correct text does not guarantee correct rendered letters.

## Repack without damaging the game

Register the result to the original geometry. Composite only reviewed text regions; preserve icons, controller glyphs, portraits, borders, pivots, UVs, alpha and unedited pixels/blocks. Do not resize an atlas to accommodate English. Preserve mipmaps, platform swizzling, compression layout and companion metadata as required by the actual format.

Erasing text over a gradient or translucent panel needs a matching clean plate and alpha envelope. Check seams, residual source-language strokes and letters clipped by polygon masks. For compressed formats, report the block-boundary footprint rather than promising pixel identity inside a changed block.

Reopen the **serialized game resource**, render it again and inspect each changed state at native size and expected display scale. Check contrasting backgrounds for transparency. Compare untouched data and copy updates to proven duplicates. Keep a generated image, a reviewed working image, a rebuilt resource and a hardware-tested result as separate milestones.

Public demonstrations should use original synthetic art. Do not publish private source images or extracted game sprites just because they make a compelling before/after.
