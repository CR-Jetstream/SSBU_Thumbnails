The purpose of this folder is to create a deployable zip package for the jetstream applications.

This uses pyinstaller to create the executables

Run Create_Jetstream_Package.cmd to create a zip package.
The other cmd scipts are helper scripts that do specific tasks done in the all_build script

Using Create_Jetstream_Package.cmd, the following is done
* Create the executables from the python code
* Copy dependencies to this location (Resources, Vod_Names, Youtube_Thumbnail, Top8_Graphic)
* Create cmd scripts to run the executables with proper command line arguments
* Zip up contents into a release package
* Delete all files created and copied to this directory (does not include release package)

