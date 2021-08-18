Tools to install before executing:

    sudo apt-get install gphoto2

    sudo apt-get install exiftool

    sudo apt-get install curl


Create 2 folders:
 
 ~/Desktop/Pictures
 
 ~/Desktop/Uploaded
 
 =
 
 Change SERIAL_PORT = "/dev/ttyACM*"  for linux
 
 When getting error: "Can't open port, permission denied" then -> sudo chmod 666 /dev/ttyACM* 
 
=
 
 In camera.py file, modify:
 
 Add Token. Ask it from Kuido.
 
 Change PROJECT_ID
 
 Change POWER_LINE_NAME
 