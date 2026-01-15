# SPDX-License-Identifier: AGPL-3.0-or-later
"""Redaction service using PyMuPDF."""

from typing import Union
import fitz  # PyMuPDF


def hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    """Convert hex color string to RGB tuple (0-1 range)."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255
        return (r, g, b)
    return (1.0, 1.0, 1.0)  # Default white


def normalize_color(color: Union[str, list[float], None]) -> tuple[float, float, float]:
    """Normalize color to RGB tuple."""
    if color is None:
        return (1.0, 1.0, 1.0)  # Default white
    if isinstance(color, str):
        return hex_to_rgb(color)
    if isinstance(color, list) and len(color) >= 3:
        return (float(color[0]), float(color[1]), float(color[2]))
    return (1.0, 1.0, 1.0)


def apply_redactions(
    doc: fitz.Document,
    redactions: list[dict],
    replacement_texts: list[dict] = None,
    password: str = None
) -> bool:
    """
    Apply redactions to a PDF document.

    Args:
        doc: PyMuPDF document object
        redactions: List of redaction areas with page, x, y, width, height, fill
        replacement_texts: Optional list of replacement texts
        password: Optional password for encrypted PDFs

    Returns:
        True if successful
    """
    if password and doc.is_encrypted:
        if not doc.authenticate(password):
            raise ValueError("Invalid password for encrypted PDF")

    if len(doc) == 0:
        raise ValueError("PDF has no pages")

    # Group redactions by page
    redactions_by_page: dict[int, list[dict]] = {}
    for r in redactions:
        page_num = r['page'] - 1  # Convert to 0-indexed
        if page_num not in redactions_by_page:
            redactions_by_page[page_num] = []
        redactions_by_page[page_num].append(r)

    # Apply redactions page by page
    for page_num, page_redactions in redactions_by_page.items():
        if page_num < 0 or page_num >= len(doc):
            continue

        page = doc[page_num]

        # Add redaction annotations
        for r in page_redactions:
            x = r['x']
            y = r['y']
            width = r['width']
            height = r['height']

            rect = fitz.Rect(x, y, x + width, y + height)
            fill = normalize_color(r.get('fill'))

            page.add_redact_annot(rect, fill=fill)

        # Apply all redactions on this page
        page.apply_redactions()

    # Add replacement texts if provided
    if replacement_texts:
        for t in replacement_texts:
            page_num = t['page'] - 1
            if page_num < 0 or page_num >= len(doc):
                continue

            page = doc[page_num]

            x = t['x']
            y = t['y'] + t.get('fontsize', 12)  # Adjust for baseline

            color = normalize_color(t.get('color'))
            fontsize = t.get('fontsize', 12)

            page.insert_text(
                (x, y),
                t['text'],
                fontsize=fontsize,
                color=color,
            )

    return True
