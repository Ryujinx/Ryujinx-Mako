from argparse import ArgumentParser, Namespace
from pathlib import Path
from github.Repository import Repository
from github.GithubException import GithubException

import yaml

from ryujinx_mako.commands._subcommand import GithubSubcommand


class UpdateReviewers(GithubSubcommand):
    @staticmethod
    def name() -> str:
        return "update-reviewers"

    @staticmethod
    def description() -> str:
        return "Update reviewers for the specified PR"

    def __init__(self, parser: ArgumentParser):
        self._reviewers = set()
        self._team_reviewers = set()

        parser.add_argument("repo_path", type=str)
        parser.add_argument("pr_number", type=int)
        parser.add_argument("config_path", type=Path)

        super().__init__(parser)

    def add_reviewers(self, new_entries: list[str]):
        for reviewer in new_entries:
            if reviewer.startswith("@"):
                self._team_reviewers.add(reviewer[1:])
            else:
                self._reviewers.add(reviewer)

    def update_reviewers(self, config, repo: Repository, pr_number: int) -> int:
        pull_request = repo.get_pull(pr_number)

        if not pull_request:
            self.logger.error(f"Unknown PR #{pr_number}")
            return 1

        if pull_request.draft:
            self.logger.warning("Not assigning reviewers for draft PRs")
            return 0

        pull_request_author = pull_request.user.login

        for label in pull_request.labels:
            if label.name in config:
                self.add_reviewers(config[label.name])

        if "default" in config:
            self.add_reviewers(config["default"])

        if pull_request_author in self._reviewers:
            self._reviewers.remove(pull_request_author)

        try:
            reviewers = list(self._reviewers)
            team_reviewers = list(self._team_reviewers)
            self.logger.info(
                f"Attempting to assign reviewers ({reviewers}) "
                f"and team_reviewers ({team_reviewers})"
            )
            pull_request.create_review_request(reviewers, team_reviewers)
            return 0
        except GithubException:
            self.logger.exception(f"Cannot assign review request for PR #{pr_number}")
            return 1

    def run(self, args: Namespace):
        repo = self.github.get_repo(args.repo_path)

        if not repo:
            self.logger.error("Repository not found!")
            exit(1)

        if not args.config_path.exists():
            self.logger.error(f"Config '{args.config_path}' not found!")
            exit(1)

        with open(args.config_path, "r") as file:
            config = yaml.safe_load(file)

        exit(self.update_reviewers(config, repo, args.pr_number))