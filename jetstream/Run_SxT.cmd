echo off 
call ..\venv\Scripts\activate.bat
python create_thumbnail.py -e "Students x Treehouse" -n 19 -o missing.log
type missing.log
pause