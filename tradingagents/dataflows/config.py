"""
Configuration module for TradingAgents dataflows.

This module provides backward compatibility while leveraging the new
unified configuration management system.
"""

from typing import Dict, Optional
try:
    from ..config_manager import get_config_manager, ConfigManager
    NEW_CONFIG_AVAILABLE = True
except ImportError:
    # Fallback to old system
    import tradingagents.default_config as default_config
    NEW_CONFIG_AVAILABLE = False

# Global variables for backward compatibility
_config: Optional[Dict] = None
DATA_DIR: Optional[str] = None


def initialize_config():
    """Initialize the configuration with default values."""
    global _config, DATA_DIR
    
    if _config is None:
        if NEW_CONFIG_AVAILABLE:
            config_manager = get_config_manager()
            _config = config_manager.get_config()
        else:
            _config = default_config.DEFAULT_CONFIG.copy()
        
        DATA_DIR = _config.get("data_dir", "./data")


def set_config(config: Dict):
    """Update the configuration with custom values."""
    global _config, DATA_DIR
    
    if _config is None:
        initialize_config()
    
    _config.update(config)
    DATA_DIR = _config.get("data_dir", "./data")
    
    # Update the global config manager if available
    if NEW_CONFIG_AVAILABLE:
        try:
            config_manager = get_config_manager()
            config_manager.update(config)
        except Exception as e:
            print(f"Warning: Could not update global config manager: {e}")


def get_config() -> Dict:
    """Get the current configuration."""
    if _config is None:
        initialize_config()
    return _config.copy()


def get_data_dir() -> str:
    """Get the data directory path."""
    if DATA_DIR is None:
        initialize_config()
    return DATA_DIR or "./data"


# Initialize with default config
initialize_config()
