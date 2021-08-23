<br>
1 - CONFIGURING RASPBERRY & PC

Tools to install to your local PC:

    arp-scan



Tools to install to raspberry before executing:

    sudo apt-get install gphoto2

    sudo apt-get install exiftool

    sudo apt-get install curl
    
    sudo apt-get install tmux
    
 
 =


Create 2 folders on raspberry:
 
 ~/Desktop/Pictures
 
 ~/Desktop/Uploaded
 
 Unzip Camera_CLI to:
 
    /home/pi/
    
 Move start_cam_stream.sh to and make it executable

    /home/pi
    chmod +x start_cam_stream.sh
 
 =
 
 Change GPS interface permission in order to prevent error: "Can't open port, permission denied":
 
    sudo chmod 666 /dev/ttyACM*
 
=

  
 Make camera.py executable:
 
    cd
    cd Camera_CLI
    sudo chmod +x camera.py
 
 =
 Open SSH port:
 
    sudo raspi-config
    => Interface options => SSH
 
 =
<br>
<br>
<br>
 
 2 - CONFIGURE
 
 *  Boot up raspberry
 *  Wait until it connects to preset wifi router
 *  Connect to the same local network with your PC
 *  Run in terminal:
 

     arp-scan -l -I <network-interface>         # en0 on Mac
 * Look for raspberry-s IP
 * Connect to raspberry. Run in terminal:
 
 
    ssh pi@<ip>
  
  * Edit start_cam_stream.sh:
  <p>1 - Add gps interface path
  
    gpspath="<path>"
  
  <p>2 - Add token
  
 
    token="<token>"






  <br>
  <br>
  <br>
  
 3 - EXECUTION
 
 TO EXECUTE the script:
 
 *  Boot up raspberry
 *  Wait until it connects to preset wifi router
 *  Connect to the same local network with your PC
 *  Run in terminal:
 

     arp-scan -l -I <network-interface>         # en0 on Mac
 * Look for raspberry-s IP
 * Connect to raspberry. Run in terminal:
 
 
    ssh pi@<ip>
  
  When connected, run in terminal:
  
  
    tmux new -s cam
    
  * Now new window is opened. You can leave this window open for the rest of the flight. 
  When wifi connection is lost, the service will keep on running and re-connects automatically when you connect to the same network again.

  * You are all set to start the camera stream.
  * START :
  * Run in tmux terminal (-p and -l are mandatory):
  
 
    cd
    
    ./start_cam_stream.sh -p <project_id> -l <power_line_name> -g <gps_interface> -t <token> 
 
 =
 
 * Camera can be turned off at any point, during the start. When camera is ON and connected and there is GPS lock, 
 then camera will start shooting with minimum time interval.
 
 * GPS must be physically connected before the execution of the script. It does not have to have a GPS lock.
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
 
 * When copter is landed, only turn off camera. Do not end the script, since it may still upload the images. 
 Wait until the terminal shows only "Camera not connected. Killing gphoto2 process.", then all the pictures have been uploaded.