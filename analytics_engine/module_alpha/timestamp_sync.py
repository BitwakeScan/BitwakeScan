import logging
import os
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Create logs directory
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Log file path
LOG_FILE = log_dir / "stillbit_monitor.log"

# Logger setup
logger = logging.getLogger("stillbit")
logger.setLevel(os.getenv("STILLBIT_LOG_LEVEL", "DEBUG"))

# Rotating handler
handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5, encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(message)s"))
logger.addHandler(handler)

# Optional console output
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(message)s"))
logger.addHandler(console)

def log_asset_status(asset_id: str, status: str, level: str = "info") -> None:
    """
    Log asset status with timestamp in message and proper level.
    Level can be 'debug', 'info', 'warning', 'error', or 'critical'.
    """
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg = f"[{ts}] Asset {asset_id}: {status}"
    lvl = level.lower()
    if lvl == "debug":
        logger.debug(msg)
    elif lvl == "info":
        logger.info(msg)
    elif lvl == "warning":
        logger.warning(msg)
    elif lvl == "error":
        logger.error(msg)
    elif lvl == "critical":
        logger.critical(msg)
    else:
        logger.info(msg)

if __name__ == "__main__":
    log_asset_status("0xabc123", "Asset stability confirmed", level="info")
    log_asset_status("0xdef456", "Asset health below threshold", level="warning")
    log_asset_status("0xghi789", "Asset unreachable", level="error")
