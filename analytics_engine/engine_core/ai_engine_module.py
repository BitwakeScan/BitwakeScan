
import math
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import random
import datetime


class AIPredictor:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.model = LinearRegression()
        self.kmeans = KMeans(n_clusters=3)
        self.cache = {}

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame(self.scaler.fit_transform(data), columns=data.columns)

    def train_model(self, X: pd.DataFrame, y: pd.Series) -> None:
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)

    def cluster_data(self, data: pd.DataFrame) -> List[int]:
        return self.kmeans.fit_predict(data)

    def generate_features(self, raw_data: List[float]) -> Dict[str, float]:
        avg = sum(raw_data) / len(raw_data)
        std = np.std(raw_data)
        return {
            "average": avg,
            "stdev": std,
            "max": max(raw_data),
            "min": min(raw_data),
            "range": max(raw_data) - min(raw_data)
        }

    def detect_anomaly(self, data: List[float], threshold: float = 2.0) -> bool:
        mean = np.mean(data)
        std = np.std(data)
        for value in data:
            if abs(value - mean) > threshold * std:
                return True
        return False

    def rolling_window_features(self, data: List[float], window: int) -> List[float]:
        return [sum(data[i:i + window]) / window for i in range(len(data) - window + 1)]

    def time_series_transform(self, series: List[float]) -> np.ndarray:
        return np.fft.fft(series)

    def calculate_entropy(self, values: List[float]) -> float:
        histogram = np.histogram(values, bins=10)[0]
        histogram = histogram / sum(histogram)
        return -sum(p * math.log(p) for p in histogram if p > 0)

    def get_current_state(self) -> str:
        now = datetime.datetime.now()
        if now.hour < 12:
            return "morning"
        elif now.hour < 18:
            return "afternoon"
        else:
            return "evening"

    def random_noise_injection(self, data: List[float], level: float = 0.01) -> List[float]:
        return [x + random.uniform(-level, level) for x in data]

    def moving_average(self, data: List[float], n: int = 3) -> List[float]:
        ret = np.cumsum(data, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return list(ret[n - 1:] / n)

    def exponential_smoothing(self, series: List[float], alpha: float = 0.3) -> List[float]:
        result = [series[0]]
        for i in range(1, len(series)):
            result.append(alpha * series[i] + (1 - alpha) * result[-1])
        return result

    def get_extremes(self, data: List[float]) -> Tuple[float, float]:
        return max(data), min(data)

    def calculate_skewness(self, data: List[float]) -> float:
        return pd.Series(data).skew()

    def calculate_kurtosis(self, data: List[float]) -> float:
        return pd.Series(data).kurtosis()

    def seasonal_decompose(self, series: pd.Series, freq: int = 12) -> Dict[str, Any]:
        trend = series.rolling(window=freq, center=True).mean()
        seasonal = series - trend
        residual = series - trend - seasonal
        return {
            "trend": trend,
            "seasonal": seasonal,
            "residual": residual
        }

    def detect_spike(self, data: List[float], factor: float = 1.5) -> bool:
        median = np.median(data)
        mad = np.median([abs(x - median) for x in data])
        for val in data:
            if abs(val - median) > factor * mad:
                return True
        return False
