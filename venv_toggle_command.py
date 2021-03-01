"""
Script that produces the output for the parent shell to execute.

The assumption here is that the virtualenv's directory is
project_directory/.venv/

This script returns a shell command that captures the following logic:
    if the current directory doesn't match the current virtualenv, deactivate
    if the current directory is a subdirectory of a directory owning a .venv/
    directory, then:
        if there is no  virtualenv is not yet activated, activate it
"""

import os
import sys
import typing


def get_maybe_deactivate_command(
    current_directory: str,
    current_virtualenv: typing.Optional[str],
) -> str:
    if not current_virtualenv:
        return ""

    # Chop off the /.venv at the end
    project_directory = "/".join(current_virtualenv.split("/")[:-1])

    if project_directory not in current_directory:
        return "deactivate; "
    else:
        return ""


def get_project_directory(current_directory) -> typing.Optional[str]:
    nodes = current_directory.split("/")
    # due to path.split("/"), the zero-th node is "" (before the root directory)
    while len(nodes) > 1:
        current_directory = "/".join(nodes)
        current_subdirectories = [
            ls_result
            for ls_result in os.listdir(current_directory)
            if os.path.isdir(current_directory + "/" + ls_result)
        ]

        if ".venv" in current_subdirectories:
            return current_directory

        nodes.pop()

    return None


def get_project_and_command() -> str:
    output = ""

    current_directory = os.getcwd()
    current_virtualenv = os.getenv("VIRTUAL_ENV")

    deactivate_command = get_maybe_deactivate_command(
        current_directory,
        current_virtualenv,
    )

    activate_command = ""
    project_directory = get_project_directory(current_directory)
    if project_directory and not current_virtualenv:
        activate_command = f"source {project_directory}/.venv/bin/activate; "

    if project_directory:
        project_name = project_directory.split("/")[-1]
    else:
        project_name = ""

    return project_name, f"{deactivate_command}{activate_command}"


if __name__ == "__main__":
    project, command = get_project_and_command()
    if sys.argv[1] in ["-c", "--command"]:
        print(command)
    if sys.argv[1] in ["-p", "--project-name"]:
        print(project)
