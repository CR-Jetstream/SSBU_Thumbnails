echo off 
call .\venv\Scripts\activate.bat
python create_thumbnail.py -e "Students x Treehouse" -n 11 -o log_file.txt
type log_file.txt
pause