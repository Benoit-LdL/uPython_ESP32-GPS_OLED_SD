import uos
import machine
import utime

#OLED
import ssd1306
import gfx
from writer.writer_minimal import Writer
from writer import arial35

#GPS
from micropyGPS import MicropyGPS
import _thread
##################__VARS__###################
#############################################
debugCounter = 0
threadCounter = 0
vMax = 0

#OLED
i2c = machine.SoftI2C(scl=machine.Pin(22),sda=machine.Pin(23))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
graphics = gfx.GFX(oled_width, oled_height, oled.pixel)

#GPS
gps = MicropyGPS(+2)
buf = ""
SentenceCounter = 0
uart = machine.UART(1,rx=16, tx=17, baudrate=9600, bits=8, parity=None, stop=1, timeout=5000, rxbuf=1024)

#SD
# sd_available = False
# sd = machine.SDCard(sck=machine.Pin(5),
#       mosi=machine.Pin(18),
#       miso=machine.Pin(19),
#       cs=machine.Pin(4))

###########__METHODS & FUNCTIONS__###########
#############################################
def GPS_Icon(gpsRadius,gpsX,gpsY,gpsLineLenght):
   global graphics
   graphics.circle(gpsX,gpsY,gpsRadius,1)
   graphics.fill_circle(gpsX,gpsY,int(gpsRadius/3),1)
   graphics.line(gpsX,gpsY-gpsRadius,gpsX,gpsY-gpsRadius-gpsLineLenght,1) #VerUp
   graphics.line(gpsX,gpsY+gpsRadius,gpsX,gpsY+gpsRadius+gpsLineLenght,1) #VerDown
   graphics.line(gpsX-gpsRadius-gpsLineLenght,gpsY,gpsX-gpsRadius,gpsY,1) #HorLeft
   graphics.line(gpsX+gpsRadius,gpsY,gpsX+gpsRadius+gpsLineLenght,gpsY,1) #HorRdown

def GPSThread():
   global gps
   global SentenceCounter
   global buf
   global vMax
   gpsSystem = ""
   gpsSentence = ""

   while True:
      #print("Thread")
      #Read Raw data from GPS and parse it
      buf = uart.readline()
      #print(buf)

      #Only  read GGA and RMC sentences because these contain all necessary data
      bufStr = str(buf)
      gpsSystem = bufStr[3:5]
      gpsSentence = bufStr[5:8]
      
      #print(bufStr)

      #if gpsSentence == "GGA" or gpsSentence == "RMC":
      for char in buf:
         gps.update(chr(char))
         
      #print(bufStr)
      if vMax < round(gps.speed[2],1):
         vMax = round(gps.speed[2],1)
      SentenceCounter +=1 

def MountSD():
    global sd_available
    global sd
    
    # sd mount
    try:
        uos.mount(sd, '/sd')
        print("SD Card mounted")
        sd_available = True
    except:
        print("Error, unmountable SD card!")
        sd_available = False

    # if Sd card is available, write to it
    if sd_available:
        # Create GPS files
        print("Writing...")

        f = open('sd/_GPS_RAW_NMEA.txt', 'a')
        f.write("\n---------------------------------------")
        f.write("\n####__RAW NMEA SENTENCES FROM GPS__####")
        f.write("\n---------------------------------------")
        f.close()

        f = open('sd/_GPS_DATA.txt', 'a')
        f.write("\n---------------------------------------------")
        f.write("\n################__GPS Data__#################")
        f.write("\n---------------------------------------------")
        f.write("\nDate | Time | #Sats | Fix | Speed | Lat | Lon")
        f.write("\n---------------------------------------------")
        f.close()

        utime.sleep(0.1)
        print("Saved")     
           
#############################################
#print(uos.uname())

#print('Scan i2c bus...')
#devices = i2c.scan()

#Check I2C devices
#while len(devices) == 0:
#  print("No i2c device !")
#  utime.sleep(1)
#  devices = i2c.scan()

#print('i2c devices found:',len(devices))
#for device in devices:  
#   print("Decimal address: ",device," | Hexa address: ",hex(device))
#############################################

#Mount SD card
#MountSD()

sd = machine.SDCard(sck=machine.Pin(5),
   	mosi=machine.Pin(18), 
      miso=machine.Pin(19),
      cs=machine.Pin(36))

uos.mount(sd, '/sd')
uos.listdir('/sd')
uos.umount('/sd')

#Starting Thread
print("Starting Thread...")
_thread.start_new_thread(GPSThread,())
print("Done.")

while True:
   oled.fill(0)


   wri = Writer(oled, arial35, verbose=False)
   Writer.set_textpos(18,38)# In case a previous test has altered this
   wri.printstring(str(round(gps.speed[2],1)))

   ######################################################################################
   #Green Oled
   ######################################################################################
   #Show # Sats
   if(gps.satellites_in_use > 9):
      oled.text("+",0,4)   
   else:
      oled.text(str(gps.satellites_in_use),0,4)
    
   #Draw GPS Icon
   GPS_Icon(gpsRadius=5,gpsX=16,gpsY=0+int(((5*2)+(2*2))/2),gpsLineLenght=2)
    
    
   #Show Fix
   if(gps.fix_type > 1):
      oled.text("Fixed",40,4)
   elif(gps.fix_type == 1):
      oled.text("No Fx",40,4)
   else:
      oled.text("0?",45,4)
    
   #Show time
   if len(str(gps.timestamp[1])) == 2:
      oled.text(str(gps.timestamp[0]) + "H" + str(gps.timestamp[1]),89,4)
   else:
      oled.text(str(gps.timestamp[0]) + "H0" + str(gps.timestamp[1]),89,4)
   ######################################################################################
   #Blue Oled
   ######################################################################################
   #Show Speed
   #oled.text(str(round(gps.speed[2],1)),0,28)
   
    
   #Show max speed
   oled.text("Vmx:" + str(vMax),0,56)

   #show gps thread counter
   if(SentenceCounter >= 99):
      SentenceCounter = 0
   
   oled.text(str(SentenceCounter),90,56)  
    
   #show counter for oled freeze
   if(debugCounter == 10):
      debugCounter = 0

   oled.text(str(debugCounter),121,56)    

   debugCounter += 1
   oled.show()
   #print("Hello World")
   utime.sleep(0.5)