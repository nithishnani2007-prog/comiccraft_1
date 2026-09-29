"""
layout_builder.py

Combines each panel's generated image with its story text into a
single structured layout ready for the preview page and PDF export.
"""

import re


def format_story_lines(value):
    """Normalize story text into a readable three-line block."""
    if value is None:
        return ""

    text = str(value).replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return ""

    segments = [segment.strip() for segment in re.split(r"\n+|(?<=[.!?])\s+", text) if segment.strip()]
    if not segments:
        return ""

    if len(segments) == 1:
        words = text.split()
        if len(words) <= 3:
            return text
        parts = [" ".join(words[i:i+max(1, len(words)//3)]) for i in range(0, len(words), max(1, len(words)//3))]
        segments = [part.strip() for part in parts if part.strip()][:3]

    while len(segments) < 3:
        segments.append("")

    return "\n".join(segments[:3])


def build_comic_layout(panels):
    layout = []
    for panel in panels:
        layout.append(
            {
                "panel_number": panel.get("panel_number"),
                "title": panel.get("title", ""),
                "image_path": panel.get("image_path", ""),
                "image_error": panel.get("image_error", ""),
                "scene_description": panel.get("scene_description", ""),
                "caption": format_story_lines(panel.get("caption", "")),
                "narration": format_story_lines(panel.get("narration", "")),
                "image_prompt": panel.get("image_prompt", ""),
            }
        )
    layout.sort(key=lambda p: p["panel_number"] if p["panel_number"] is not None else 0)
    return layout
