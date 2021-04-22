echo off 
:: Create thumbnail exe
call ..\venv\Scripts\activate.bat
pyinstaller ..\jetstream\create_thumbnail.py --onefile --name thumbnail_generator