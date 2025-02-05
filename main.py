"""
RFID Data Handler
=================

This module reads RFID data, converts it to ASCII, and displays it on an LCD screen.
It also manages LED indicators to signal different states.

Modules:
    - lcd_display: Handles LCD screen operations.
    - rfid_handler: Reads data from an RFID scanner.
    - led_controller: Controls LED indicators.
    - machine: Provides access to hardware-related functionalities (Pin control).

Usage:
    Run this module to start reading RFID data and displaying it on the LCD.
"""

from lcd_display import LCD_Display
from rfid_handler import RFID_Handler
from led_controller import LED_Controller
from machine import Pin

led_controller = LED_Controller()

def convert_hex_to_ASCII_string(data):
    """
    Converts a list of hexadecimal values to an ASCII string, ignoring null (0) values.
    
    :param data: List of integers representing ASCII character codes.
    :type data: list[int]
    :return: Converted ASCII string.
    :rtype: str
    """
    
    return "".join(chr(value) for value in data if value != 0)

def handle_data(data):
    """
    Handles RFID data processing and displays it on an LCD screen.
    
    :param data: List of hexadecimal values from the RFID tag.
    :type data: list[int]
    """
    
    try:
        display = LCD_Display()
        
        # Turn on LCD backlight
        lcd_led_pin = Pin(28, Pin.OUT)
        lcd_led_pin.value(1)
        
        # Convert data to ASCII and display it
        ascii_data = convert_hex_to_ASCII_string(data)
        display.print(ascii_data)
        display.lcd_init()
        
    except Exception as e:
        print(f"Display error: {e}")

def main():
    """Main function that initializes the RFID handler and starts reading data."""
    try:
        rfid_handler = RFID_Handler(led_controller=led_controller)
        rfid_handler.read_data(handle_data)
        
    except Exception as e:
        print(f"RFID error: {e}")

if __name__ == "__main__":
    main()
