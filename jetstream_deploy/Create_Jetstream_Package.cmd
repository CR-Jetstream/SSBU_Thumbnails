echo off 
:: Create exes
call exe_create_thumbnail_py.cmd
call exe_create_top8_graphic_py.cmd
:: Copy dependencies
call exe_dependencies_copy.cmd
:: Create sample cmd scripts
call exe_cmd_sample_create.cmd
:: Create zip file
echo Compressing, this can take a couple minutes
call exe_compress.cmd
:: Remove all folders except for zip output
call exe_cleanup.cmd
:: Done
echo Jetstream_Generator.zip is created
pause