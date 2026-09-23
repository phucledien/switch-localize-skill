# Private inputs, keys and local extraction

This guide covers the handoff from a user's own device/files to a private localization workspace. It ships no keys, firmware, payload binaries or game data. Do not fetch key packs, other people's backups, tickets or games. Do not promise that ownership alone settles every legal question about modification or redistribution.

## 1. Establish what the user already has

Record the model/revision, installed firmware, existing mod environment, game region/version and whether the input is an encrypted container or already extracted RomFS. Do not request serial numbers, account credentials or key values. A mod-capable device is a prerequisite for device-side procedures; this skill does not install a modchip, alter boot settings or prescribe a universal exploit.

If usable decrypted files already exist, skip key acquisition. If not, choose a maintained own-device export workflow that actually supports the user's hardware/firmware. Check upstream documentation when doing the task, rather than copying a historical button sequence.

## 2. Guide the user through their own key export, when needed

1. Start with the documentation for the user's existing, trusted console setup and the selected dumper's upstream requirements. Confirm whether that version exports decrypted filesystem sections directly or needs an external key file.
2. When it requires a separate key exporter, verify that exporter's current upstream provenance and exact hardware/firmware support. Older documentation may mention tools that are no longer maintained or available. Do not send the user to an unverified mirror or treat an old payload as a current recommendation.
3. Have the user perform the documented **local key-export operation on their own device**. The agent should name the verified tool/version, source documentation, expected local output filename and compatible setup before giving concrete steps. Do not guess menu labels or automate console operations without authorization.
4. Copy only the required output to a private folder on the user's computer, outside Git and cloud-synced share folders. Common local tools accept a `prod.keys` file; title-rights-encrypted content may require additional locally obtained title-specific material. Requirements vary by tool and content.
5. Give the agent the **file path**, not its contents. Restrict file permissions using the host OS and retain an offline backup. Never print, screenshot, commit, hash into a public manifest, or attach the keys to an issue.
6. Verify the setup by successful metadata parsing/decryption and content integrity checks, not by showing the keys. If compatibility is unverified, stop this setup step and continue with available decrypted inputs; do not change firmware or boot configuration to force progress.

[nxdumptool's upstream repository](https://github.com/DarkMatterCore/nxdumptool) documents device-side dumping, including filesystem-section support. Its [rewrite documentation](https://github.com/DarkMatterCore/nxdumptool/tree/rewrite) distinguishes development builds from older versions. Follow the requirements for the build actually chosen; this reference is not a blanket compatibility endorsement.

## 3. Keep three separate locations

```text
private-secrets/       # Keys and device-specific material; never share
private-game-project/ # Original dump, extracted assets, translation work
switch-localize-skill/# This public instructions-and-tools repository
```

Do not recursively inventory a drive, home folder, SD card or secrets directory. Point inventory helpers at a deliberately selected extracted asset directory. Logs can contain secrets too: disable shell tracing, keep raw extraction logs private, and redact diagnostic excerpts before sharing. Do not paste raw title keys as command-line arguments or environment-variable values.

## 4. Decrypt/extract locally

Use the upstream tool's help and the actual container type. [hactool](https://github.com/SciresM/hactool#usage) documents an external keyset file and NCA RomFS/ExeFS extraction. This example applies only to an already identified **Program NCA**, not directly to every NSP/XCI or update:

```sh
hactool --keyset /private-secrets/prod.keys \
  --romfsdir /private-game-project/extracted/romfs \
  --exefsdir /private-game-project/extracted/exefs \
  /private-game-project/original/program.nca
```

All paths above are illustrative. Confirm flags in the installed version. Do not assume this tool supports every newer content feature. NSP/XCI container extraction, rights handling and update/base merging are separate format-specific steps; identify the correct content using metadata rather than choosing the largest file. Never use placeholder/fake base data for a real translation build.

Verify the application ID, version, region and relevant build ID from the extracted metadata. Hash originals, check the tool's integrity results, then mark sources immutable. Missing-key or integrity failures must be resolved from the user's own inputs; do not suppress errors and call extraction successful. Store the tool/version and nonsecret result summary in the private project.

## 5. Hand off to localization

Run the skill's inventory helper only on extracted assets. Establish unchanged parse/rebuild round trips before editing. Proceed with dialogue, typography, raster discovery and validation; see [engine-assets.md](engine-assets.md) and [image-text.md](image-text.md).

Do not run decryption in public CI or upload inputs to an image-generation service. Any image tool used later receives only the selected visual input the user authorized for that service, never containers, keys or device data.
