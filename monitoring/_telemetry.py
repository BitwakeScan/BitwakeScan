import logging
from datetime import datetime
from collections import deque
from statistics import mean, stdev
from typing import List, Optional, Any

logger = logging.getLogger("stream_watch")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger.addHandler(handler)


def advanced_log_event(event_type: str, data: Any) -> None:
    """Log events with ISO timestamp and structured message."""
    timestamp = datetime.utcnow().isoformat()
    logger.info(f"[{event_type}] - {data} - at {timestamp}")


def detect_anomalous_patterns(
    data_series: List[float], multiplier: float = 1.5
) -> Optional[List[float]]:
    """
    Identify values exceeding mean * multiplier.
    Returns list of outliers or None if none found.
    """
    if not data_series:
        return None
    μ = mean(data_series)
    threshold = μ * multiplier
    outliers = [v for v in data_series if v > threshold]
    return outliers or None


class StreamWatch:
    """
    Maintains a sliding window of recent events and checks for anomalies.
    """

    def __init__(self, maxlen: int = 100):
        self.events: deque[float] = deque(maxlen=maxlen)

    def add_event(self, value: float) -> None:
        """Add a new event value to the buffer."""
        self.events.append(value)
        advanced_log_event("EVENT_ADDED", value)

    def check_for_anomalies(self) -> str:
        """
        Check the current buffer for anomalies.
        Returns a status string and logs details if anomalies found.
        """
        if not self.events:
            return "No Data"

        # use standard deviation to refine detection if enough data
        ds = list(self.events)
        outliers = detect_anomalous_patterns(ds)
        if outliers:
            logger.warning(f"Anomalies detected: {outliers}")
            return "⚠️ Anomaly Detected"
        else:
            return "✅ Stable"

    def get_statistics(self) -> dict:
        """Return basic stats about current window."""
        ds = list(self.events)
        if not ds:
            return {}
        stats
