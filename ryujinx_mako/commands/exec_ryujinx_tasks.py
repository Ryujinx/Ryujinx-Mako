import json
import os
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any

from github.Repository import Repository
from github.WorkflowRun import WorkflowRun

from ryujinx_mako.commands._subcommand import GithubSubcommand


class ExecRyujinxTasks(GithubSubcommand):
    @staticmethod
    def name() -> str:
        return "exec-ryujinx-tasks"

    @staticmethod
    def description() -> str:
        return "Execute all Ryujinx tasks for a specific event"

    # noinspection PyTypeChecker
    def __init__(self, parser: ArgumentParser):
        self._workspace: Path = None
        self._repo: Repository = None
        self._workflow_run: WorkflowRun = None
        self._event: dict[str, Any] = None
        self._event_name: str = None

        parser.add_argument(
            "--event-name",
            type=str,
            required=True,
            help="the name of the event that triggered the workflow run",
        )
        parser.add_argument(
            "--event-path",
            type=str,
            required=True,
            help="the path to the file on the runner that contains the full "
            "event webhook payload",
        )
        parser.add_argument(
            "-w",
            "--workspace",
            type=Path,
            required=False,
            default=Path(os.getcwd()),
            help="the working directory on the runner",
        )
        parser.add_argument(
            "repo_path",
            type=str,
            help="full name of the GitHub repository (format: OWNER/REPO)",
        )
        parser.add_argument(
            "run_id",
            type=int,
            help="The unique identifier of the workflow run",
        )
        super().__init__(parser)

    def update_reviewers(self):
        # Prepare update-reviewers
        self.logger.info("Task: update-reviewers")
        args = Namespace()
        args.repo_path = self._repo.full_name
        args.pr_number = self._event["number"]
        args.config_path = Path(self._workspace, ".github", "reviewers.yml")
        # Run task
        self.get_subcommand("update-reviewers").run(args)

    def run(self, args: Namespace):
        self.logger.info("Executing Ryujinx tasks...")

        self._workspace = args.workspace
        self._repo = self.github.get_repo(args.repo_path)
        self._workflow_run = self._repo.get_workflow_run(args.run_id)
        self._event_name = args.event_name
        with open(args.event_path, "r") as file:
            self._event = json.load(file)

        if args.event_name == "pull_request_target":
            self.update_reviewers()

        self.logger.info("Finished executing Ryujinx tasks!")
