"""Technical analysis module for stock analysis."""

import logging
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from dataclasses import dataclass

@dataclass
class TechnicalIndicators:
    """Class to hold technical indicator values."""
    rsi: Optional[float] = None
    macd: Optional[Dict[str, float]] = None
    bollinger_bands: Optional[Dict[str, float]] = None

class TechnicalAnalyzer:
    """Class for technical analysis of stock data."""
    
    def __init__(self):
        """Initialize technical analyzer."""
        self.logger = logging.getLogger(__name__)
        self.data = None
    
    def set_data(self, data: pd.DataFrame) -> None:
        """Set the data for analysis."""
        self.data = data
    
    def calculate_rsi(self, period: int = 14) -> float:
        """
        Calculate Relative Strength Index (RSI).
        
        Args:
            period: Period for RSI calculation
            
        Returns:
            RSI value
        """
        if self.data is None or len(self.data) < period:
            return None
            
        try:
            # Calculate price changes
            delta = self.data['CLOSE'].diff()
            
            # Separate gains and losses
            gains = delta.where(delta > 0, 0)
            losses = -delta.where(delta < 0, 0)
            
            # Calculate average gains and losses
            avg_gains = gains.rolling(window=period).mean()
            avg_losses = losses.rolling(window=period).mean()
            
            # Calculate RS and RSI
            rs = avg_gains / avg_losses
            rsi = 100 - (100 / (1 + rs))
            
            return float(rsi.iloc[-1])
            
        except Exception as e:
            self.logger.error(f"Error calculating RSI: {str(e)}")
            return None
    
    def calculate_macd(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Dict[str, float]:
        """
        Calculate Moving Average Convergence Divergence (MACD).
        
        Args:
            fast_period: Fast EMA period
            slow_period: Slow EMA period
            signal_period: Signal line period
            
        Returns:
            Dict containing MACD line, signal line, and histogram values
        """
        if self.data is None or len(self.data) < slow_period:
            return None
            
        try:
            # Calculate EMAs
            fast_ema = self.data['CLOSE'].ewm(span=fast_period, adjust=False).mean()
            slow_ema = self.data['CLOSE'].ewm(span=slow_period, adjust=False).mean()
            
            # Calculate MACD line and signal line
            macd_line = fast_ema - slow_ema
            signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
            
            # Calculate histogram
            histogram = macd_line - signal_line
            
            return {
                'macd_line': float(macd_line.iloc[-1]),
                'signal_line': float(signal_line.iloc[-1]),
                'histogram': float(histogram.iloc[-1])
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating MACD: {str(e)}")
            return None
    
    def calculate_bollinger_bands(self, period: int = 20, num_std: float = 2.0) -> Dict[str, float]:
        """
        Calculate Bollinger Bands.
        
        Args:
            period: Period for moving average
            num_std: Number of standard deviations
            
        Returns:
            Dict containing upper band, middle band, and lower band values
        """
        if self.data is None or len(self.data) < period:
            return None
            
        try:
            # Calculate middle band (SMA)
            middle_band = self.data['CLOSE'].rolling(window=period).mean()
            
            # Calculate standard deviation
            std = self.data['CLOSE'].rolling(window=period).std()
            
            # Calculate upper and lower bands
            upper_band = middle_band + (std * num_std)
            lower_band = middle_band - (std * num_std)
            
            return {
                'upper_band': float(upper_band.iloc[-1]),
                'middle_band': float(middle_band.iloc[-1]),
                'lower_band': float(lower_band.iloc[-1])
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating Bollinger Bands: {str(e)}")
            return None
    
    def analyze(self, indicators: List[str]) -> TechnicalIndicators:
        """
        Perform technical analysis for specified indicators.
        
        Args:
            indicators: List of indicators to calculate
            
        Returns:
            Dict containing calculated indicators
        """
        if self.data is None:
            return TechnicalIndicators()
            
        results = TechnicalIndicators()
        
        if 'RSI' in indicators:
            results.rsi = self.calculate_rsi()
            
        if 'MACD' in indicators:
            results.macd = self.calculate_macd()
            
        if 'BB' in indicators:
            results.bollinger_bands = self.calculate_bollinger_bands()
            
        return results
