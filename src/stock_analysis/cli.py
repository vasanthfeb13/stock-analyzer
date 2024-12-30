#!/usr/bin/env python3
"""
Command Line Interface for Stock Analyzer
"""

import argparse
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import colorama
from colorama import Fore, Style

from .main import StockAnalyzer
from . import __version__

# Initialize colorama
colorama.init()

# ASCII Art Logo
LOGO = f"""{Fore.CYAN}
╔═══════════════════════════════════════════════════════════════╗
║  ███████╗████████╗ ██████╗  ██████╗██╗  ██╗                  ║
║  ██╔════╝╚══██╔══╝██╔═══██╗██╔════╝██║ ██╔╝                  ║
║  ███████╗   ██║   ██║   ██║██║     █████╔╝                   ║
║  ╚════██║   ██║   ██║   ██║██║     ██╔═██╗                   ║
║  ███████║   ██║   ╚██████╔╝╚██████╗██║  ██╗                  ║
║  ╚══════╝   ╚═╝    ╚═════╝  ╚═════╝╚═╝  ╚═╝                  ║
║     █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗███████╗ ║
║    ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝██╔════╝██╔════╝ ║
║    ███████║██╔██╗ ██║███████║██║   ╚████╔╝ █████╗  ███████╗ ║
║    ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝  ██╔══╝  ╚════██║ ║
║    ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████╗███████║ ║
║    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚══════╝ ║
╚═══════════════════════════════════════════════════════════════╝
{Style.BRIGHT}{Fore.WHITE}Version: {__version__}{Style.RESET_ALL}
"""

# Configure logging
def setup_logging(verbose: bool = False):
    """
    Set up logging configuration.
    
    Args:
        verbose: If True, set log level to DEBUG
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format=f'{Fore.YELLOW}%(asctime)s{Style.RESET_ALL} - %(name)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

def validate_symbols(symbols: str) -> List[str]:
    """
    Validate stock symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols
        
    Returns:
        List of validated stock symbols
    """
    if not symbols:
        raise ValueError("Stock symbols must be provided")
    
    symbol_list = [s.strip().upper() for s in symbols.split(',')]
    
    if not all(symbol.isalnum() for symbol in symbol_list):
        raise ValueError("Stock symbols must be alphanumeric")
    
    return symbol_list

def validate_period(period: int) -> int:
    """
    Validate analysis period.
    
    Args:
        period: Number of days for analysis
        
    Returns:
        Validated period
    """
    if period <= 0:
        raise ValueError("Period must be a positive integer")
    if period > 365 * 5:  # 5 years
        raise ValueError("Period cannot exceed 1825 days (5 years)")
    return period

def validate_indicators(indicators: str) -> List[str]:
    """
    Validate technical indicators.
    
    Args:
        indicators: Comma-separated list of indicators
        
    Returns:
        List of validated indicators
    """
    if not indicators:
        return ['RSI', 'MACD']  # Default indicators
    
    valid_indicators = {'RSI', 'MACD', 'BB'}
    indicator_list = [i.strip().upper() for i in indicators.split(',')]
    
    invalid = set(indicator_list) - valid_indicators
    if invalid:
        raise ValueError(f"Invalid indicators: {', '.join(invalid)}")
    
    return indicator_list

def validate_chart_type(chart_type: str) -> str:
    """
    Validate chart type.
    
    Args:
        chart_type: Type of chart to generate
        
    Returns:
        Validated chart type
    """
    valid_types = {'line', 'candlestick'}
    chart_type = chart_type.lower()
    
    if chart_type not in valid_types:
        raise ValueError(f"Invalid chart type. Must be one of: {', '.join(valid_types)}")
    
    return chart_type

def validate_output_dir(output_dir: str) -> str:
    """
    Validate and create output directory.
    
    Args:
        output_dir: Path to output directory
        
    Returns:
        Validated output directory path
    """
    if not output_dir:
        return None
        
    path = Path(output_dir)
    try:
        path.mkdir(parents=True, exist_ok=True)
        return str(path)
    except Exception as e:
        raise ValueError(f"Invalid output directory: {e}")

def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Stock Analyzer - Technical and Fundamental Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --symbols TATAMOTORS,WIPRO,BHARTIARTL
  %(prog)s --symbols RELIANCE,TCS --period 90 --indicators RSI,MACD
  %(prog)s --symbols INFY --chart-type line --output-dir my_charts
        """
    )
    
    parser.add_argument(
        '--symbols',
        type=str,
        required=True,
        help='Comma-separated list of stock symbols (e.g., TATAMOTORS,WIPRO)'
    )
    
    parser.add_argument(
        '--period',
        type=int,
        default=365,
        help='Analysis period in days (default: 365, max: 1825)'
    )
    
    parser.add_argument(
        '--indicators',
        type=str,
        default='RSI,MACD',
        help='Technical indicators to display (RSI,MACD,BB)'
    )
    
    parser.add_argument(
        '--chart-type',
        type=str,
        default='line',
        help='Type of chart to generate (line, candlestick)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Directory to save charts (default: stock_charts)'
    )
    
    parser.add_argument(
        '--top-n',
        type=int,
        help='Show only top N stocks by volume'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    return parser.parse_args(args)

def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        argv: List of command line arguments
        
    Returns:
        Exit code
    """
    try:
        args = parse_args(argv or sys.argv[1:])
        setup_logging(args.verbose)
        
        # Display logo and start message
        print(LOGO)
        print(f"{Fore.GREEN}Stock Analysis Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60 + Style.RESET_ALL)
        print()

        # Validate inputs
        symbols = validate_symbols(args.symbols)
        indicators = validate_indicators(args.indicators) if args.indicators else None
        chart_type = validate_chart_type(args.chart_type) if args.chart_type else 'candlestick'
        output_dir = validate_output_dir(args.output_dir) if args.output_dir else Path('stock_charts')
        
        # Initialize analyzer
        analyzer = StockAnalyzer(
            symbols=symbols,
            period=args.period,
            indicators=indicators,
            chart_type=chart_type,
            output_dir=output_dir
        )
        
        # Run analysis
        analyzer.run()
        
        # Display completion message
        print()
        print(f"{Fore.GREEN}Analysis completed successfully!")
        print(f"Charts have been saved to: {output_dir}")
        print("=" * 60 + Style.RESET_ALL)
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Analysis interrupted by user{Style.RESET_ALL}")
        return 1
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}", exc_info=True)
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
