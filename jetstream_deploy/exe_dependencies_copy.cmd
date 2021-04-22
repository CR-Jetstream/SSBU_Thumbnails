echo off 
:: Copy renders
Xcopy /E /I ..\jetstream\Resources\Character_Renders dist\Resources\Character_Renders
:: Copy fonts
Xcopy /E /I ..\jetstream\Resources\Fonts dist\Resources\Fonts
:: Copy Overlays
Xcopy ..\jetstream\Resources\Overlays\*png dist\Resources\Overlays\*png
:: Copy Top8 Graphics
Xcopy ..\jetstream\Resources\Top8_Graphics\*png dist\Resources\Top8_Graphics\*png
:: Copy databases
copy ..\jetstream\Resources\Character_database.csv dist\Resources\Character_database.csv
copy ..\jetstream\Resources\Player_database.csv dist\Resources\Player_database.csv
:: Copy Vod_Names folder
Xcopy /E /I ..\jetstream\Vod_Names dist\Vod_Names
:: Create Youtube_Thumbnails folder
mkdir dist\Youtube_Thumbnails
:: Create Top8_Graphic folder
mkdir dist\Top8_Graphic