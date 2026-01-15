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
docker-compose up
```

The service will be available at `http://localhost:8080`.

### Manual Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Ghostscript (macOS)
brew install ghostscript

# Install Ghostscript (Ubuntu/Debian)
apt-get install ghostscript

# Run the service
uvicorn src.main:app --host 0.0.0.0 --port 8080
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Service health check |
| `/api/v1/pages/delete` | POST | Delete specified pages |
| `/api/v1/pages/insert-blank` | POST | Insert a blank page |
| `/api/v1/pages/insert-pdf` | POST | Insert pages from another PDF |
| `/api/v1/pages/extract` | POST | Extract pages to new PDF |
| `/api/v1/pages/rotate` | POST | Rotate specified pages |
| `/api/v1/redact` | POST | Apply true redactions |
| `/api/v1/compress` | POST | Compress PDF |

## API Usage

### Request Format

PDFs are sent as base64-encoded strings in JSON:

```json
{
  "pdf": "base64_encoded_pdf_data",
  "pages": [1, 3, 5],
  "password": "optional_password"
}
```

### Response Format

```json
{
  "success": true,
  "pdf": "base64_encoded_result",
  "details": {
    "deleted_pages": 3
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "INVALID_PDF",
    "message": "The provided file is not a valid PDF"
  }
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AGPL_API_KEY` | - | API key for authentication |
| `MAX_FILE_SIZE_MB` | 100 | Maximum PDF file size |
| `REQUEST_TIMEOUT_SECONDS` | 120 | Request timeout |

## Source Code

The source code for this project is available at:
https://github.com/YOUR-ORG/pdf-agpl-tools

As required by the AGPL license, if you modify this software and provide it as a network service, you must make your modified source code available to users of that service.
