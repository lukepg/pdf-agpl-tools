# SPDX-License-Identifier: AGPL-3.0-or-later
"""Configuration management for pdf-agpl-tools."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API authentication
    api_key: str = ""

    # File size limits
    max_file_size_mb: int = 100

    # Timeouts
    request_timeout_seconds: int = 120
    compression_timeout_seconds: int = 300

    # Service info
    service_name: str = "pdf-agpl-tools"
    version: str = "1.0.0"
    source_code_url: str = "https://github.com/lukepg/pdf-agpl-tools"

    class Config:
        env_prefix = "AGPL_"


settings = Settings()
