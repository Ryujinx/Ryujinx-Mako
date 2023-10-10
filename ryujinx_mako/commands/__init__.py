from typing import Type

from ryujinx_mako.commands._subcommand import Subcommand
from ryujinx_mako.commands.exec_ryujinx_tasks import ExecRyujinxTasks
from ryujinx_mako.commands.setup_git import SetupGit
from ryujinx_mako.commands.update_reviewers import UpdateReviewers

SUBCOMMANDS: list[Type[Subcommand]] = [
    SetupGit,
    UpdateReviewers,
    ExecRyujinxTasks,
]

__all__ = SUBCOMMANDS
