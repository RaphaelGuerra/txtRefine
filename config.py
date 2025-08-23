#!/usr/bin/env python3
"""
Configuration management for txtRefine.
Centralizes all configurable parameters.
"""

import os
from pathlib import Path
from typing import Dict, Any
import json


class Config:
    """Configuration manager for txtRefine."""

    def __init__(self, config_file: str = None):
        self.config_file = config_file or os.path.join(
            os.path.dirname(__file__), 'config.json'
        )
        self._config = self._load_default_config()
        self._load_config_file()

    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration values."""
        return {
            # Model settings
            'default_model': 'llama3.2:latest',
            'fallback_models': ['neural-chat:latest', 'openchat:latest'],
            'model_timeout': 120,  # seconds

            # Processing settings
            'max_words_per_chunk': 800,
            'min_words_per_chunk': 400,
            'max_retries': 3,
            'retry_delay': 2,
            'content_loss_threshold': 0.7,

            # File settings
            'default_encoding': 'utf-8',
            'output_prefix': 'refined_',
            'backup_prefix': 'backup_',
            'max_backup_files': 10,

            # Performance settings
            'parallel_processing': False,
            'max_parallel_chunks': 3,
            'cache_refinements': True,
            'cache_dir': 'cache',

            # UI settings
            'progress_bar': True,
            'verbose_logging': False,
            'color_output': True,

            # Prompt settings
            'custom_prompt_template': None,
            'preserve_academic_terms': True,
        }

    def _load_config_file(self):
        """Load configuration from JSON file if it exists."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    self._config.update(file_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")

    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save config file {self.config_file}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value."""
        self._config[key] = value

    def update(self, config_dict: Dict[str, Any]):
        """Update multiple configuration values."""
        self._config.update(config_dict)

    # Convenient property accessors
    @property
    def default_model(self) -> str:
        return self.get('default_model')

    @property
    def max_words_per_chunk(self) -> int:
        return self.get('max_words_per_chunk')

    @property
    def max_retries(self) -> int:
        return self.get('max_retries')

    @property
    def parallel_processing(self) -> bool:
        return self.get('parallel_processing')


# Global configuration instance
config = Config()
