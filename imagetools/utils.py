from __future__ import annotations

import os
import math
import shutil
from typing import Optional, Tuple

from PIL import Image, ImageOps, ImageDraw


def _ensure_backup(image_path: str) -> None:
    """Copy the original file once into an 'originals/' folder next to it."""
    try:
        folder = os.path.dirname(image_path)
        name = os.path.basename(image_path)
        originals = os.path.join(folder, 'originals')
        os.makedirs(originals, exist_ok=True)
        backup_path = os.path.join(originals, name)
        if not os.path.exists(backup_path):
            shutil.copy2(image_path, backup_path)
    except Exception:
        # Best-effort; failures shouldn't block processing
        pass


def _parse_ratio(ratio_text: str) -> Optional[Tuple[int, int]]:
    if not ratio_text:
        return None
    if ratio_text.lower() in {"none", "keep"}:
        return None
    try:
        a, b = ratio_text.split(":", 1)
        return int(a), int(b)
    except Exception:
        return None


def crop_to_ratio(image: Image.Image, ratio_text: str) -> Image.Image:
    ratio = _parse_ratio(ratio_text)
    if not ratio:
        return image
    w, h = image.size
    target_w, target_h = ratio
    if target_w <= 0 or target_h <= 0:
        return image
    target = target_w / float(target_h)
    current = w / float(h) if h else 1.0
    if math.isclose(target, current, rel_tol=1e-3):
        return image
    if current > target:
        # too wide -> reduce width
        new_w = int(h * target)
        left = (w - new_w) // 2
        box = (max(left, 0), 0, max(left, 0) + max(new_w, 1), h)
    else:
        # too tall -> reduce height
        new_h = int(w / target) if target else h
        top = (h - new_h) // 2
        box = (0, max(top, 0), w, max(top, 0) + max(new_h, 1))
    return image.crop(box)


def add_frame(image: Image.Image, border_px: int = 0, color: str = "#ffffff", rounded: Optional[int] = None) -> Image.Image:
    border_px = int(border_px or 0)
    if border_px <= 0:
        return image
    # Simple rectangular border
    framed = ImageOps.expand(image, border=border_px, fill=color or "#ffffff")
    # Rounded corners are non-trivial; keep simple to avoid alpha issues
    return framed


def _paste_with_opacity(base: Image.Image, overlay: Image.Image, position: Tuple[int, int], opacity: float) -> Image.Image:
    if overlay.mode != "RGBA":
        overlay = overlay.convert("RGBA")
    alpha = overlay.split()[3]
    alpha = Image.eval(alpha, lambda a: int(a * (opacity)))
    overlay.putalpha(alpha)
    base.paste(overlay, position, overlay)
    return base


