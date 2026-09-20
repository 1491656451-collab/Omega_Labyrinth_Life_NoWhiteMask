# Validation Record

The original PC `illust.unity3d` bundle contained 34,409 Unity objects and 359 `Texture2D` objects.

The patch targets exactly 26 names: thirteen `spa_*_effB` textures and their thirteen `_PS4` counterparts. All targets are 2048x2048 DXT5 textures.

After rebuilding, the output bundle retained 34,409 objects and 359 `Texture2D` objects. Each target was reloaded from the finished Bundle and verified to have an alpha-channel range of `(0, 0)`.

The completed bundle SHA-256 was:

```text
3e0c6c78a11d0719219c6106e4ffc7169635d783deb94f84b853048feea2795f
```

The result was structurally verified. Runtime scene validation remains a separate check from this repository's static Bundle validation.
