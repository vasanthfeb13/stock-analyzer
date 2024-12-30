"""
Main module for stock analysis
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import argparse

from .data_fetcher import DataFetcher
from .technical_analysis import TechnicalAnalyzer
from .fundamental_analysis import FundamentalAnalyzer
from .visualizer import Visualizer

class StockAnalyzer:
    """Main class for stock analysis."""
    
    def __init__(
        self,
        symbols: List[str],
        period: int = 365,
        indicators: Optional[List[str]] = None,
        chart_type: str = 'candlestick',
        output_dir: Optional[Path] = None
    ):
        """
        Initialize stock analyzer.
        
        Args:
            symbols: List of stock symbols to analyze
            period: Analysis period in days
            indicators: List of technical indicators to calculate
            chart_type: Type of chart to generate
            output_dir: Directory to save charts
        """
        self._setup_logging()
        self.data_fetcher = DataFetcher()
        self.tech_analyzer = TechnicalAnalyzer()
        self.fund_analyzer = FundamentalAnalyzer()
        self.visualizer = Visualizer()
        
        # Store parameters
        self.symbols = symbols
        self.period = period
        self.indicators = indicators or ['RSI', 'MACD']
        self.chart_type = chart_type
        self.output_dir = output_dir or Path('stock_charts')
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def run(self) -> Dict:
        """
        Run the stock analysis.
        
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Log analysis start
            self.logger.info(f"Analyzing {', '.join(self.symbols)}...")
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.period)
            
            results = {}
            for symbol in self.symbols:
                # Fetch data
                data = self.data_fetcher.get_historical_data(
                    symbol,
                    start_date=start_date,
                    end_date=end_date
                )
                
                if data.empty:
                    self.logger.warning(f"No data available for {symbol}")
                    continue
                
                # Set data for technical analysis
                self.tech_analyzer.set_data(data)
                
                # Perform technical analysis
                tech_results = self.tech_analyzer.analyze(self.indicators)
                
                # Generate charts
                if self.output_dir:
                    self.visualizer.plot_stock_data(
                        data,
                        symbol,
                        chart_type=self.chart_type,
                        indicators=self.indicators,
                        output_dir=self.output_dir
                    )
                
                # Store results
                results[symbol] = {
                    'technical_indicators': tech_results,
                    'current_data': self.data_fetcher.get_current_data(symbol)
                }
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error during analysis: {str(e)}", exc_info=True)
            raise
    
    def _print_analysis_report(self, results: Dict):
        """
        Print analysis report.
        
        Args:
            results: Analysis results
        """
        for symbol, data in results.items():
            print(f"\nAnalysis Report for {symbol}")
            print("-" * 40)
            
            # Print current market data
            current_data = data['current_data']
            print("\nCurrent Market Data:")
            print(f"Last Price: {current_data['last_price']}")
            print(f"Change: {current_data['change']}")
            print(f"Volume: {current_data['volume']:,}")
            print(f"Last Updated: {current_data['timestamp']}")
            
            # Print technical indicators
            tech_indicators = data['technical_indicators']
            print("\nTechnical Indicators:")
            
            if tech_indicators.rsi is not None:
                print(f"RSI: {tech_indicators.rsi:.2f}")
            
            if tech_indicators.macd is not None:
                print("\nMACD:")
                print(f"MACD Line: {tech_indicators.macd['macd_line']:.2f}")
                print(f"Signal Line: {tech_indicators.macd['signal_line']:.2f}")
                print(f"Histogram: {tech_indicators.macd['histogram']:.2f}")
            
            if tech_indicators.bollinger_bands is not None:
                print("\nBollinger Bands:")
                print(f"Upper Band: {tech_indicators.bollinger_bands['upper_band']:.2f}")
                print(f"Middle Band: {tech_indicators.bollinger_bands['middle_band']:.2f}")
                print(f"Lower Band: {tech_indicators.bollinger_bands['lower_band']:.2f}")
            
            print("\n" + "=" * 40)

def main():
    """Main entry point for the stock analysis program."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Stock Analysis Tool')
    parser.add_argument('--stocks', type=str, help='Comma-separated list of stock symbols (e.g., RELIANCE,TCS,INFY)')
    parser.add_argument('--period', type=int, default=180, help='Analysis period in days (default: 180)')
    parser.add_argument('--indicators', type=str, default='all',
                       help='Comma-separated list of technical indicators to show (RSI,MACD,BB,MA,VOL) or "all"')
    parser.add_argument('--chart-type', type=str, default='candlestick',
                       choices=['candlestick', 'line', 'all'],
                       help='Type of chart to generate (default: candlestick)')
    parser.add_argument('--output-dir', type=str, default='stock_charts',
                       help='Directory to save charts (default: stock_charts)')
    parser.add_argument('--top-n', type=int, help='Show only top N stocks by volume')
    args = parser.parse_args()
    
    analyzer = StockAnalyzer(
        symbols=[s.strip().upper() for s in args.stocks.split(',')] if args.stocks else [
            "RELIANCE",  # Reliance Industries
            "TCS",      # Tata Consultancy Services
            "INFY",     # Infosys
            "HDFCBANK", # HDFC Bank
            "ITC"       # ITC Limited
        ],
        period=args.period,
        indicators=[i.strip().upper() for i in args.indicators.split(',')] if args.indicators != 'all' else None,
        chart_type=args.chart_type,
        output_dir=Path(args.output_dir)
    )
    
    try:
        # Get market overview
        # market_overview = analyzer._get_market_status()
        # print("\nMarket Overview:")
        # print(f"Status: {market_overview['status']}")
        # print(f"Time: {market_overview['timestamp']}\n")
        
        # Analyze stocks
        results = analyzer.run()
        
        # Print analysis report
        analyzer._print_analysis_report(results)
        
    except Exception as e:
        print(f"\nError in main program: {e}")

if __name__ == "__main__":
    main()
