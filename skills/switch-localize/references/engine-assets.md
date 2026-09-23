# Engine and asset mechanics

## Diagnose before editing

Inspect signatures, file inventories, metadata and loading code where needed. A file extension or engine-looking folder is only a clue. Other engines require their own format adapters; the Unity findings here do not justify running Unity tools on unknown data.

For each editable format, demonstrate unchanged byte round-trip, a bounded edit, reopening/reparse and preservation of non-display data. Discover alignment, string length fields, compression and checksums before increasing text length. Prefer structural editing over raw global string replacement.

## Unity / IL2CPP findings

These are format-specific pitfalls to check when the target is actually Unity:

- UI may load from `resources.assets` and ResourceManager paths while similarly named Addressables bundles are fallback or unused assets. Resolve actual language/platform paths and object references.
- Load companion `.resS` streams from the appropriate source when reading unedited streamed textures. A rebuilt `.assets` file alone may not contain them.
- Preserve object path IDs, external file references, sprite rectangles/pivots, animation/cell identifiers and font relationships. Reopen saved files and compare raw object payload hashes: allow only explicit intended IDs/types.
- UnityPy's original object reader can still return old raw bytes before serialization; capture the intended saved object payload, then verify reopened bytes. Do not compare two stale reader views and call the change verified.
- Texture, sprite and animation coordinates can differ in origin. Cell-map and sprite rectangles may use opposite vertical origins. Establish the actual convention using a known visible cell.
- Enumerate dimensions, pixel format, mip count, streaming info, alpha and Switch platform/swizzle metadata. Do not assume one format or no mipmaps. Decode/re-encode using suitable tooling and preserve physical texture layout.
- Some loaders support replacing crunched BC1/BC3 textures with uncrunched DXT1/DXT5 while preserving untouched compression blocks; prove support in the target first. This is not a universal format conversion rule. DXT1 is Unity format10, DXT5 is12 in that tested toolchain; inspect enum/version rather than treating integer5 as DXT1.
- Preserve Switch swizzling and verify swizzle/deswizzle round trips where applicable. Block-aligned edits can affect pixels at rectangle boundaries; inspect reopened output at those boundaries.

### Addressables

Rebuilt bundles may change uncompressed bundle CRC and stored size. Update the correct catalog provider records and offsets while preserving unrelated entries. A filesystem-file CRC is not necessarily the bundle CRC. Derive the algorithm from the actual format/tool; verify original CRCs before modifying them. Do not disable integrity checks as a shortcut. Check whether companion hash/catalog cache files participate in this game's loading path.

### Runtime text and speaker names

Classify IL2CPP metadata literals by actual use. Display labels, lookup keys, resource paths, diagnostics and framework strings can look alike. Preserve indexed literal references and non-target metadata regions when rebuilding.

Speaker name literals may be shared with dictionary keys. Translating a shared key can silently break lookup. Prefer an existing display-only mapping or safe supported interception at the display boundary. Cover fallback names and unknown-name placeholders separately; confirm all keys emitted by scripts resolve. Keep custom-name variables intact.

If a native fix is necessary, pin executable SHA-256, build ID, instruction signatures, data layouts and runtime assumptions. Verify ASLR-relative addressing, stack/register preservation, null/initialization guards and string allocation semantics. Never mutate interned source strings. Emulated tests with mocked calls do not establish Unity/GC/loader safety; report this hardware-test boundary. No address or hook from another build is a reusable patch.

## Raster menu text

Inspect title, save/load, name entry, confirmations, settings, HUD, controller guides, flowchart, galleries, route filters, bonus screens, badges, notices and ending captions. Include normal, selected, pressed, disabled and duplicated volume/language states that the target uses.

For raster editing, use available image-editing tools and inspect local targets first. Separately generated exact lettering masks are often safer than replacing a whole generated atlas. Pack only bounded label regions into original geometry; retain icons, borders, alpha, texture size, sprite layout and non-target blocks. Keep exact prompt text and generated asset provenance in the project.

When removing lettering over patterned art, reconstruct a clean plate and inspect seams. A solid opaque rectangle can destroy a translucent banner's fade. Reuse an appropriate original alpha envelope or carefully restore it, then inspect at native scale over contrasting backgrounds. Preserve original alpha outside the edit. Check every accent after generation, scaling and compression; exact words in a prompt do not guarantee exact pixels.

Export proofs from reopened rebuilt assets, not just working PNGs. A sheet with labels is an intermediate artifact, not a packaged translation.
