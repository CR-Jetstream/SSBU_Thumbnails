echo off 
call ..\venv\Scripts\activate.bat
python create_thumbnail.py -e "Students x Treehouse" -n 17 -o missing.log
type missing.log
pause