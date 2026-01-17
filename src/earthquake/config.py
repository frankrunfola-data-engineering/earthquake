# src/earthquake/config.py
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    base_url: str
    output_dir: Path
    lookback_days: int
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "PipelineConfig":
        base_url = os.getenv("API_BASE_URL", "https://earthquake.usgs.gov/fdsnws/event/1/query")
        output_dir = Path(os.getenv("OUTPUT_DIR", "data"))
        lookback_days = int(os.getenv("LOOKBACK_DAYS", "1"))
        log_level = os.getenv("LOG_LEVEL", "INFO")
        return cls(
            base_url=base_url,
            output_dir=output_dir,
            lookback_days=lookback_days,
            log_level=log_level,
        )
