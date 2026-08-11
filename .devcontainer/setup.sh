#!/usr/bin/env bash
# Runs once, when a Codespace is first created.
#
# Builds the course virtual environment and makes it activate automatically
# in every terminal, so that a Codespace behaves exactly like a correctly
# set up laptop - same commands, same (.venv) prompt, same check_setup.py
# result.

set -e

echo "Creating the course virtual environment..."
python3 -m venv .venv

echo "Installing the course packages..."
./.venv/bin/python -m pip install --quiet --upgrade pip
./.venv/bin/python -m pip install --quiet -r requirements.txt

# Activate it in this and every future terminal in this Codespace.
ACTIVATE="source ${PWD}/.venv/bin/activate"
if ! grep -qsF "${ACTIVATE}" "${HOME}/.bashrc"; then
    printf '\n# Course virtual environment\n%s\n' "${ACTIVATE}" >> "${HOME}/.bashrc"
fi

echo
echo "------------------------------------------------------------"
echo "Your Codespace is ready."
echo
echo "Open a new terminal and check the setup with:"
echo
echo "    python check_setup.py"
echo
echo "Your prompt should start with (.venv). If it does not, close the"
echo "terminal and open a new one."
echo "------------------------------------------------------------"