def apply_watermark(
    image: Image.Image,
    watermark: Image.Image,
    position: str = "bottom_right",
    opacity: float = 0.3,
    scale: float = 0.25,
    margin_px: int = 16,
) -> Image.Image:
    if not watermark:
        return image
    if image.mode != "RGBA":
        base = image.convert("RGBA")
    else:
        base = image.copy()

    W, H = base.size
    # Scale watermark relative to width
    try:
        scale = max(0.02, min(float(scale or 0.25), 1.0))
    except Exception:
        scale = 0.25
    target_w = max(1, int(W * scale))
    w_w, w_h = watermark.size
    if w_w <= 0 or w_h <= 0:
        return image
    ratio = w_h / float(w_w)
    wm = watermark.resize((target_w, max(1, int(target_w * ratio))), Image.LANCZOS)

    # Compute position
    margin = int(margin_px or 0)
    x = margin
    y = margin
    if position in ("top_left", "left_top"):
        x, y = margin, margin
    elif position in ("top_right", "right_top"):
        x, y = max(0, W - wm.size[0] - margin), margin
    elif position in ("bottom_left", "left_bottom"):
        x, y = margin, max(0, H - wm.size[1] - margin)
    elif position in ("center", "middle"):
        x, y = max(0, (W - wm.size[0]) // 2), max(0, (H - wm.size[1]) // 2)
    else:  # bottom_right
        x, y = max(0, W - wm.size[0] - margin), max(0, H - wm.size[1] - margin)

    try:
        opacity = max(0.0, min(float(opacity or 0.3), 1.0))
    except Exception:
        opacity = 0.3

    out = _paste_with_opacity(base, wm, (x, y), opacity)
    return out.convert(image.mode)


def process_image(image_path: str, options: dict) -> None:
    """Apply a sequence of edits to an image file in-place.

    Options may include: 'aspect_ratio', 'border_px', 'border_color', 'rounded',
    'watermark_file' (file-like), 'wm_position', 'wm_opacity', 'wm_scale', 'wm_margin'.
    """
    _ensure_backup(image_path)
    with Image.open(image_path) as im:
        im = im.convert("RGB")

        # Crop to aspect ratio
        aspect = options.get('aspect_ratio')
        if aspect and aspect.lower() != 'none':
            im = crop_to_ratio(im, aspect)

        # Add frame/border
        border_px = options.get('border_px') or 0
        if border_px:
            color = options.get('border_color') or '#ffffff'
            rounded = options.get('rounded') or None
            im = add_frame(im, int(border_px), str(color), int(rounded) if rounded else None)

        # Watermark
        wm_file = options.get('watermark_image')
        if wm_file:
            try:
                wm = Image.open(wm_file)
                im = apply_watermark(
                    im,
                    wm,
                    position=options.get('wm_position') or 'bottom_right',
                    opacity=float(options.get('wm_opacity') or 0.3),
                    scale=float(options.get('wm_scale') or 0.25),
                    margin_px=int(options.get('wm_margin') or 16),
                )
            except Exception:
                pass

        # Save back
        im.save(image_path, quality=90, optimize=True)


def _avg_color_in_region(image: Image.Image, box: tuple) -> tuple:
    try:
        region = image.crop(box)
        if region.mode not in ("RGB", "RGBA"):
            region = region.convert("RGB")
        # Downsize for speed, then average
        small = region.resize((1, 1), Image.BILINEAR)
        px = small.getpixel((0, 0))
        if isinstance(px, tuple):
            return px[:3]
        return (int(px), int(px), int(px))
    except Exception:
        return (0, 0, 0)


def apply_corner_triangle(
    image: Image.Image,
    corner: str = "bottom_left",
    size_ratio: float = 0.24,
    color: str | tuple | None = None,
    opacity: float = 1.0,
) -> Image.Image:
    """Draw a filled right triangle at a corner to occlude a logo.

    - corner: one of 'bottom_left', 'bottom_right', 'top_left', 'top_right'
    - size_ratio: leg length as a fraction of image width
    - color: hex string, RGB tuple, or None to auto-pick from nearby region
    - opacity: 0..1
    """
    if image.mode != "RGBA":
        base = image.convert("RGBA")
    else:
        base = image.copy()

    W, H = base.size
    if W <= 1 or H <= 1:
        return image

    try:
        r = max(0.02, min(float(size_ratio or 0.24), 0.9))
    except Exception:
        r = 0.24
    L = max(2, int(W * r))

    # Auto color from corner region if not provided
    col = color
    if col is None:
        pad = max(4, int(min(W, H) * 0.12))
        if corner == "bottom_left":
            box = (0, max(0, H - pad), min(pad, W), H)
        elif corner == "bottom_right":
            box = (max(0, W - pad), max(0, H - pad), W, H)
        elif corner == "top_left":
            box = (0, 0, min(pad, W), min(pad, H))
        else:  # top_right
            box = (max(0, W - pad), 0, W, min(pad, H))
        col = _avg_color_in_region(base, box)

    # Normalize color
    if isinstance(col, str):
        # hex like #rrggbb
        c = col.lstrip('#')
        try:
            col_t = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
        except Exception:
            col_t = (0, 0, 0)
    elif isinstance(col, tuple) and len(col) >= 3:
        col_t = tuple(int(max(0, min(255, v))) for v in col[:3])
    else:
        col_t = (0, 0, 0)

    # Build triangle points
    if corner == "bottom_left":
        pts = [(0, H), (L, H), (0, max(0, H - L))]
    elif corner == "bottom_right":
        pts = [(W, H), (max(0, W - L), H), (W, max(0, H - L))]
    elif corner == "top_left":
        pts = [(0, 0), (L, 0), (0, min(H, L))]
    else:  # top_right
        pts = [(W, 0), (max(0, W - L), 0), (W, min(H, L))]

    # Draw on a transparent overlay to control opacity
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    a = int(max(0.0, min(1.0, float(opacity or 1.0))) * 255)
    draw.polygon(pts, fill=(col_t[0], col_t[1], col_t[2], a))

    out = Image.alpha_composite(base, overlay)
    return out.convert(image.mode)


def add_corner_triangle_to_file(
    image_path: str,
    corner: str = "bottom_left",
    size_ratio: float = 0.24,
    color: str | tuple | None = None,
    opacity: float = 1.0,
) -> None:
    """Open an image, apply a corner triangle, and save back in-place."""
    _ensure_backup(image_path)
    with Image.open(image_path) as im:
        im = im.convert("RGB")
        out = apply_corner_triangle(im, corner=corner, size_ratio=size_ratio, color=color, opacity=opacity)
        out.save(image_path, quality=90, optimize=True)


def add_logo_watermark_to_file(
    image_path: str,
    logo_path: str,
    position: str = "bottom_left",
    opacity: float = 0.85,
    scale: float = 0.22,
    margin_px: int = 12,
) -> None:
    """Add a logo image as watermark to an image file in-place.

    - position: same keywords as apply_watermark
    - scale: relative to base image width (0..1)
    - margin_px: distance from edge in pixels
    """
    _ensure_backup(image_path)
    try:
        with Image.open(image_path) as im:
            im = im.convert("RGB")
            with Image.open(logo_path) as wm:
                out = apply_watermark(
                    im,
                    wm,
                    position=position,
                    opacity=float(opacity or 0.85),
                    scale=float(scale or 0.22),
                    margin_px=int(margin_px or 12),
                )
                out.save(image_path, quality=90, optimize=True)
    except Exception:
        # best effort; let caller account failures
        raise
