# Omega Labyrinth Life No White Mask

Build tool for the Steam PC version of Omega Labyrinth Life that removes the white illustration masks stored as `spa_*effB` textures in `illust.unity3d`.

This repository contains no game files. It creates the patch from the user's own installed copy.

## Scope

- Patches only `OmegaLabyrinth Life_Data/StreamingAssets/StandaloneWindows64/illust.unity3d`.
- Replaces 26 `spa_*effB` textures with fully transparent 2048x2048 textures.
- Includes both standard and `_PS4` mask variants present in the active PC bundle.
- Does not modify models, materials, scene objects, UI, shaders, audio, or ordinary gameplay effects.

## Requirements

- A legitimate Steam installation of Omega Labyrinth Life.
- Python 3.10 or later.

Install dependencies:

```powershell
py -3 -m pip install -r requirements.txt
```

## Install

Exit the game, then run this from the repository directory:

```powershell
py -3 tools/build_patch.py "D:\SteamLibrary\steamapps\common\Omega Labyrinth Life"
```

The tool validates the original bundle SHA-256 before it writes anything. It creates `illust.unity3d.bak0000`, rewrites the active bundle, reloads the completed bundle, and checks that all 26 target textures are still 2048x2048 with alpha values of zero.

It rejects an unknown game version without changing files. Running it again verifies an already-installed patch.

## Restore

Use Steam's "Verify integrity of game files" command, or replace `illust.unity3d` with `illust.unity3d.bak0000`.

## Known Original Bundle

| File | SHA-256 |
| --- | --- |
| `illust.unity3d` | `ceb7809079fc0a6f2b02f3bc5fca10ece1e5971e668c9570375a79510aebfbd1` |

## Technical Notes

The patch retains every Unity object and material reference. Rather than deleting an object or performing fixed-offset binary edits, it replaces pixel data in the existing `Texture2D` objects and lets UnityPy rebuild the Bundle using its original compression mode.

This project is an unofficial modification. Use it only with a copy of the game you own.
