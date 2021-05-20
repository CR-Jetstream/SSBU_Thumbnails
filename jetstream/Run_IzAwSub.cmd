echo off 
call ..\venv\Scripts\activate.bat
python create_thumbnail.py -e "IzAw Sub" -n "Random" -o missing.log
type missing.log
pause