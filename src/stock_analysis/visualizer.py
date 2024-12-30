"""Visualization module for stock analysis."""

import logging
from typing import List, Optional
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf

class Visualizer:
    """Class for visualizing stock data and analysis results."""
    
    def __init__(self):
        """Initialize visualizer."""
        self.logger = logging.getLogger(__name__)
        self._setup_style()
    
    def _setup_style(self):
        """Set up plotting style."""
        plt.style.use('default')
        sns.set_theme(style="darkgrid")
    
    def plot_stock_data(
        self,
        data: pd.DataFrame,
        symbol: str,
        chart_type: str = 'line',
        indicators: Optional[List[str]] = None,
        output_dir: Optional[str] = None
    ) -> None:
        """
        Plot stock data with technical indicators.
        
        Args:
            data: DataFrame with OHLCV data
            symbol: Stock symbol
            chart_type: Type of chart ('line' or 'candlestick')
            indicators: List of indicators to plot
            output_dir: Directory to save plots
        """
        try:
            # Create output directory if it doesn't exist
            if output_dir:
                output_path = Path(output_dir)
                output_path.mkdir(parents=True, exist_ok=True)
            
            # Create figure and subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])
            
            # Plot price data
            if chart_type.lower() == 'candlestick':
                mpf.plot(
                    data,
                    type='candle',
                    style='charles',
                    title=f'{symbol} Stock Price',
                    ylabel='Price',
                    ax=ax1,
                    volume=ax2
                )
            else:
                data['CLOSE'].plot(ax=ax1, label='Close Price')
                ax1.set_title(f'{symbol} Stock Price')
                ax1.set_ylabel('Price')
                ax1.legend()
                
                # Plot volume
                data['VOLUME'].plot(ax=ax2, label='Volume', color='gray', alpha=0.5)
                ax2.set_ylabel('Volume')
                ax2.legend()
            
            # Adjust layout and save
            plt.tight_layout()
            if output_dir:
                plt.savefig(output_path / f'{symbol}_price.png')
                plt.close()
            
            # Plot technical indicators if specified
            if indicators:
                self._plot_indicators(data, symbol, indicators, output_dir)
            
        except Exception as e:
            self.logger.error(f"Error plotting stock data for {symbol}: {str(e)}")
    
    def _plot_indicators(
        self,
        data: pd.DataFrame,
        symbol: str,
        indicators: List[str],
        output_dir: Optional[str] = None
    ) -> None:
        """
        Plot technical indicators.
        
        Args:
            data: DataFrame with OHLCV data
            symbol: Stock symbol
            indicators: List of indicators to plot
            output_dir: Directory to save plots
        """
        try:
            for indicator in indicators:
                plt.figure(figsize=(12, 6))
                
                if indicator == 'RSI':
                    # Calculate and plot RSI
                    delta = data['CLOSE'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi = 100 - (100 / (1 + rs))
                    
                    plt.plot(rsi, label='RSI')
                    plt.axhline(y=70, color='r', linestyle='--', alpha=0.5)
                    plt.axhline(y=30, color='g', linestyle='--', alpha=0.5)
                    
                elif indicator == 'MACD':
                    # Calculate and plot MACD
                    exp1 = data['CLOSE'].ewm(span=12, adjust=False).mean()
                    exp2 = data['CLOSE'].ewm(span=26, adjust=False).mean()
                    macd = exp1 - exp2
                    signal = macd.ewm(span=9, adjust=False).mean()
                    
                    plt.plot(macd, label='MACD')
                    plt.plot(signal, label='Signal Line')
                    plt.bar(data.index, macd - signal, label='Histogram', alpha=0.3)
                    
                elif indicator == 'BB':
                    # Calculate and plot Bollinger Bands
                    ma20 = data['CLOSE'].rolling(window=20).mean()
                    std20 = data['CLOSE'].rolling(window=20).std()
                    
                    plt.plot(data['CLOSE'], label='Close Price')
                    plt.plot(ma20, label='20-day MA')
                    plt.plot(ma20 + (std20 * 2), label='Upper Band')
                    plt.plot(ma20 - (std20 * 2), label='Lower Band')
                
                plt.title(f'{symbol} - {indicator}')
                plt.legend()
                plt.grid(True, alpha=0.3)
                
                if output_dir:
                    plt.savefig(Path(output_dir) / f'{symbol}_{indicator}.png')
                plt.close()
                
        except Exception as e:
            self.logger.error(f"Error plotting indicators for {symbol}: {str(e)}")
    
    def plot_comparison(
        self,
        data: dict,
        output_dir: Optional[str] = None
    ) -> None:
        """
        Plot comparison of multiple stocks.
        
        Args:
            data: Dict of DataFrames with stock data
            output_dir: Directory to save plots
        """
        try:
            plt.figure(figsize=(12, 6))
            
            for symbol, df in data.items():
                # Normalize prices for comparison
                normalized = df['CLOSE'] / df['CLOSE'].iloc[0] * 100
                plt.plot(normalized, label=symbol)
            
            plt.title('Stock Price Comparison (Normalized)')
            plt.ylabel('Normalized Price (%)')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            if output_dir:
                plt.savefig(Path(output_dir) / 'comparison.png')
            plt.close()
            
        except Exception as e:
            self.logger.error(f"Error plotting stock comparison: {str(e)}")
    
    def plot_correlation(
        self,
        data: dict,
        output_dir: Optional[str] = None
    ) -> None:
        """
        Plot correlation matrix of stocks.
        
        Args:
            data: Dict of DataFrames with stock data
            output_dir: Directory to save plots
        """
        try:
            # Create correlation matrix
            returns = pd.DataFrame()
            for symbol, df in data.items():
                returns[symbol] = df['CLOSE'].pct_change()
            
            corr = returns.corr()
            
            # Plot correlation matrix
            plt.figure(figsize=(10, 8))
            sns.heatmap(
                corr,
                annot=True,
                cmap='coolwarm',
                center=0,
                fmt='.2f',
                square=True
            )
            
            plt.title('Stock Returns Correlation Matrix')
            
            if output_dir:
                plt.savefig(Path(output_dir) / 'correlation.png')
            plt.close()
            
        except Exception as e:
            self.logger.error(f"Error plotting correlation matrix: {str(e)}")
