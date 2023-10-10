import subprocess
from argparse import Namespace, ArgumentParser

from ryujinx_mako._const import NAME, GH_BOT_SUFFIX, GH_EMAIL_TEMPLATE
from ryujinx_mako.commands._subcommand import GithubSubcommand


class SetupGit(GithubSubcommand):
    @staticmethod
    def name() -> str:
        return "setup-git"

    @staticmethod
    def description() -> str:
        return f"Configure git identity for {NAME}"

    def __init__(self, parser: ArgumentParser):
        parser.add_argument(
            "-l",
            "--local",
            action="store_true",
            help="configure the git identity only for the current repository",
        )
        super().__init__(parser)

    def run(self, args: Namespace):
        base_command = ["git", "config"]
        gh_username = f"{NAME}{GH_BOT_SUFFIX}"

        self.logger.debug(f"Getting GitHub user for: {gh_username}")
        user = self.github.get_user(gh_username)
        email = GH_EMAIL_TEMPLATE.format(user_id=user.id, username=user.login)

        if args.local:
            self.logger.debug("Setting git identity for local repo...")
        else:
            self.logger.debug("Setting git identity globally...")
            base_command.append("--global")

        config = {"user.name": user.login, "user.email": email}
        for option, value in config.items():
            self.logger.info(f"Setting git {option} to: {value}")
            command = base_command.copy()
            command.extend([option, value])
            process = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            process.check_returncode()
            self.logger.info("Success!")
