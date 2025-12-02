from __future__ import annotations

from django import forms


ASPECT_CHOICES = (
    ("none", "No crop (keep)"),
    ("1:1", "1:1 (square)"),
    ("4:3", "4:3"),
    ("3:2", "3:2"),
    ("16:9", "16:9"),
)

POSITION_CHOICES = (
    ("bottom_right", "Bottom right"),
    ("bottom_left", "Bottom left"),
    ("top_right", "Top right"),
    ("top_left", "Top left"),
    ("center", "Center"),
)


class BulkImageEditForm(forms.Form):
    # Crop
    aspect_ratio = forms.ChoiceField(choices=ASPECT_CHOICES, required=False, initial="none")

    # Frame
    border_px = forms.IntegerField(min_value=0, required=False, initial=0)
    border_color = forms.CharField(required=False, initial="#ffffff")
    rounded = forms.IntegerField(min_value=0, required=False)

    # Watermark
    watermark_image = forms.ImageField(required=False)
    wm_position = forms.ChoiceField(choices=POSITION_CHOICES, required=False, initial="bottom_right")
    wm_opacity = forms.FloatField(min_value=0, max_value=1, required=False, initial=0.3)
    wm_scale = forms.FloatField(min_value=0.02, max_value=1.0, required=False, initial=0.25)
    wm_margin = forms.IntegerField(min_value=0, required=False, initial=16)

    # Safety
    confirm = forms.BooleanField(required=True, help_text="Confirm applying edits to selected images")


class LogoWatermarkForm(forms.Form):
    wm_position = forms.ChoiceField(choices=POSITION_CHOICES, required=False, initial="bottom_left")
    wm_opacity = forms.FloatField(min_value=0, max_value=1, required=False, initial=0.85)
    wm_scale = forms.FloatField(min_value=0.02, max_value=1.0, required=False, initial=0.22)
    wm_margin = forms.IntegerField(min_value=0, required=False, initial=12)
    confirm = forms.BooleanField(required=False, help_text="Optional safety checkbox before applying the logo watermark")
