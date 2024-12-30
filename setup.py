from setuptools import setup, find_packages
import os

# Read version from __init__.py
version = '1.0.0'

# Read README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stock-analyzer',
    version=version,
    author='Stock Analyzer Team',
    author_email='support@stockanalyzer.com',
    description='A comprehensive stock analysis tool for technical and fundamental analysis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vasanthfeb13/stock-analyzer',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Office/Business :: Financial :: Investment',
    ],
    python_requires='>=3.8',
    install_requires=[
        'pandas>=2.2.0',
        'numpy>=1.26.0',
        'matplotlib>=3.9.0',
        'mplfinance>=0.12.10b0',
        'TA-Lib>=0.5.0',
        'seaborn>=0.13.0',
        'requests>=2.31.0',
        'python-dateutil>=2.9.0',
        'colorama>=0.4.6',
    ],
    entry_points={
        'console_scripts': [
            'stock-analyzer=stock_analysis.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
