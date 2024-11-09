@echo off
echo Initializing virtual environment and installing dependencies...
echo:

if not exist .venv (
    python -m venv .venv
    call .venv\Scripts\activate
) else (
    echo .venv directory already exists, skipping virtual environment setup!
)
call .venv\Scripts\activate
pip install -r requirements.txt
