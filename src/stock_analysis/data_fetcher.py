"""
Data fetching module for stock analysis
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import random
import pandas as pd
import numpy as np

class DataFetcher:
    """Class to fetch stock data from various sources."""
    
    def __init__(self):
        """Initialize the data fetcher."""
        self.logger = logging.getLogger(__name__)
    
    def get_market_status(self) -> str:
        """Get current market status."""
        # Mock implementation
        current_hour = datetime.now().hour
        if 9 <= current_hour < 16:
            return "Open"
        return "Closed"
    
    def get_current_data(self, symbol: str) -> Dict[str, Any]:
        """Get current market data for a stock."""
        # Mock implementation
        return {
            'last_price': None,
            'change': None,
            'volume': 1_000_000,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_historical_data(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """Get historical data for a stock."""
        # Mock implementation
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=365)
        
        # Generate dates
        dates = pd.date_range(start=start_date, end=end_date, freq='B')
        
        # Generate mock price data
        np.random.seed(hash(symbol) % 2**32)  # Use symbol as seed for consistency
        
        base_price = 1000 + np.random.rand() * 2000  # Random base price between 1000 and 3000
        prices = np.random.normal(0, 1, size=len(dates)).cumsum()
        prices = base_price + prices * 50  # Scale the prices
        
        # Generate OHLC data
        data = pd.DataFrame({
            'DATE': dates,
            'OPEN': prices + np.random.normal(0, 5, size=len(dates)),
            'HIGH': prices + np.random.normal(10, 5, size=len(dates)),
            'LOW': prices + np.random.normal(-10, 5, size=len(dates)),
            'CLOSE': prices,
            'VOLUME': np.random.randint(100000, 1000000, size=len(dates))
        })
        
        # Ensure High is highest and Low is lowest
        data['HIGH'] = data[['OPEN', 'HIGH', 'LOW', 'CLOSE']].max(axis=1)
        data['LOW'] = data[['OPEN', 'HIGH', 'LOW', 'CLOSE']].min(axis=1)
        
        return data.set_index('DATE')
    
    def get_top_gainers_losers(self) -> Dict[str, list]:
        """Get top gainers and losers."""
        # Mock implementation
        mock_data = {
            'top_gainers': [
                {'symbol': 'STOCK1', 'change_percent': 5.2},
                {'symbol': 'STOCK2', 'change_percent': 4.1},
                {'symbol': 'STOCK3', 'change_percent': 3.8}
            ],
            'top_losers': [
                {'symbol': 'STOCK4', 'change_percent': -4.5},
                {'symbol': 'STOCK5', 'change_percent': -3.9},
                {'symbol': 'STOCK6', 'change_percent': -3.2}
            ]
        }
        return mock_data
