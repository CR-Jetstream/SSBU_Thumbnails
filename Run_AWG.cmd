echo off 
call .\venv\Scripts\activate.bat
python create_thumbnail.py -e AWG -n Winter_Split_5 -o log_file.txt
type log_file.txt
pause