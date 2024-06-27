# Sample python command line app with developer environment and continuous integration

This repository demonstrates an opinionated setup for a python command line app. It shows how to

- configure the VS Code IDE for easy  python3 based development, including testing and linting
- a docker based development environment
- package management and python version tooling
- continuous integration using GitHub including unit tests and code coverage
- packaging and building the python CLI app ready for distribution
- Use pre-commit hooks

Built using a combination of https://github.com/alastairtree/python-cli-devenv-and-ci-sample and https://github.com/ImperialCollegeLondon/poetry_template . Thanks Alastair Crabtree and the computer research team at Imperial!
# Jupyter Notebooks and ipytest
Follow the README in notebooks/ to also view a good practice jupyter notebook, including ipytest integration for testing with the notebook environment

## Developer Quick start

- install vs code and docker (tested on windows with WSL2 and docker desktop)
- clone the repository
- open the repo in vscode and switch to the dev container (CTRL-P -> Reopen in dev container)
- open a terminal and run `poetry install` to restore dependencies
- run the code within poetry in a virtual environment: `poetry run demo hello bob`
- or run the code with python3 in a virtual environment: `poetry shell` and `poetry install` to setup env and then `python3 src/main.py hello alice` or even just `demo hello charlie` works because the command is actually installed in the virtual env.
- One click to run the tests and generate coverage: `./build.sh`
- One click to package the app into the /dist folder: `./pack.sh`
- One click to run the tests and package the app across multiple versions of python 3.9, 3.10, 3.11 etc: `./build-all.sh`

## How to install and use the tool

See `install.sh`.

- Download the tar from the GitHub Actions build artifacts (could also use the wheel (.whl) if you prefer)
- Install pipx (not required but this ensures the tool is installed in it's own environment and dependencies cannot make a mess of your system)
- [Install it with pipx](https://pypa.github.io/pipx/docs/#pipx-install) `pipx install --python some-version path-to-tar` (or with pip if you must).
- Run `demo hello world` on the command line to check it installed ok

## IDE, Docker, Python

The app uses VS code with docker the devcontainers feature to setup a python environment with all tools preinstalled. All you need is vscode and docker to be able develop.

## Python command line app using typer

This repo publishes to the `/dist` folder a python wheel (.whl) and tar containing a CLI executable called `demo` that can be installed and run. This app uses the library typer to produce a user friendly interactive cli

## Tools - poetry, pyenv, isort, flake8, black

All these tools are preinstalled in the dev container:

- **Python3** - multiple versions installed and available, managed using pyenv
- **Poetry** - tool to manage python dependencies, tools and package
- **isort, black and flake8** - configured to lint and tidy up your python code automatically. Executed using ./build.sh and CTRL+SHIFT+B (build in vscode)

## Testing - pytest, code coverage

The project shows how to create unit test.

Either use the test runner in vscode (with debugging)

Or on the cli using pytest:

```
$ pytest

# or a subset of tests
$ pytest tests/test_main.py
$ pytest -k hello
```

The tests can be run:

- from inside vscode using the Testing window
- from the CLI against the current and multiple python versions (See quick start)
- In GitHub actions on every check-in

Test reports appear automatically in the github actions report

Code coverage data is generated on build into the folder `htmlcov`


## Continuous Integration with GitHub Actions

The `.github/workflows/ci.yml` define a workflow to run on build and test the CLI against multiple versions of python. Build artifacts are generated and a copy of the cli app is available for download for every build

## Pre-commit hooks
Pre-commit hooks will stop you from committing files that do not follow flake8 and black, amongst other things. I've added some common hooks. Check them out in .pre-commit-config.yaml. If you try to commit something naughty you will be prompted to fix it. Try it out by trying to commit a notebook without clearning the output.

Test your pre-commit hooks are working with:
```
$  pre-commit run --all-files
```

I had some issues getting the pre-commit hooks working. It was fixed with:
```
git config --local core.hooksPath .git/hooks
```
This tells git where the hooks are explicity.

## Want to know more?

Check out the [Tour](Tour.md)

## Troubleshooting

Make sure you have opened the folder in VS Code with Dev Containers.

Reinstall everything by re-running instal script (done for you in dev container init is using vscode)

```
./dev-env-first-time.sh
```

Check the tools are on the path and work:

```
$ poetry --version
Poetry (version 1.3.2)

# also you can update it
$ poetry self update
```

Start a shell (this creates a virtual env for you automatically) with the tools we need available. vscode may do this automagically when you spawn a terminal.

```
$ poetry shell
```

Restore dependencies

```
$ poetry install
```

and now you can run tools on the cli such as

```
pytest
flake8
black src
```

You may need to tell vscode to use your python venv: CTRL+P `Python: select Interpreter` and select the python in the `.venv/bin/python3` folder


Try changing from zsh to bash shell.

You made have to give the dev-env-first-time.sh exec permeisssions with:
```
 chmod +x dev-env-first-time.sh
```
if you get permission denied
### SSH keys issues

You may have issues with git keys not being forwarded to the dev container. Make sure ssh-agent is running. I had a lot of trouble with this!


In Vscode dev-container documentation they explain how to use SSH agent to pass the shh keys to the container:

[vscode](https://code.visualstudio.com/docs/devcontainers/containers#_using-ssh-keys)

first find they keys files that you have on your system. To do that run the following in your WSL terminal (e.g. Ubuntu) ls ~/.ssh/. By default the shh key file name start with a id_. look for such a file (e.g. id_ed25519).

In the terminal run eval "$(ssh-agent -s)". Then run ssh-add ~/.ssh/id_ed25519 (replace the file name with your key file).

BTW to list the already added keys, run ssh-add -l

The problem is that in linux the ssh-agent doesn't start automatically on start up. So we need to add it to ~/.bash_profile file.

In the terminal run code ~/.bash_profile to open the file in vscode. Then add the following to the file:
```
if [ -z "$SSH_AUTH_SOCK" ]; then
   # Check for a currently running instance of the agent
   RUNNING_AGENT="`ps -ax | grep 'ssh-agent -s' | grep -v grep | wc -l | tr -d '[:space:]'`"
   if [ "$RUNNING_AGENT" = "0" ]; then
        # Launch a new instance of the agent
        ssh-agent -s &> $HOME/.ssh/ssh-agent
   fi
   eval `cat $HOME/.ssh/ssh-agent`
   ssh-add ~/.ssh/id_ed25519
fi
```
