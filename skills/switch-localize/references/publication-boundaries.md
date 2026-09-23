# Publication boundaries

A skill repository and a game patch are different deliverables. Keep this repository limited to generic instructions/helpers, synthetic fixtures, original demo art and material the contributor has permission to share.

Exclude keys, firmware, tickets/certificates, console identifiers/backups, game containers, decrypted archives, proprietary fonts, extracted textures/audio/video, full dialogue catalogs, private local paths and project-specific executable patches. Do not publish a historical private case study with its hardware details, output archives or unrelated source excerpts.

Game-specific release decisions require their own review. A binary delta is not automatically free of copyrighted material; rebuilt resources can contain unchanged source art. The repository license grants no rights to commercial games or third-party tools. Never promise that a scan or disclaimer prevents legal complaints.

Before publishing, review the exact Git diff and all staged filenames, inspect images and metadata, run the public-file audit, and verify the complete commit history to be uploaded. A clean new commit does not remove secrets from earlier commits. Use an allowlist and synthetic test data; ignore rules alone do not protect already tracked files.

If sensitive material is found, stop publication of that material. Remove it from the intended upload, assess history exposure, and handle remediation without echoing the secret. Do not upload a problematic commit in order to delete it later.
