# Auto `virtualenv`

I'm so confused why there's no existing utility to automatically activate and
deactivate virtual environments.

```
# ~/.bashrc

auto_virtualenv() {
    command=$(python3 ~/auto-virtualenv/venv_toggle_command.py --command)
    eval $command
}

virtualenv_info() {
    project_name=$(python3 ~/auto-virtualenv/venv_toggle_command.py --project-name)
    if [[ -n $project_name ]]; then
        echo "($project_name) "
    fi
}

export VIRTUAL_ENV_DISABLE_PROMPT=1
export PROMPT_COMMAND=auto_virtualenv
export PS1="\$(virtualenv_info) ~> "
```
