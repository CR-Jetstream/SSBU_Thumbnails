echo off 
call .\venv\Scripts\activate.bat
python create_thumbnail.py -e Quarantainment -n 48 -o log_file.txt
type log_file.txt
pause