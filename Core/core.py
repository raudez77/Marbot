import os
import pathlib
from typing import Optional
from pydantic import BaseModel
from strictyaml  import YAML , load


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent
ROOT =  PACKAGE_ROOT.parent 
CONFIG_FILE_PATH = PACKAGE_ROOT / 'config.yml'
DATA_DIR = ROOT / 'Tasks'

class OpenAIConnectionPointConfig(BaseModel):
    """ Application-level config for openai"""

    author: str
    model: str
    openai_keys: list

class OtherFunctions (BaseModel):
    """ Application-level config for OtherFunctions """

    other_messages:list
    chain_flows:list

class Config (BaseModel):
    """ Master Config Object"""
    app_config_openai : OpenAIConnectionPointConfig
    app_config_other : OtherFunctions


def find_config_file() -> pathlib.Path:
    """ Locate the configuration file"""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"config file not found at {CONFIG_FILE_PATH!r}")

def fetch_config_from_yaml (cfg_path: Optional[pathlib.Path] = None) -> YAML:
    """ Pase YAML containing the app configuration"""
    
    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open (cfg_path, "r") as config_file:
            # Load configuration file YAML
            parse_config = load(config_file.read())
            return parse_config

    raise OSError(f"Did not find config file at path {cfg_path}")

def create_and_validate_connection_points (parsed_config:YAML = None) -> Config:
    """ Run validation on config values. """

    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

        # Load the data attribute from strict  YAML type.
        _config = Config(
            app_config_openai = OpenAIConnectionPointConfig(**parsed_config.data),
            app_config_other = OtherFunctions(**parsed_config.data)
        )

        return _config
    
config = create_and_validate_connection_points()