# Stock Analyzer 📈

A powerful Python-based stock analysis tool for Indian markets, providing comprehensive technical analysis with beautiful visualizations.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://github.com/vasanthfeb13/stock-analyzer/workflows/Python%20application/badge.svg)

## 🌟 Features

### Technical Analysis
- **RSI (Relative Strength Index)** - Momentum indicator
- **MACD** - Trend-following momentum indicator
- **Volume Analysis** - Trading volume patterns
- **Moving Averages** - Simple and Exponential
- **Support/Resistance Levels** - Key price levels

### Data Visualization
- **Interactive Charts** - Candlestick/OHLC patterns
- **Technical Overlays** - Indicators on price charts
- **Volume Profiles** - Volume distribution analysis
- **Multi-timeframe Analysis** - Different time periods
- **Export Options** - Save charts as PNG/PDF

### User Experience
- **Command-line Interface** - Easy to use CLI
- **Customizable Analysis** - Flexible parameters
- **Real-time Updates** - Live market data
- **Batch Processing** - Analyze multiple stocks
- **Progress Tracking** - Visual feedback

## 🚀 Installation Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/vasanthfeb13/stock-analyzer.git
cd stock-analyzer
```

### Step 2: Install TA-Lib
TA-Lib is required for technical analysis. Follow the platform-specific instructions:

**macOS:**
```bash
brew install ta-lib
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ta-lib
```

**Windows:**
Download and install the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)

### Step 3: Install Dependencies and Setup
```bash
# Create and activate virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Step 4: Run the Analyzer
You can run the analyzer in two ways:

1. Using the run script:
```bash
python run.py --symbols TATAMOTORS
```

2. Using the installed command:
```bash
stock-analyzer --symbols TATAMOTORS
```

## 📊 Usage Examples

### Basic Stock Analysis
```bash
stock-analyzer --symbols TATAMOTORS
```

### Multiple Stocks
```bash
stock-analyzer --symbols TATAMOTORS,RELIANCE,TCS
```

### Custom Period
```bash
stock-analyzer --symbols TATAMOTORS --period 60
```

### Full Analysis
```bash
stock-analyzer --symbols TATAMOTORS \
              --period 30 \
              --indicators RSI,MACD \
              --chart-type candlestick \
              --output-dir my_analysis
```

## 📸 Sample Outputs

Here are some sample outputs from the Stock Analyzer:

### CLI Interface
![CLI Startup](samples/cli_startup.png)
*Stock Analyzer CLI startup screen with ASCII art logo*

### Installation Process
![Installation](samples/installation.png)
*Installing dependencies in a virtual environment*

### Project Structure
![Project Structure](samples/project_structure.png)
*Project directory structure showing main components*

### Package Installation
![Package Installation](samples/package_installation.png)
*Successful package installation output*

### Technical Analysis
![MACD Analysis](samples/sample_macd.png)
*Sample MACD technical analysis chart for TATAMOTORS*

## 📋 Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--symbols` | Stock symbols (comma-separated) | Required |
| `--period` | Analysis period in days | 90 |
| `--indicators` | Technical indicators | RSI,MACD |
| `--chart-type` | Chart type (candlestick/line) | candlestick |
| `--output-dir` | Output directory | stock_charts |
| `--verbose` | Detailed output | False |

## 📁 Output Files

```
stock_charts/
├── SYMBOL_price.png      # Price chart with indicators
├── SYMBOL_volume.png     # Volume analysis
├── SYMBOL_indicators.png # Technical indicators
└── analysis_report.txt   # Summary report
```

## 🐛 Troubleshooting

### Common Issues

1. **Virtual Environment**
   ```bash
   # If you see import errors, make sure your virtual environment is activated:
   source .venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```

2. **TA-Lib Installation**
   - If TA-Lib installation fails, try installing from wheels:
   ```bash
   # Windows: Download appropriate wheel from
   # https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
   pip install TA_Lib‑0.4.24‑cp39‑cp39‑win_amd64.whl
   ```

3. **Package Not Found**
   ```bash
   # Reinstall the package
   pip install -e .
   ```

### Getting Help
- Check installation: `pip list | grep stock-analyzer`
- Verify dependencies: `pip freeze`
- Report issues on our [GitHub repository](https://github.com/vasanthfeb13/stock-analyzer/issues)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for market data
- [TA-Lib](https://github.com/mrjbq7/ta-lib) for technical analysis
- [mplfinance](https://github.com/matplotlib/mplfinance) for charting
- [pandas](https://github.com/pandas-dev/pandas) for data processing

## 📬 Support

- Report issues on GitHub
- Join our community discussions
- Follow us for updates

---
Made with ❤️ by Stock Analyzer Team
