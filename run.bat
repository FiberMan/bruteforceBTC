color 0A

:: change current directory to the batch file directory
cd /D "%~dp0"

:: create virtual environment with Python 3.13 if not already present
:: (coincurve requires Python <=3.13; install via: py install 3.13)
if not exist .venv (
    py -3.13 -m venv .venv
)

:: activate virtual environment
call .venv\Scripts\activate

:: install/update dependencies
pip install -r requirements.txt

python brute.py

cmd /k