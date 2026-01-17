# src/earthquake/app.py
from __future__ import annotations

import os

from dotenv import load_dotenv

from .config import PipelineConfig
from .logging_utils import configure_logging
from .pipeline import run_pipeline


def main(argv: list[str] | None = None) -> int:
    """
    No CLI parsing. No overrides.
    Everything comes from env/.env via PipelineConfig.from_env().
    """
    load_dotenv(override=False)

    cfg = PipelineConfig.from_env()

    # Logging: prefer config.log_level if you have it, else LOG_LEVEL env, else INFO.
    log_level = getattr(cfg, "log_level", None) or os.getenv("LOG_LEVEL", "INFO")
    logger = configure_logging(log_level)

    result = run_pipeline(config=cfg)

    logger.info("Run date: %s", result.run_date.isoformat())
    logger.info("Bronze records: %s", result.records_bronze)
    logger.info("Silver records: %s", result.records_silver)
    logger.info("Gold records: %s", result.records_gold)

    return 0
