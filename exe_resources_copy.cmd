echo off 
Xcopy /E /I Resources\Character_Renders dist\Resources\Character_Renders
Xcopy /E /I Resources\Fonts dist\Resources\Fonts
copy Resources\Character_database.csv dist\Resources\Character_database.csv
copy Resources\Player_database.csv dist\Resources\Player_database.csv