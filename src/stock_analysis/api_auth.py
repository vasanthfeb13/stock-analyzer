import time
from typing import Dict, Optional, Callable
import logging
from functools import wraps
import json
import os
from datetime import datetime, timedelta
import requests
from dataclasses import dataclass

@dataclass
class APICredentials:
    """Store API credentials"""
    api_key: str
    api_secret: Optional[str] = None
    access_token: Optional[str] = None
    token_expiry: Optional[datetime] = None

class RateLimiter:
    """
    Implements rate limiting for API calls
    """
    
    def __init__(self, calls: int, period: int):
        """
        Initialize rate limiter
        
        Args:
            calls: Number of calls allowed
            period: Time period in seconds
        """
        self.calls = calls
        self.period = period
        self.timestamps = []

    def __call__(self, func: Callable) -> Callable:
        """Decorator to implement rate limiting"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Remove timestamps outside the window
            self.timestamps = [
                ts for ts in self.timestamps 
                if ts > now - self.period
            ]
            
            if len(self.timestamps) >= self.calls:
                sleep_time = self.timestamps[0] - (now - self.period)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
            self.timestamps.append(now)
            return func(*args, **kwargs)
            
        return wrapper

class NSEAuthManager:
    """
    Handles authentication and session management for NSE API
    """
    
    def __init__(self, credentials_file: str = "nse_credentials.json"):
        """
        Initialize auth manager
        
        Args:
            credentials_file: Path to credentials file
        """
        self.credentials_file = credentials_file
        self.credentials = self._load_credentials()
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _load_credentials(self) -> APICredentials:
        """Load credentials from file"""
        try:
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as f:
                    creds = json.load(f)
                return APICredentials(**creds)
            else:
                self.logger.warning(
                    f"Credentials file {self.credentials_file} not found"
                )
                return APICredentials(api_key="")
        except Exception as e:
            self.logger.error(f"Error loading credentials: {str(e)}")
            return APICredentials(api_key="")

    def _save_credentials(self):
        """Save credentials to file"""
        try:
            with open(self.credentials_file, 'w') as f:
                json.dump(
                    {
                        'api_key': self.credentials.api_key,
                        'api_secret': self.credentials.api_secret,
                        'access_token': self.credentials.access_token,
                        'token_expiry': self.credentials.token_expiry.isoformat() 
                            if self.credentials.token_expiry else None
                    },
                    f
                )
        except Exception as e:
            self.logger.error(f"Error saving credentials: {str(e)}")

    def set_credentials(
        self, 
        api_key: str, 
        api_secret: Optional[str] = None
    ):
        """
        Set API credentials
        
        Args:
            api_key: NSE API key
            api_secret: NSE API secret
        """
        self.credentials = APICredentials(
            api_key=api_key,
            api_secret=api_secret
        )
        self._save_credentials()

    def _generate_access_token(self) -> Optional[str]:
        """Generate new access token"""
        try:
            response = requests.post(
                "https://api.nseindia.com/auth/token",
                headers={
                    "X-API-KEY": self.credentials.api_key,
                    "X-API-SECRET": self.credentials.api_secret
                }
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('access_token')
        except Exception as e:
            self.logger.error(f"Error generating access token: {str(e)}")
            return None

    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests
        
        Returns:
            Dictionary of headers including authentication
        """
        now = datetime.now()
        
        # Check if token needs refresh
        if (
            not self.credentials.access_token or
            not self.credentials.token_expiry or
            now >= self.credentials.token_expiry
        ):
            token = self._generate_access_token()
            if token:
                self.credentials.access_token = token
                self.credentials.token_expiry = now + timedelta(hours=1)
                self._save_credentials()
        
        return {
            "X-API-KEY": self.credentials.api_key,
            "Authorization": f"Bearer {self.credentials.access_token}"
                if self.credentials.access_token else "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/91.0.4472.124 Safari/537.36"
        }

class APISession:
    """
    Manages API session with rate limiting and authentication
    """
    
    def __init__(
        self, 
        auth_manager: NSEAuthManager,
        rate_limit_calls: int = 100,
        rate_limit_period: int = 60
    ):
        """
        Initialize API session
        
        Args:
            auth_manager: Authentication manager instance
            rate_limit_calls: Number of calls allowed in period
            rate_limit_period: Time period in seconds
        """
        self.auth_manager = auth_manager
        self.rate_limiter = RateLimiter(rate_limit_calls, rate_limit_period)
        self.session = requests.Session()

    @RateLimiter(calls=100, period=60)
    def get(self, url: str, **kwargs) -> requests.Response:
        """
        Make GET request with rate limiting and authentication
        
        Args:
            url: Request URL
            **kwargs: Additional request parameters
        """
        headers = self.auth_manager.get_auth_headers()
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        
        response = self.session.get(url, **kwargs)
        response.raise_for_status()
        return response

    @RateLimiter(calls=100, period=60)
    def post(self, url: str, **kwargs) -> requests.Response:
        """
        Make POST request with rate limiting and authentication
        
        Args:
            url: Request URL
            **kwargs: Additional request parameters
        """
        headers = self.auth_manager.get_auth_headers()
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        
        response = self.session.post(url, **kwargs)
        response.raise_for_status()
        return response
