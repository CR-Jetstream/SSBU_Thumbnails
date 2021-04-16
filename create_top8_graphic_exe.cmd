echo off 
:: Create exe
call .\venv\Scripts\activate.bat
pyinstaller create_top8_graphic.py --onefile --name top8_generator
:: Copy resources to dist folder where exe lives
if not exist Resources (
	call exe_resources_copy.cmd
)
else (
echo Resources folder already exists
)
pause