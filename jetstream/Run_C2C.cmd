echo off 
call .\venv\Scripts\activate.bat
python create_thumbnail.py -e "C2C Finale" -n "Winter 2021" -o missing.log
type missing.log
pause