echo off 
call ..\venv\Scripts\activate.bat
python create_thumbnail.py -e Quarantainment -n 81 -o missing.log
type missing.log
pause