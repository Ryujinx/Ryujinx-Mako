import logging
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Any

from github import Github
from github.Auth import AppAuth

from ryujinx_mako._const import (
    APP_ID,
    PRIVATE_KEY,
    INSTALLATION_ID,
    SCRIPT_NAME,
    IS_DRY_RUN,
)


class Subcommand(ABC):
    _subcommands: dict[str, Any] = {}

    @abstractmethod
    def __init__(self, parser: ArgumentParser):
        parser.set_defaults(func=self.run)

    @property
    def logger(self):
        return logging.getLogger(SCRIPT_NAME).getChild(
            type(self).name().replace("-", "_")
        )

    @abstractmethod
    def run(self, args: Namespace):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def name() -> str:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def description() -> str:
        raise NotImplementedError()

    @classmethod
    def get_subcommand(cls, name: str):
        return cls._subcommands[name]

    @classmethod
    def add_subcommand(cls, name: str, subcommand):
        if name in cls._subcommands.keys():
            raise ValueError(f"Key '{name}' already exists in {cls}._subcommands")
        cls._subcommands[name] = subcommand


class GithubSubcommand(Subcommand, ABC):
    _github = (
        Github(auth=AppAuth(APP_ID, PRIVATE_KEY).get_installation_auth(INSTALLATION_ID))
        if not IS_DRY_RUN
        else None
    )

    @property
    def github(self):
        return type(self)._github
