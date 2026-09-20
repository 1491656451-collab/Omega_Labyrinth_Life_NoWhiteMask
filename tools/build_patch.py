#!/usr/bin/env python3
"""构建 Omega Labyrinth Life 的插画白色遮罩去除补丁。

本工具仅处理 PC 版实际使用的 illust.unity3d。它不会分发或下载游戏资源，
使用者须提供自己安装的游戏副本。
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
        raise RuntimeError(f"应有 {EXPECTED_TEXTURES} 张 spa_*effB 纹理，实际找到 {len(targets)} 张")
    for texture in targets:
        if (texture.m_Width, texture.m_Height) != (2048, 2048):
            raise RuntimeError(f"{texture.m_Name} 尺寸异常：{texture.m_Width}x{texture.m_Height}")
        if texture.image.convert("RGBA").getchannel("A").getextrema() != (0, 0):
            raise RuntimeError(f"纹理并非完全透明：{texture.m_Name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="构建 Omega Labyrinth Life 去除白色遮罩补丁。")
    parser.add_argument("game_root", type=Path, help="Omega Labyrinth Life 游戏安装目录")
    args = parser.parse_args()

    bundle = args.game_root / RELATIVE_BUNDLE
    backup = bundle.with_name(bundle.name + ".bak0000")
    if not bundle.is_file():
        raise SystemExit(f"找不到游戏 Bundle：{bundle}")

    current_hash = sha256(bundle)
    if current_hash == PATCHED_SHA256:
        verify_patched_bundle(bundle)
        print("补丁已安装，验证通过。")
        return 0
    if current_hash != ORIGINAL_SHA256:
        raise SystemExit(
            "illust.unity3d 的哈希不符合已知原版，未修改任何文件。"
            "请在 Steam 验证游戏文件后重试。\n"
            f"预期原版：{ORIGINAL_SHA256}\n实际哈希：{current_hash}"
        )
    if backup.exists():
        raise SystemExit(f"备份已存在：{backup}。未修改任何文件。")

    shutil.copy2(bundle, backup)
    try:
        env = UnityPy.load(str(backup))
        textures = target_textures(env)
        if len(textures) != EXPECTED_TEXTURES:
            raise RuntimeError(f"应有 {EXPECTED_TEXTURES} 张 spa_*effB 纹理，实际找到 {len(textures)} 张")
        for texture in textures:
            transparent = Image.new("RGBA", (texture.m_Width, texture.m_Height), (0, 0, 0, 0))
            texture.set_image(transparent)
            texture.save()
        bundle.write_bytes(env.file.save(packer="original"))
        verify_patched_bundle(bundle)
    except Exception:
        shutil.move(backup, bundle)
        raise

    print("补丁已安装并验证通过。")
    print(f"备份：{backup}")
    print(f"已处理纹理：{EXPECTED_TEXTURES} 张")
    return 0


if __name__ == "__main__":
    sys.exit(main())
