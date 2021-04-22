echo off 
:: Create top8 exe
call ..\venv\Scripts\activate.bat
pyinstaller ..\jetstream\create_top8_graphic.py --onefile --name top8_generator