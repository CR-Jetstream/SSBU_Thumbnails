echo off 
call .\venv\Scripts\activate.bat
python create_thumbnail.py -e "Catman" -n "Invitational" -o missing.log
type missing.log
pause