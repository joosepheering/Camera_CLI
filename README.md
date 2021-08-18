Tools to install before executing:

    sudo apt-get install gphoto2

    sudo apt-get install exiftool

    sudo apt-get install curl


Create 2 folders:
 
 ~/Desktop/Pictures
 
 ~/Desktop/Uploaded
 
 Unzip Camera_CLI to:
 
    /home/pi/
 
 =
 
 In camera.py, change SERIAL_PORT = "/dev/ttyACM*"  for linux
 
 Search it with:
 
    ls /dev
 
 When getting error during camera.py execution: "Can't open port, permission denied" then:
 
    sudo chmod 666 /dev/ttyACM* 
 
=

 In camera.py file, modify:
 
 Add TOKEN : str. Ask it from Kuido.
 
 Change PROJECT_ID : str
 
 Change POWER_LINE_NAME : str
 
 =
 
  
 Make camera.py executable:
 
    cd
    cd Camera_CLI
    sudo chmod +x camera.py
 
 =
 
 EXECUTE the script with:
 
    cd
    cd Camera_CLI
    python3 camera.py
 
 * Camera can be turned off at any point, during the start. When camera is ON and connected and there is GPS lock, 
 then camera will start shooting with minimum time interval.
 
 * GPS must be connected before the execution of the script. It does not have to have a GPS lock.
  When it gets GPS lock, 2 red LED-s will start to blink with interval ~1Hz. 
  Then it's safe to take off, because camera will not take pictures, unless it has GPS lock.
 
 * Upload to uBird will take place if there is network connection and there are photos in the buffer that aren't uploaded yet.
 In case of network outage, the upload will stop and resume automatically, after connection is established.
 If the script is stopped and buffer includes photos that are not uploaded, the upload will start automatically during next
 execution of the script.
 
 * NB! If you change PROJECT_ID / POWER_LINE_NAME or wish to collect new batch of images, 
 make sure that the ~/Desktop/Pictures folder is empty, otherwise images this folder will be uploaded to new project/power line.
 
 * NB! Uploaded images are stored on Raspberry as well, in folder ~/Desktop/Uploaded/. 
 In case there are longer flights, this folder must be cleaned manually after the flight.
 
 