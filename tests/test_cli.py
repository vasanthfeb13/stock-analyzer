import unittest
from unittest.mock import patch
from stock_analysis.cli import parse_args

class TestCLI(unittest.TestCase):
    def test_parse_args_default(self):
        with patch('sys.argv', ['stock-analyzer', '--symbols', 'TATAMOTORS']):
            args = parse_args()
            self.assertEqual(args.symbols, ['TATAMOTORS'])
            self.assertEqual(args.period, 90)  # Default period
            self.assertEqual(args.indicators, ['RSI', 'MACD'])  # Default indicators

    def test_parse_args_multiple_symbols(self):
        with patch('sys.argv', ['stock-analyzer', '--symbols', 'TATAMOTORS,RELIANCE']):
            args = parse_args()
            self.assertEqual(args.symbols, ['TATAMOTORS', 'RELIANCE'])

    def test_parse_args_custom_period(self):
        with patch('sys.argv', ['stock-analyzer', '--symbols', 'TATAMOTORS', '--period', '30']):
            args = parse_args()
            self.assertEqual(args.period, 30)

    def test_parse_args_custom_indicators(self):
        with patch('sys.argv', ['stock-analyzer', '--symbols', 'TATAMOTORS', '--indicators', 'RSI']):
            args = parse_args()
            self.assertEqual(args.indicators, ['RSI'])

if __name__ == '__main__':
    unittest.main()
