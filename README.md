# pdf-agpl-tools

A standalone microservice providing PDF manipulation operations using PyMuPDF and Ghostscript.

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See the [LICENSE](LICENSE) file for the full license text, or visit:
https://www.gnu.org/licenses/agpl-3.0.en.html

### AGPL Dependencies

This project uses the following AGPL-licensed libraries:
- **PyMuPDF (fitz)** - PDF manipulation library
- **Ghostscript** - PDF compression and rasterization

## Features

- **Page Operations**: Delete, insert, extract, rotate PDF pages
- **Redaction**: True content removal (not just visual overlay)
- **Compression**: Multiple quality presets using Ghostscript

## Quick Start

### Using Docker (Recommended)

```bash
# Using Docker Compose
docker-compose up

# Or pull from GitHub Container Registry
docker run -d -p 8080:8080 -e AGPL_API_KEY=your-key ghcr.io/lukepg/pdf-agpl-tools:latest
```

The service will be available at `http://localhost:8080`.

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/lukepg/pdf-agpl-tools.git
cd pdf-agpl-tools

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Ghostscript (macOS)
brew install ghostscript

# Install Ghostscript (Ubuntu/Debian)
apt-get install ghostscript

# Run the service
uvicorn src.main:app --host 0.0.0.0 --port 8080
```

### Verify Installation

```bash
curl http://localhost:8080/api/v1/health
```

## API Reference

### Authentication

If `AGPL_API_KEY` is configured, include it in requests:

```
X-API-Key: your-api-key
```

### Health Check

```
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "pymupdf": { "available": true, "version": "1.23.0" },
    "ghostscript": { "available": true, "version": "10.02.1" }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### Page Operations

#### Delete Pages

Remove specified pages from a PDF.

```
POST /api/v1/pages/delete
```

**Request:**
```json
{
  "pdf": "base64_encoded_pdf",
  "pages": [1, 3, 5],
  "password": "optional"
}
```

**Response:**
```json
{
  "success": true,
  "pdf": "base64_encoded_result",
  "details": {
    "deleted_pages": 3,
    "remaining_pages": 7
  }
}
```

---

#### Insert Blank Page

Insert a blank page before or after a reference page.

```
POST /api/v1/pages/insert-blank
```

**Request:**
```json
{
  "pdf": "base64_encoded_pdf",
  "position": "after",
  "reference_page": 2,
  "width": 612,
  "height": 792,
  "password": "optional"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pdf` | string | Yes | Base64-encoded PDF |
| `position` | string | Yes | `"before"` or `"after"` |
| `reference_page` | integer | Yes | 1-indexed page number |
| `width` | number | No | Page width (defaults to reference page) |
| `height` | number | No | Page height (defaults to reference page) |
| `password` | string | No | PDF password if encrypted |

**Response:**
```json
{
  "success": true,
  "pdf": "base64_encoded_result",
  "details": {
    "new_page_count": 11,
    "inserted_at": 3
  }
}
```

---

#### Insert PDF Pages

Insert pages from another PDF.

```
POST /api/v1/pages/insert-pdf
```

