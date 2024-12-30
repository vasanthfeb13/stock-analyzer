import unittest
import pandas as pd
import numpy as np
from stock_analysis.technical_analysis import calculate_rsi, calculate_macd

class TestTechnicalAnalysis(unittest.TestCase):
    def setUp(self):
        # Create sample data
        dates = pd.date_range(start='2024-01-01', periods=100)
        self.data = pd.DataFrame({
            'Close': np.random.randn(100).cumsum() + 100,  # Random walk starting at 100
            'Volume': np.random.randint(1000, 10000, 100)
        }, index=dates)

    def test_rsi_calculation(self):
        # Test RSI calculation
        rsi = calculate_rsi(self.data['Close'])
        self.assertIsInstance(rsi, pd.Series)
        self.assertTrue(all(0 <= x <= 100 for x in rsi.dropna()))
        self.assertEqual(len(rsi), len(self.data))

    def test_macd_calculation(self):
        # Test MACD calculation
        macd, signal, hist = calculate_macd(self.data['Close'])
        self.assertIsInstance(macd, pd.Series)
        self.assertIsInstance(signal, pd.Series)
        self.assertIsInstance(hist, pd.Series)
        self.assertEqual(len(macd), len(self.data))

if __name__ == '__main__':
    unittest.main()
