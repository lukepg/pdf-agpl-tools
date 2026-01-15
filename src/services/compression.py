# SPDX-License-Identifier: AGPL-3.0-or-later
"""Compression service using Ghostscript."""

import subprocess
import tempfile
import os
from pathlib import Path


COMPRESSION_METHODS = {
    "gs-minimum": {"preset": "screen", "dpi": 36, "name": "Minimum (36 DPI)", "description": "Smallest file - very low quality"},
    "gs-screen": {"preset": "screen", "dpi": 72, "name": "Screen (72 DPI)", "description": "Low quality - good for screen viewing"},
    "gs-ebook": {"preset": "ebook", "dpi": 150, "name": "eBook (150 DPI)", "description": "Balanced quality and size"},
    "gs-printer": {"preset": "printer", "dpi": 300, "name": "Print (300 DPI)", "description": "High quality - suitable for printing"},
}


def is_ghostscript_available() -> bool:
    """Check if Ghostscript is available."""
    try:
        result = subprocess.run(
            ["gs", "--version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def compress_pdf(
    input_bytes: bytes,
    method: str,
    rasterize: bool = False,
    timeout: int = 300
) -> dict:
    """
    Compress a PDF using Ghostscript.

    Args:
        input_bytes: PDF file content as bytes
        method: Compression method (gs-minimum, gs-screen, gs-ebook, gs-printer)
        rasterize: If True, flatten pages to images
        timeout: Timeout in seconds

    Returns:
        dict with success, data (bytes), and stats
    """
    if not is_ghostscript_available():
        raise RuntimeError("Ghostscript is not installed")

    if method not in COMPRESSION_METHODS:
        raise ValueError(f"Invalid compression method: {method}")

    method_config = COMPRESSION_METHODS[method]
    original_size = len(input_bytes)

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = Path(temp_dir) / "input.pdf"
        output_path = Path(temp_dir) / "output.pdf"

        # Write input file
        input_path.write_bytes(input_bytes)

        if rasterize:
            # Rasterize pages to images
            args = [
                "gs",
                "-sDEVICE=pdfimage24",
                f"-r{method_config['dpi']}",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                f"-sOutputFile={output_path}",
                str(input_path),
            ]
        else:
            # Standard compression
            args = [
                "gs",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.4",
                f"-dPDFSETTINGS=/{method_config['preset']}",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                "-dColorImageDownsampleType=/Bicubic",
                "-dGrayImageDownsampleType=/Bicubic",
                "-dMonoImageDownsampleType=/Bicubic",
            ]

            # For minimum, override DPI
            if method == "gs-minimum":
                args.extend([
                    "-dColorImageResolution=36",
                    "-dGrayImageResolution=36",
                    "-dMonoImageResolution=36",
                    "-dDownsampleColorImages=true",
                    "-dDownsampleGrayImages=true",
                    "-dDownsampleMonoImages=true",
                ])

            args.extend([f"-sOutputFile={output_path}", str(input_path)])

        # Run Ghostscript
        result = subprocess.run(
            args,
            capture_output=True,
            timeout=timeout
        )

        if result.returncode != 0:
            stderr = result.stderr.decode("utf-8", errors="replace")
            raise RuntimeError(f"Ghostscript failed: {stderr}")

        if not output_path.exists():
            raise RuntimeError("Compression output file was not created")

        # Read output
        output_bytes = output_path.read_bytes()
        compressed_size = len(output_bytes)

        compression_ratio = (
            ((original_size - compressed_size) / original_size) * 100
            if original_size > 0
            else 0
        )

        return {
            "success": True,
            "data": output_bytes,
            "stats": {
                "original_size": original_size,
                "compressed_size": compressed_size,
                "compression_ratio": round(compression_ratio, 2),
                "saved_bytes": original_size - compressed_size,
            }
        }


def get_compression_methods() -> list[dict]:
    """Get list of available compression methods."""
    return [
        {
            "method": method,
            "name": config["name"],
            "description": config["description"],
            "dpi": config["dpi"],
        }
        for method, config in COMPRESSION_METHODS.items()
    ]
