"""utilities for the test framework."""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_config(config_path: str | None = None) -> dict:
    """Load configuration from settings.json."""
    resolved: str | Path = (
        config_path
        if config_path is not None
        else Path(__file__).parent.parent.parent.parent / "config" / "settings.json"
    )
    logger.info(f"Loading configuration from {resolved}")
    with open(resolved) as f:
        return json.load(f)


def get_credentials(config: dict, user_type: str) -> tuple:
    """Return (username, password) tuple for the given user type."""
    logger.debug(f"Retrieving credentials for user type '{user_type}'")
    creds = config["credentials"][user_type]
    return creds["username"], creds["password"]
