# uPython_ESP32-GPS_OLED_SD

## Goal

Use a ESP32 together with a Oled screen, a GPS module and a SD card module to read, sotre and show GPS data to the user.

## Functionality of project

* Connect to and read data from GPS module
* Show data on Oled screen

## To-DO List

* Add SD card to save NMEA sentences and other info
* Create webpage on which we can access the stored NMEA data
  * Showing data from SD card is easy
  * Showing a map on which every point is plotted whould be amazing
  
## Hardware

* Adafruit Huzzah32 (ESP32 board)
  -> Tried to use the ESP32-CAM before was extremely painfull to work with....
* Neo-6M GPS module, Neo-M8N is way slower to fix on statelites. I got both from AliExpress so they are probably fake.
* 128x64 pixel I2C Oled screen
* SD card module (3.3v compatible!)

## Software

* I installed uPython as explained [here](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)
