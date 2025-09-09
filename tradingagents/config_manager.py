"""
Unified Configuration Management for TradingAgents

This module provides a centralized configuration system that handles
both US and Indian market configurations with proper validation and
environment variable support.
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from .default_config import DEFAULT_CONFIG
from .indian_config import INDIAN_CONFIG


class ConfigManager:
    """Centralized configuration manager for TradingAgents."""
    
    def __init__(self, market_type: str = "us", config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            market_type: Type of market ("us" or "india")
            config_path: Optional path to custom config file
        """
        self.market_type = market_type.lower()
        self.config_path = config_path
        self._config = self._load_config()
        self._validate_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration based on market type and custom config."""
        
        # Start with base config
        if self.market_type == "india":
            base_config = INDIAN_CONFIG.copy()
        else:
            base_config = DEFAULT_CONFIG.copy()
        
        # Load custom config if provided
        if self.config_path and os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    custom_config = json.load(f)
                base_config.update(custom_config)
            except Exception as e:
                print(f"Warning: Could not load custom config from {self.config_path}: {e}")
        
        # Override with environment variables
        self._apply_env_overrides(base_config)
        
        return base_config
    
    def _apply_env_overrides(self, config: Dict[str, Any]) -> None:
        """Apply environment variable overrides to config."""
        
        env_mappings = {
            "TRADINGAGENTS_LLM_PROVIDER": "llm_provider",
            "TRADINGAGENTS_DEEP_THINK_LLM": "deep_think_llm",
            "TRADINGAGENTS_QUICK_THINK_LLM": "quick_think_llm",
            "TRADINGAGENTS_BACKEND_URL": "backend_url",
            "TRADINGAGENTS_MAX_DEBATE_ROUNDS": "max_debate_rounds",
            "TRADINGAGENTS_ONLINE_TOOLS": "online_tools",
            "OPENAI_API_KEY": None,  # Handled by langchain
            "ANTHROPIC_API_KEY": None,  # Handled by langchain
            "GOOGLE_API_KEY": None,  # Handled by langchain
        }
        
        for env_var, config_key in env_mappings.items():
            if config_key and env_var in os.environ:
                value = os.environ[env_var]
                
                # Type conversion for specific keys
                if config_key == "max_debate_rounds":
                    try:
                        value = int(value)
                    except ValueError:
                        print(f"Warning: Invalid value for {env_var}, using default")
                        continue
                elif config_key == "online_tools":
                    value = value.lower() in ('true', '1', 'yes', 'on')
                
                config[config_key] = value
    
    def _validate_config(self) -> None:
        """Validate configuration values."""
        
        required_keys = [
            "llm_provider", "deep_think_llm", "quick_think_llm",
            "backend_url", "max_debate_rounds", "online_tools"
        ]
        
        for key in required_keys:
            if key not in self._config:
                raise ValueError(f"Missing required configuration key: {key}")
        
        # Validate LLM provider
        valid_providers = ["openai", "anthropic", "google", "ollama", "openrouter"]
        if self._config["llm_provider"] not in valid_providers:
            raise ValueError(f"Invalid LLM provider: {self._config['llm_provider']}")
        
        # Validate numeric values
        if not isinstance(self._config["max_debate_rounds"], int) or self._config["max_debate_rounds"] < 1:
            raise ValueError("max_debate_rounds must be a positive integer")
        
        # Create necessary directories
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        
        directories = [
            self._config.get("results_dir", "./results"),
            self._config.get("data_dir", "./data"),
            self._config.get("data_cache_dir", "./dataflows/data_cache"),
        ]
        
        for directory in directories:
            if directory:
                os.makedirs(directory, exist_ok=True)
    
    def get_config(self) -> Dict[str, Any]:
        """Get the current configuration."""
        return self._config.copy()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a specific configuration value."""
        return self._config.get(key, default)
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update configuration with new values."""
        self._config.update(updates)
        self._validate_config()
    
    def save_config(self, path: str) -> None:
        """Save current configuration to file."""
        try:
            with open(path, 'w') as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            raise Exception(f"Could not save config to {path}: {e}")
    
    def is_indian_market(self) -> bool:
        """Check if configured for Indian market."""
        return self.market_type == "india" or self._config.get("market", "us").lower() == "india"
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service."""
        service_mappings = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "google": "GOOGLE_API_KEY",
            "finnhub": "FINNHUB_API_KEY",
            "alpha_vantage": "ALPHA_VANTAGE_API_KEY",
        }
        
        env_var = service_mappings.get(service.lower())
        if env_var:
            return os.environ.get(env_var)
        
        return None


# Global configuration instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager(market_type: str = "us", config_path: Optional[str] = None) -> ConfigManager:
    """Get or create global configuration manager."""
    global _config_manager
    
    if _config_manager is None:
        _config_manager = ConfigManager(market_type, config_path)
    
    return _config_manager


def set_config_manager(config_manager: ConfigManager) -> None:
    """Set global configuration manager."""
    global _config_manager
    _config_manager = config_manager


def get_config() -> Dict[str, Any]:
    """Get current configuration (for backward compatibility)."""
    return get_config_manager().get_config()


def set_config(config: Dict[str, Any]) -> None:
    """Set configuration (for backward compatibility)."""
    get_config_manager().update(config)
