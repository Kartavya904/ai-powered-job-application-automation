"""
Configuration Loader Module
Loads and validates configuration from config.yaml.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigLoader:
    """Load and manage configuration from YAML files."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize config loader.
        
        Args:
            config_path: Path to config.yaml file
        """
        self.config_path = Path(config_path)
        self.config: Optional[Dict[str, Any]] = None
        self.load()
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        return self.config
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path (e.g., 'job_preferences.remote_only')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        if self.config is None:
            self.load()
        
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def save(self, output_path: Optional[Path] = None) -> None:
        """Save current configuration to YAML file."""
        if self.config is None:
            raise ValueError("No configuration loaded")
        
        output_path = output_path or self.config_path
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
    
    def validate(self) -> bool:
        """
        Validate configuration structure.
        
        Returns:
            True if valid, raises ValueError if invalid
        """
        required_sections = [
            'job_preferences',
            'ai_settings',
            'resume',
            'automation',
            'logging',
        ]
        
        if self.config is None:
            raise ValueError("No configuration loaded")
        
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        return True


# Global config instance
_config = None


def get_config(config_path: str = "config.yaml") -> ConfigLoader:
    """Get or create global config instance."""
    global _config
    if _config is None:
        _config = ConfigLoader(config_path)
    return _config

