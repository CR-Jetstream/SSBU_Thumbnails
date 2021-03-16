echo off 
call .\venv\Scripts\activate.bat
python create_thumbnail.py -e AWG -n Spring_Split_1 -o log_file.txt
type log_file.txt
pause