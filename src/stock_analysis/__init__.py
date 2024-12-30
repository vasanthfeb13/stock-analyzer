"""
Stock Analysis Package

A Python package for analyzing stock market data using technical and fundamental analysis.
"""

__version__ = '1.0.0'
__author__ = 'Your Name'
__email__ = 'your.email@example.com'

# Import main components
from .main import StockAnalyzer
from .data_fetcher import DataFetcher
from .technical_analysis import TechnicalAnalyzer
from .fundamental_analysis import FundamentalAnalyzer
from .visualizer import Visualizer
from .cli import main

__all__ = [
    'StockAnalyzer',
    'DataFetcher',
    'TechnicalAnalyzer',
    'FundamentalAnalyzer',
    'Visualizer',
    'main'
]
