#!/usr/bin/env python3
import os
import re
import subprocess
from typing import Union


def run_mako_command(command: Union[str, list[str]]) -> str:
    subprocess_cmd = ["poetry", "run", "ryujinx-mako"]

    if isinstance(command, str):
        subprocess_cmd.append(command)
    elif isinstance(command, list):
        subprocess_cmd.extend(command)
    else:
        raise TypeError(command)

    env = os.environ.copy()
    env["MAKO_DRY_RUN"] = "1"

    process = subprocess.run(
        subprocess_cmd, stdout=subprocess.PIPE, check=True, env=env
    )

    return process.stdout.decode()


def print_help(name: str, output: str, level=3):
    headline_prefix = "#" * level
    print(f"{headline_prefix} {name}\n")
    print("```")
    print(output.rstrip())
    print("```\n")


general_help = run_mako_command("--help")
for line in general_help.splitlines():
    subcommands = re.match(r" {2}\{(.+)}", line)
    if subcommands:
        break
else:
    subcommands = None

if not subcommands:
    print("Could not find subcommands in general help output:")
    print(general_help)
    exit(1)

subcommands = subcommands.group(1).split(",")

print_help("Available commands", general_help, 2)
for subcommand in subcommands:
    print_help(subcommand, run_mako_command([subcommand, "--help"]))
