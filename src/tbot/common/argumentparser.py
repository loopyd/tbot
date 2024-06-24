"""
Python module that acts as a pydantic abstraction for ArgumentParser, dotenv, and configuration.json.
"""

from argparse import _ArgumentGroup, ArgumentParser
import json
import os
from typing import Any, Dict, List, Optional, Tuple
from pydantic import ConfigDict, Field
from pydotenv import Environment

from .easymodel import EasyModel


class ArgumentConfigModel(EasyModel):
    """
    Model for argument configuration
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    group: Optional[str] = Field(
        default=None, description="Group of the argument", alias="group")
    flags: List[str] = Field(
        default=[], description="Flag of the argument", alias="flags")
    name: str = Field(
        default="", description="Name of the argument", alias="name")
    argtype: Optional[type] = Field(
        default=None, title="Type of the argument", alias="type")
    required: Optional[bool] = Field(
        default=None, title="Whether the argument is required", alias="required")
    help: Optional[str] = Field(
        default=None, title="Help text for the argument", alias="help")
    action: Optional[str] = Field(
        default=None, title="Action of the argument", alias="action")
    choices: Optional[List[Any]] = Field(
        default=None, title="Choices for the argument", alias="choices")
    netavar: Optional[str | Tuple[str]] = Field(
        default=None, title="Environment variable for the argument", alias="netavar"
    )
    default: Optional[Any] = Field(
        default=None, title="Default value for the argument", alias="default")
    nargs: Optional[List[int | str]] = Field(
        default=None, title="Number of arguments for the argument", alias="nargs")


class ArgumentParserConfigModel(EasyModel):
    """
    Model for ArgumentParser configuration
    """
    prog: Optional[str] = Field(
        default=None, description="Program name", alias="prog")
    description: Optional[str] = Field(
        default=None, description="Description of the program", alias="description")
    add_help: Optional[bool] = Field(
        default=None, description="Whether to add help", alias="add_help")


class ConfigController(EasyModel):
    """
    Config controller for ArgumentParser, dotenv, and config.json
    """
    args: List[ArgumentConfigModel] = Field(default=...,
                                            title="List of argument configurations")
    parser_config: ArgumentParserConfigModel = Field(
        default=..., title="Configuration for the ArgumentParser")

    def parse(self, args: List[str]) -> Dict[str, Any]:
        """
        Parse the arguments and return the parsed arguments
        """
        parser = ArgumentParser(
            **self.parser_config.to_dict(exclude=["model_config"]))
        groups: Dict[str, _ArgumentGroup] = {}
        for group in (
            [group for group in set([arg.group for arg in list(
                self.args)]) if group is not None] if self.args else []
        ):
            groups[group] = parser.add_argument_group(title=group)
        for arg in list(self.args):
            curent_group: _ArgumentGroup | ArgumentParser = groups[
                arg.group] if arg.group is not None else parser
            curent_group.add_argument(
                *arg.flags, **arg.to_dict(exclude=["model_config", "group", "flags", "name"]))
        parsed: Dict[str, Any] = vars(parser.parse_args(args=args))
        if "env_file" in parsed.keys():
            env_file: Any | None = parsed.get("env_file")
            if env_file and os.path.exists(path=str(object=env_file or "")) and isinstance(env_file, (int, str, bytes)):
                env: List[str] = Environment(file_path=str(env_file), check_file_exists=False).items()
                env_dict: Dict[str, str] = {env[i]: env[i + 1]
                                            for i in range(0, len(env), 2)}
                for env_key, env_value in env_dict.items():
                    parsed[str(object=env_key).lower()] = env_value
                print(f"Environment loaded from {parsed.get('env_file')}")
        if "config_file" in parsed.keys():
            config_file: Any | None = parsed.get("config_file")
            if config_file and isinstance(config_file, str) and os.path.exists(path=config_file):
                with open(
                    file=config_file, mode="r", encoding="utf-8"
                ) as file:
                    cfg = json.load(file)
                    for key, value in cfg.items():
                        parsed[key] = value
                print(f"Configuration loaded from {config_file}")
        if "save_config" in parsed.keys():
            if parsed.get("save_config"):
                config_file = parsed.get("config_file")
                if config_file and isinstance(config_file, str) and os.path.exists(path=config_file):
                    os.remove(path=config_file)
                if config_file and isinstance(config_file, str):
                    with open(file=config_file, mode='w', encoding='utf-8') as file:
                        json.dump(obj=parsed, fp=file, indent=4)
                    print(f"Configuration saved to {parsed.get('config_file')}")
        return parsed
