echo off 
:: Create exe
call .\venv\Scripts\activate.bat
pyinstaller create_thumbnail.py --onefile --name thumbnail_generator
:: Copy resources to dist folder where exe lives
if not exist Resources (
	call exe_resources_copy.cmd
)
else (
echo Resources folder already exists
)
pause