# hanover-flipdot-esp32
An esp32 that can drive a Hanover Flipdot display via MQTT

https://github.com/user-attachments/assets/f6e26094-01f5-4e91-84e5-9354b79c0fce

I consider myself the lucky owner of a Hanover flipdot display (that was meant to be used as a bus display). I had it running for some time within ESPHome in Home Assistant following the github code of Gareth. More information on this can be found in: https://community.home-assistant.io/t/hanover-flipdot-bus-sign-display-component/357483 and https://github.com/garethm79/hanover_flipdot_esphome. It took me some time to get it working, but in the end the esp32 pulls a predefined set of data out of Home Assistant and displays these on the display. Although it worked it has the disadvantage that it is not really flexible thereafter (unless you update the code with new sensors).

As I also have a MQTT broker running within Home Assistant, this would provide a far more flexible solution because I can send any information to the display, either via automations within Home Assistant as via any MQTT program (MQTT explorer in Windows or an app on my phone). 

Some more details about my setup:

•	Resolution: 84x8 pixels (yellow/black flipdots)

•	Address: when you open the display at the back, you can see the motherboard and there are dials on it to set the address. Mine was set to 1 (which means later on that the address will be 2, as 1 is to be added)

•	I installed the 4 files (__init__.py, display.py, hanover_flipdot.cpp, hanover_flipdot.h) from the Gareth github repository into my Home Assistant directory (/homeassistant/esphome/custom_components/hanover_flipdot/)

•	Bought a RS485 USB connector (a cheap one from Amazon)

•	I first connected the red and black communication cables that came out of the Hanover to the USB485 adapter (red to red, black to black). Furthermore, the LED display itself must be connected to the power supply (mine 24V - 2A)

•	Installed the esp32 in ESPHome/Home Assistant

•	Via file editor uploaded the two fonts (hanover6x8.ttf and pixel8.ttf) into /homeassistant/esphome/

•	One of the fonts is the standard hanover font for text, the other one (pixel8) was designed by me to be able to show icons on the display

•	After it became live, uploaded the code (hanoverflipdot.py) to the esp32

![flipdot4](https://github.com/user-attachments/assets/11d82494-78ae-4f9f-a6d1-42f22838ae37)

The hanoverflipdot.py works as follows:

•	When a simple text message is received in the mqtt-topic ‘hanoverflipdot/display’ the text is displayed on the hanover

•	You can add an icon out of my pixel8.ttf by putting the character between [ ]. In the ‘Pixel font.png’ file you can find the mapping. When you want a cloud with rain icon to be displayed, the message to be sent to mqtt is [r]. There is also a text file added (‘bitmapfont8x8.txt’) that you can use to change or add icons.

•	You can send also combinations of icons and text. For example if you need the water tap combined with text ‘Drink!’ the mqtt message should be: [k] Drink!

•	Lastly, you can send automated data from within Home Assistant. An automation example (YAML code) can be found in ‘HA MQTT automation.yaml’


https://github.com/user-attachments/assets/a992c8a6-50dc-4b98-9ae6-6f772e5b771f
