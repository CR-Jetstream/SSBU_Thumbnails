echo off 
Xcopy /E /I Resources\Character_Renders dist\Resources\Character_Renders
Xcopy /E /I Resources\Fonts dist\Resources\Fonts
Xcopy Resources\Top8_Graphics\*png dist\Resources\Top8_Graphics\*png
Xcopy Resources\Overlays\*png dist\Resources\Overlays\*png
copy Resources\Character_database.csv dist\Resources\Character_database.csv
copy Resources\Player_database.csv dist\Resources\Player_database.csv