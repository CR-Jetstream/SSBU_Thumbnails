echo off 
call ..\venv\Scripts\activate.bat
python create_thumbnail.py -e "AWG Just Tech It 5!" -o missing.log
type missing.log
pause