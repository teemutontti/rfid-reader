"""
RFID Handler for reading and processing RFID tags using the MFRC522 module.

This class provides functionality to interact with an MFRC522 RFID reader,
including reading data from RFID tags, managing the reader reset, and
providing visual feedback via LEDs. It also includes a restart mechanism
for the system and supports custom callback functions to process the
retrieved data.

The system is built for microcontroller environments and utilizes the
machine library to interact with hardware pins. LED feedback can be controlled
using an optional LED controller.

Main Features:
- Initialization and configuration of the RFID reader.
- Tag detection and data reading from multiple sectors and blocks.
- System reset functionality.
- LED feedback during RFID reading process.
- Customizable callback function to process the read data.

Hardware Requirements:
- MFRC522 RFID reader connected via SPI.
- Optionally, an LED controller for visual feedback during reading process.

"""

from machine import Pin, SPI, I2C, reset
from mfrc522 import MFRC522
from lcd_display import LCD_Display
import time
import threading

class RFID_Handler:
    SECTORS = 16

    def __init__(self, spi=1, sck=14, mosi=15, miso=12, cs=13, rst=9, led_controller=None) -> None:
        """
        Initializes the RFID handler with the necessary pins and settings.
        
        :param spi: SPI bus identifier (default: 1).
        :param sck: SPI clock pin (default: 14).
        :param mosi: SPI MOSI pin (default: 15).
        :param miso: SPI MISO pin (default: 12).
        :param cs: SPI chip select pin (default: 13).
        :param rst: RFID reset pin (default: 9).
        :type spi, sck, mosi, miso, cs, rst: int
        :param led_controller: Optional LED controller to manage LED state (default: None).
        :type led_controller: object or None
        """
        
        self.mfrc522 = MFRC522(sck=sck, mosi=mosi, miso=miso, rst=rst, cs=cs, spi_id=1)
        self.spi_id = spi
        self.keyA = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF] # Default key for sector A
        self.keyB = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00] # Default key for sector B
        self.reset_pin = Pin(rst, Pin.OUT)
        self.leds = led_controller

    def read_data(self, callback):
        """
        Reads data from an RFID tag and processes it using a callback function.
        Provides LED feedback during the process.

        :param callback: A function to handle the read RFID data.
        :type callback: function
        """
        
        print("READING: Waiting for RFID tag...")
        
        if self.leds:
            self.leds.success.low()
            self.leds.progress.low()
            self.leds.error.low()
        
        fail_flag = False
        
        request = 0
        while True:
            start_time = time.ticks_ms()
            request += 1

            all_data = []
            read_failed = False

            (status, tag_type) = self.mfrc522.request(self.mfrc522.REQALL)
            
            if status == self.mfrc522.OK:
                if self.leds:
                    self.leds.progress.high()

                (status, uid) = self.mfrc522.SelectTagSN()

                for sector in range(1, RFID_Handler.SECTORS):
                    for block in range(3):                       

                        (status, data) = self.mfrc522.readSectorBlock(uid, sector, block, self.keyA)
                        if status == self.mfrc522.OK and data is not None:
                            all_data.extend(data) # Append the block's data
                            fail_flag = False
                        else:
                            read_failed = True
                            
                            if not fail_flag:
                                if self.leds:
                                    self.leds.progress.low()
                                    self.leds.blink(self.leds.error)
                                fail_flag = True
                                

                        if sector == 15 and block == 2:
                            if not read_failed:
                                if self.leds:
                                    self.leds.progress.low()
                                    threading.start_thread(self.leds.success.high, ())
                                callback(all_data)
                                
                                # Release the tag for the next read
                                self.mfrc522.stop_crypto1()  # This releases the tag
                                
                                # TEMPORARY:
                                reset() # Calls system reset
            
            
            time.sleep(0.2)
            elapsed_time = time.ticks_diff(time.ticks_ms(), start_time)
            print(f"Request {request} ({status}, {tag_type}) took {elapsed_time} ms", end="\r")
            
if __name__ == "__main__":
    print("This module should NOT be run directly!")
