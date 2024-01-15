@echo off

rem Create virtual environment named "automate"
python -m venv automate

rem Activate the virtual environment
call automate\Scripts\activate

rem Install packages from requirements.txt
pip install -r requirements.txt

rem Deactivate the virtual environment
deactivate

