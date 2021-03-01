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

**Q:** Why do we use `PROMPT_COMMAND`? Wouldn't it be easier if `virtualenv_info` just
executed `auto_virtualenv` for us?

**A:** That would be cleaner. However, `$(...)` (known as command substitution)
executes the command in a subshell. If we `source bin/activate` in a subshell,
the modifications done in `bin/activate` would not be reflected in the shell
that we're working in. As far as I know, there's no way for bash to evaluate
the `$()` calls inside the `PS1` string in the current shell.