**Request:**
```json
{
  "target_pdf": "base64_encoded_target",
  "source_pdf": "base64_encoded_source",
  "position": "after",
  "reference_page": 2,
  "pages_to_insert": [1, 2, 3],
  "target_password": "optional",
  "source_password": "optional"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `target_pdf` | string | Yes | Base64-encoded target PDF |
| `source_pdf` | string | Yes | Base64-encoded source PDF |
| `position` | string | Yes | `"before"` or `"after"` |
| `reference_page` | integer | Yes | 1-indexed page in target |
| `pages_to_insert` | array | No | 1-indexed pages from source (defaults to all) |

**Response:**
```json
{
  "success": true,
  "pdf": "base64_encoded_result",
  "details": {
    "new_page_count": 13,
    "inserted_pages": 3
  }
}
```

---

#### Extract Pages

Extract (keep only) specified pages.

```
POST /api/v1/pages/extract
```

**Request:**
```json
{
  "pdf": "base64_encoded_pdf",
  "pages": [1, 3, 5],
  "password": "optional"
}
```

**Response:**
```json
{
  "success": true,
  "pdf": "base64_encoded_result",
  "details": {
    "extracted_pages": 3,
    "original_pages": 10
  }
}
```

---

#### Rotate Pages

Rotate specified pages.

```
POST /api/v1/pages/rotate
```

**Request:**
```json
{
  "pdf": "base64_encoded_pdf",
  "pages": [1, 2],
  "rotation": 90,
  "password": "optional"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pdf` | string | Yes | Base64-encoded PDF |
| `pages` | array | Yes | 1-indexed page numbers |
| `rotation` | integer | Yes | `90`, `180`, or `270` degrees |
| `password` | string | No | PDF password if encrypted |

**Response:**
```json
{
  "success": true,
  "pdf": "base64_encoded_result",
  "details": {
    "rotated_pages": 2,
    "rotation": 90
  }
}
```

---

### Redaction

Apply true redactions (removes content from PDF streams, not just visual overlay).

```
POST /api/v1/redact
```

**Request:**
```json
{
  "pdf": "base64_encoded_pdf",
  "redactions": [
    {
      "page": 1,
      "x": 100,
      "y": 200,
      "width": 150,
      "height": 20,
      "fill": "#000000"
    }
  ],
  "replacement_texts": [
    {
      "page": 1,
      "x": 100,
      "y": 200,
      "text": "REDACTED",
      "fontsize": 12,
      "color": "#FFFFFF"
    }
  ],
  "password": "optional"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `redactions[].page` | integer | Yes | 1-indexed page number |
| `redactions[].x` | number | Yes | X coordinate |
| `redactions[].y` | number | Yes | Y coordinate |
| `redactions[].width` | number | Yes | Redaction width |
| `redactions[].height` | number | Yes | Redaction height |
| `redactions[].fill` | string | No | Fill color (default: `#FFFFFF`) |
| `replacement_texts` | array | No | Text to insert after redaction |

**Response:**
```json
{
  "success": true,
  "pdf": "base64_encoded_result"
}
```

---

### Compression

Compress PDF using Ghostscript.

```
POST /api/v1/compress
```

**Request:**
```json
{
  "pdf": "base64_encoded_pdf",
  "method": "gs-ebook",
  "rasterize": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pdf` | string | Yes | Base64-encoded PDF |
| `method` | string | Yes | Compression method (see below) |
| `rasterize` | boolean | No | Flatten pages to images (default: false) |

**Compression Methods:**

| Method | DPI | Description |
|--------|-----|-------------|
| `gs-minimum` | 36 | Smallest file, very low quality |
| `gs-screen` | 72 | Low quality, good for screen viewing |
| `gs-ebook` | 150 | Balanced quality and size |
| `gs-printer` | 300 | High quality, suitable for printing |

**Response:**
```json
{
  "success": true,
  "pdf": "base64_encoded_result",
  "stats": {
    "original_size": 1048576,
    "compressed_size": 524288,
    "compression_ratio": 50.0,
    "saved_bytes": 524288
  }
}
```

#### Get Compression Methods

```
GET /api/v1/compress/methods
```

**Response:**
```json
{
  "methods": [
    { "method": "gs-minimum", "name": "Minimum (36 DPI)", "description": "...", "dpi": 36 },
    { "method": "gs-screen", "name": "Screen (72 DPI)", "description": "...", "dpi": 72 },
    { "method": "gs-ebook", "name": "eBook (150 DPI)", "description": "...", "dpi": 150 },
    { "method": "gs-printer", "name": "Print (300 DPI)", "description": "...", "dpi": 300 }
  ]
}
```

---

## Error Handling

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description"
  }
}
```

| Error Code | Description |
|------------|-------------|
| `INVALID_PDF` | Not a valid PDF file |
| `ENCRYPTED_PDF` | PDF requires password |
| `INVALID_PASSWORD` | Provided password is incorrect |
| `INVALID_PAGES` | Page numbers out of range |
| `INVALID_INPUT` | Request validation failed |
| `PROCESSING_FAILED` | Internal processing error |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AGPL_API_KEY` | - | API key for authentication (optional) |
| `AGPL_MAX_FILE_SIZE_MB` | 100 | Maximum PDF file size |
| `AGPL_REQUEST_TIMEOUT_SECONDS` | 120 | Request timeout |
| `AGPL_COMPRESSION_TIMEOUT_SECONDS` | 300 | Compression timeout |
| `AGPL_SOURCE_CODE_URL` | GitHub URL | Source code URL for AGPL compliance |

---

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Building Docker Image

```bash
docker build -t pdf-agpl-tools .
```

---

## Source Code

The source code for this project is available at:
https://github.com/lukepg/pdf-agpl-tools

As required by the AGPL license, if you modify this software and provide it as a network service, you must make your modified source code available to users of that service.

All API responses include an `X-Source-Code` header pointing to this repository.
