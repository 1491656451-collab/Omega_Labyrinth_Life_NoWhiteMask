#!/usr/bin/env python3
"""Build the Omega Labyrinth Life illustration white-mask removal patch.

This tool only handles the PC game's active illust.unity3d bundle. It never
ships or downloads game assets; the user supplies their own installed copy.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

import UnityPy
from PIL import Image


RELATIVE_BUNDLE = Path("OmegaLabyrinth Life_Data") / "StreamingAssets" / "StandaloneWindows64" / "illust.unity3d"
ORIGINAL_SHA256 = "ceb7809079fc0a6f2b02f3bc5fca10ece1e5971e668c9570375a79510aebfbd1"
PATCHED_SHA256 = "3e0c6c78a11d0719219c6106e4ffc7169635d783deb94f84b853048feea2795f"
EXPECTED_TEXTURES = 26


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def target_textures(env: UnityPy.Environment) -> list:
    matches = []
    for obj in env.objects:
        if obj.type.name != "Texture2D":
            continue
        texture = obj.read()
        name = texture.m_Name.lower()
        if name.startswith("spa_") and "effb" in name:
            matches.append(texture)
    return matches


def verify_patched_bundle(path: Path) -> None:
    env = UnityPy.load(str(path))
    targets = target_textures(env)
    if len(targets) != EXPECTED_TEXTURES:
        raise RuntimeError(f"expected {EXPECTED_TEXTURES} spa_*effB textures, found {len(targets)}")
    for texture in targets:
        if (texture.m_Width, texture.m_Height) != (2048, 2048):
            raise RuntimeError(f"unexpected dimensions for {texture.m_Name}: {texture.m_Width}x{texture.m_Height}")
        if texture.image.convert("RGBA").getchannel("A").getextrema() != (0, 0):
            raise RuntimeError(f"texture is not fully transparent: {texture.m_Name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the Omega Labyrinth Life no-white-mask patch.")
    parser.add_argument("game_root", type=Path, help="Omega Labyrinth Life installation directory")
    args = parser.parse_args()

    bundle = args.game_root / RELATIVE_BUNDLE
    backup = bundle.with_name(bundle.name + ".bak0000")
    if not bundle.is_file():
        raise SystemExit(f"Missing game bundle: {bundle}")

    current_hash = sha256(bundle)
    if current_hash == PATCHED_SHA256:
        verify_patched_bundle(bundle)
        print("Patch is already installed and verified.")
        return 0
    if current_hash != ORIGINAL_SHA256:
        raise SystemExit(
            "Unexpected illust.unity3d hash. No files were changed. "
            "Verify game files in Steam, then run this tool again.\n"
            f"Expected original: {ORIGINAL_SHA256}\nActual:            {current_hash}"
        )
    if backup.exists():
        raise SystemExit(f"Backup already exists: {backup}. No files were changed.")

    shutil.copy2(bundle, backup)
    try:
        env = UnityPy.load(str(backup))
        textures = target_textures(env)
        if len(textures) != EXPECTED_TEXTURES:
            raise RuntimeError(f"expected {EXPECTED_TEXTURES} spa_*effB textures, found {len(textures)}")
        for texture in textures:
            transparent = Image.new("RGBA", (texture.m_Width, texture.m_Height), (0, 0, 0, 0))
            texture.set_image(transparent)
            texture.save()
        bundle.write_bytes(env.file.save(packer="original"))
        verify_patched_bundle(bundle)
    except Exception:
        shutil.move(backup, bundle)
        raise

    print("Patch installed and verified.")
    print(f"Backup: {backup}")
    print(f"Patched textures: {EXPECTED_TEXTURES}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
