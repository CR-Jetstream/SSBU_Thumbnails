echo off 
:: Create exes
call create_thumbnail_exe.cmd
call create_top8_graphic_exe.cmd
:: Copy Resources folder
if not exist dist\Resources (
	call exe_resources_copy.cmd
) else (
	echo Resources folder already exists
)
:: Copy cmd scripts
call exe_cmd_copy.cmd
:: Create zip file
echo Compressing, this will take a minute
call exe_compress.cmd
:: Remove all folders except for zip output
::call exe_cleanup.comd