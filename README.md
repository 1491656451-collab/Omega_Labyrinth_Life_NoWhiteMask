# Omega Labyrinth Life 去除插画圣光遮罩

这是《Omega Labyrinth Life》Steam PC 版的补丁构建工具。它会将 `illust.unity3d` 中名为 `spa_*effB` 的白色插画遮罩替换为透明纹理。

本仓库不包含任何游戏文件；补丁始终从使用者自己安装的正版游戏资源生成。

## 作用范围

- 仅处理 `OmegaLabyrinth Life_Data/StreamingAssets/StandaloneWindows64/illust.unity3d`。
- 将 26 张 `spa_*effB` 纹理替换为完全透明的 2048x2048 纹理。
- 包含当前 PC 资源包中的普通版与 `_PS4` 厚遮罩变体。
- 不修改模型、材质引用、场景对象、UI、着色器、音频或一般战斗/环境特效。

## 前置条件

- 已安装正版 Steam 版《Omega Labyrinth Life》。
- Python 3.10 或更新版本。

安装依赖：

```powershell
py -3 -m pip install -r requirements.txt
```

## 安装

先完全退出游戏，再在本仓库目录执行：

```powershell
py -3 tools/build_patch.py "D:\SteamLibrary\steamapps\common\Omega Labyrinth Life"
```

工具会先校验原版 Bundle 的 SHA-256，校验通过前不会写入任何文件。随后它会创建 `illust.unity3d.bak0000` 备份、重写运行时 Bundle、重新加载成品包，并确认 26 张目标纹理仍为 2048x2048 且 alpha 均为零。

遇到未知游戏版本时，工具会拒绝执行且不修改文件。重复运行时会验证已安装的补丁。

## 恢复原版

可在 Steam 中执行“验证游戏文件完整性”，或将 `illust.unity3d.bak0000` 覆盖回 `illust.unity3d`。

## 已验证的原版 Bundle

| File | SHA-256 |
| --- | --- |
| `illust.unity3d` | `ceb7809079fc0a6f2b02f3bc5fca10ece1e5971e668c9570375a79510aebfbd1` |

## 技术说明

补丁保留全部 Unity 对象与材质引用：不删除对象，也不做固定偏移的二进制替换；只替换现有 `Texture2D` 对象的像素数据，再让 UnityPy 以原 Bundle 的压缩模式重新打包。

这是非官方修改，请仅用于自己拥有的游戏副本。
