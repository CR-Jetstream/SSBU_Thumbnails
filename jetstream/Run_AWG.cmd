echo off 
call ..\venv\Scripts\activate.bat
python create_thumbnail.py -e AWG -n Spring_Split_1 -o missing.log
type missing.log
pause