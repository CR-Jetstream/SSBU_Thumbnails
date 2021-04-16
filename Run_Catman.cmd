echo off 
call .\venv\Scripts\activate.bat
python create_thumbnail.py -e "Catman" -n "Invitational" -o log_file.txt
type log_file.txt
pause