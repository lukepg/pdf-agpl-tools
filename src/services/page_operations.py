# SPDX-License-Identifier: AGPL-3.0-or-later
"""Page operations service using PyMuPDF."""

import fitz  # PyMuPDF


def delete_pages(doc: fitz.Document, pages: list[int], password: str = None) -> dict:
    """
    Delete specified pages from a PDF document.

    Args:
        doc: PyMuPDF document object
        pages: List of 1-indexed page numbers to delete
        password: Optional password for encrypted PDFs

    Returns:
        dict with operation details
    """
    if password and doc.is_encrypted:
        if not doc.authenticate(password):
            raise ValueError("Invalid password for encrypted PDF")

    page_count = len(doc)

    # Convert to 0-indexed and validate
    indices_to_delete = sorted(
        [p - 1 for p in pages if 0 <= p - 1 < page_count],
        reverse=True  # Delete from end to preserve indices
    )

    if not indices_to_delete:
        raise ValueError("No valid pages to delete")

    if len(indices_to_delete) >= page_count:
        raise ValueError("Cannot delete all pages from document")

    # Delete pages from end to start
    for idx in indices_to_delete:
        doc.delete_page(idx)

    return {
        "deleted_pages": len(indices_to_delete),
        "remaining_pages": page_count - len(indices_to_delete)
    }


def insert_blank_page(
    doc: fitz.Document,
    position: str,
    reference_page: int,
    width: float = None,
    height: float = None,
    password: str = None
) -> dict:
    """
    Insert a blank page before or after a reference page.

    Args:
        doc: PyMuPDF document object
        position: "before" or "after"
        reference_page: 1-indexed page number
        width: Optional page width (defaults to reference page)
        height: Optional page height (defaults to reference page)
        password: Optional password for encrypted PDFs

    Returns:
        dict with operation details
    """
    if password and doc.is_encrypted:
        if not doc.authenticate(password):
            raise ValueError("Invalid password for encrypted PDF")

    page_count = len(doc)

    # Validate reference page
    ref_idx = reference_page - 1
    if ref_idx < 0 or ref_idx >= page_count:
        raise ValueError(f"Invalid reference page: {reference_page}")

    # Get page size from reference if not specified
    if width is None or height is None:
        ref_page = doc[ref_idx]
        rect = ref_page.rect
        width = width or rect.width
        height = height or rect.height

    # Calculate insert position
    insert_idx = ref_idx if position == "before" else ref_idx + 1

    # Insert blank page
    doc.new_page(pno=insert_idx, width=width, height=height)

    return {
        "new_page_count": page_count + 1,
        "inserted_at": insert_idx + 1
    }


def insert_pdf_pages(
    doc: fitz.Document,
    source_doc: fitz.Document,
    position: str,
    reference_page: int,
    pages_to_insert: list[int] = None,
    password: str = None,
    source_password: str = None
) -> dict:
    """
    Insert pages from another PDF.

    Args:
        doc: Target PyMuPDF document
        source_doc: Source PyMuPDF document
        position: "before" or "after"
        reference_page: 1-indexed page number in target
        pages_to_insert: Optional list of 1-indexed pages from source (defaults to all)
        password: Optional password for target PDF
        source_password: Optional password for source PDF

    Returns:
        dict with operation details
    """
    if password and doc.is_encrypted:
        if not doc.authenticate(password):
            raise ValueError("Invalid password for encrypted PDF")

    if source_password and source_doc.is_encrypted:
        if not source_doc.authenticate(source_password):
            raise ValueError("Invalid password for source PDF")

    target_page_count = len(doc)
    source_page_count = len(source_doc)

    # Validate reference page
    ref_idx = reference_page - 1
    if ref_idx < 0 or ref_idx >= target_page_count:
        raise ValueError(f"Invalid reference page: {reference_page}")

    # Determine which pages to insert
    if pages_to_insert:
        source_indices = [p - 1 for p in pages_to_insert if 0 <= p - 1 < source_page_count]
    else:
        source_indices = list(range(source_page_count))

    if not source_indices:
        raise ValueError("No valid pages to insert from source PDF")

    # Calculate insert position
    insert_idx = ref_idx if position == "before" else ref_idx + 1

    # Insert pages from source
    doc.insert_pdf(
        source_doc,
        from_page=min(source_indices),
        to_page=max(source_indices),
        start_at=insert_idx
    )

    return {
        "new_page_count": target_page_count + len(source_indices),
        "inserted_pages": len(source_indices)
    }


def extract_pages(doc: fitz.Document, pages: list[int], password: str = None) -> dict:
    """
    Extract (keep) only specified pages from a PDF.

    Args:
        doc: PyMuPDF document object
        pages: List of 1-indexed page numbers to keep
        password: Optional password for encrypted PDFs

    Returns:
        dict with operation details
    """
    if doc.is_encrypted:
        if password:
            if not doc.authenticate(password):
                raise ValueError("Invalid password for encrypted PDF")
        else:
            # Try empty password
            if not doc.authenticate(""):
                raise ValueError("PDF is encrypted and requires a password")

    page_count = len(doc)

    # Convert to 0-indexed and validate, maintaining original order
    indices_to_keep = [p - 1 for p in pages if 0 <= p - 1 < page_count]

    # Remove duplicates while preserving order
    seen = set()
    unique_indices = []
    for idx in indices_to_keep:
        if idx not in seen:
            seen.add(idx)
            unique_indices.append(idx)
    indices_to_keep = unique_indices

    if not indices_to_keep:
        raise ValueError("No valid pages to extract")

    # Create list of pages to delete
    all_indices = set(range(page_count))
    indices_to_delete = sorted(all_indices - set(indices_to_keep), reverse=True)

    # Delete pages from end to start
    for idx in indices_to_delete:
        doc.delete_page(idx)

    return {
        "extracted_pages": len(indices_to_keep),
        "original_pages": page_count
    }


def rotate_pages(
    doc: fitz.Document,
    pages: list[int],
    rotation: int,
    password: str = None
) -> dict:
    """
    Rotate specified pages by the given angle.

    Args:
        doc: PyMuPDF document object
        pages: List of 1-indexed page numbers to rotate
        rotation: Rotation angle (90, 180, or 270)
        password: Optional password for encrypted PDFs

    Returns:
        dict with operation details
    """
    if rotation not in [90, 180, 270]:
        raise ValueError(f"Invalid rotation angle: {rotation}. Must be 90, 180, or 270.")

    if password and doc.is_encrypted:
        if not doc.authenticate(password):
            raise ValueError("Invalid password for encrypted PDF")

    page_count = len(doc)

    # Convert to 0-indexed and validate
    indices_to_rotate = [p - 1 for p in pages if 0 <= p - 1 < page_count]

    if not indices_to_rotate:
        raise ValueError("No valid pages to rotate")

    # Rotate each specified page
    for idx in indices_to_rotate:
        page = doc[idx]
        current_rotation = page.rotation
        new_rotation = (current_rotation + rotation) % 360
        page.set_rotation(new_rotation)

    return {
        "rotated_pages": len(indices_to_rotate),
        "rotation": rotation
    }
