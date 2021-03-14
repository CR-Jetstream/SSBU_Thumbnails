echo off 
call .\venv\Scripts\activate.bat
python create_thumbnail.py -e "Fro Fridays" -n 33 -o log_file.txt
type log_file.txt
pause