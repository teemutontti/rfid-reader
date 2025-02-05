"""
LCD Display Manager

This module provides a class to interface with a standard 16x2 LCD display using
a 4-bit parallel connection. It includes methods for initializing the display,
sending commands and data, setting the cursor position, displaying text (including
handling (not supporting) Nordic characters), and scrolling long text messages.

Author: Teemu Tontti
"""

from machine import Pin
import time

__author__ = "Teemu Tontti"

class LCD_Display:
    """A class to interface with a standard 16x2 LCD display using a 4-bit parallel connection."""
    
    CYCLE_SPEED = 0.5
    DEFAULT_WAIT = 2

    def __init__(self, RS=22, E=21, D4=17, D5=18, D6=19, D7=20) -> None:
        """
        Initializes the LCD display with the given GPIO pin configuration.
        
        :param RS: Register Select pin
        :param E: Enable pin
        :param D4, D5, D6, D7: Data pins for 4-bit communication
        :type RS, E, D4, D5, D6, D7: int
        """
        
        self.RS = Pin(RS, Pin.OUT)
        self.E = Pin(E, Pin.OUT)
        self.D4 = Pin(D4, Pin.OUT)
        self.D5 = Pin(D5, Pin.OUT)
        self.D6 = Pin(D6, Pin.OUT)
        self.D7 = Pin(D7, Pin.OUT)
        self.lcd_init()

    def lcd_command(self, cmd):
        """
        Sends a command to the LCD.

        :param cmd: The command to be sent
        :type cmd: int
        """
        
        self.RS.value(0)
        self.write_lcd(cmd)

    def lcd_data(self, data):
        """
        Sends data to the LCD.

        :param data: The data to be sent
        :type data: int
        """
        
        self.RS.value(1)
        self.write_lcd(data)

    def write_lcd(self, value):
        """
        Writes a value to the LCD by splitting it into high and low nibble.

        :param value: The value to be written
        :type value: int
        """
        
        self.D4.value((value >> 4) & 1)
        self.D5.value((value >> 5) & 1)
        self.D6.value((value >> 6) & 1)
        self.D7.value((value >> 7) & 1)

        self.pulse_enable()

        self.D4.value(value & 1)
        self.D5.value((value >> 1) & 1)
        self.D6.value((value >> 2) & 1)
        self.D7.value((value >> 3) & 1)

        self.pulse_enable()

    def pulse_enable(self):
        """
        Pulses the Enable pin to trigger the LCD to read the data.

        This function ensures that the LCD registers the command or data sent.
        """
        
        self.E.value(1)
        time.sleep_us(1)
        self.E.value(0)
        time.sleep_us(100)

    def lcd_init(self):
        """
        Initializes the LCD with basic settings such as display on, cursor off,
        and 4-bit communication mode.
        """
        
        time.sleep_ms(15)  # Wait for the LCD to power up
        self.lcd_command(0x33)  # Initialize in 8-bit mode
        self.lcd_command(0x32)  # Switch to 4-bit mode

        # Configure for display with two lines (0x20 for 1 line, 0x28 for 2 lines)
        self.lcd_command(0x28)

        self.lcd_command(0x0C)  # Display ON, Cursor OFF
        self.lcd_command(0x06)  # Move cursor right
        self.lcd_command(0x01)  # Clear display

    def lcd_set_cursor(self, line, col):
        """
        Sets the cursor to the specified line and column.

        :param line: The line number (1 or 2)
        :param col: The column number (0 to 15)
        :type line, col: int
        """
        
        if line == 1:
            addr = 0x80 + col  # Line 1 start address (0x80)
        elif line == 2:
            addr = 0xC0 + col  # Line 2 start address (0xC0)
        self.lcd_command(addr)

    def lcd_string(self, first_line: str, second_line: str = ""):
        """
        Displays text on the LCD, with optional second line.

        :param first_line: The text for the first line
        :param second_line: The text for the second line (default is empty)
        :type first_line, second_line: str
        """
        
        self.lcd_set_cursor(1, 0)
        for char in first_line:
            self.lcd_data(ord(char))

        if len(second_line) > 0:
            self.lcd_set_cursor(2, 0)
            for char in second_line:
                self.lcd_data(ord(char))

    def check_for_nordics(self, string: str) -> str:
        """
        Converts Nordic characters (e.g., Ä, Ö, Å) to compatible characters.

        :param string: The string to check for Nordic characters
        :return: The modified string with Nordic characters replaced
        :rtype: str
        """
        
        new_string = ""
        for char in string:
            if char == "Ä":
                new_string += "A"
            elif char == "ä":
                new_string += "a"
            elif char == "Ö":
                new_string += "O"
            elif char == "ö":
                new_string += "o"
            elif char == "Å":
                new_string += "A"
            elif char == "å":
                new_string += "a"
            else:
                new_string += char
        return new_string

    def scroll_content(self, string: str, scroll_count: int):
        """
        Scrolls the given string across the LCD screen.

        :param string: The string to scroll
        :param scroll_count: The number of times to scroll the text
        :type string: str
        :type scroll_count: int
        """
        
        indices = 0, 16
        string = string + " " + string

        for scroll in range(scroll_count):
            for index in range(len(string) - 15):  # Loop past the end of the string for smooth scrolling
                # Display the string segment
                self.lcd_string(string[indices[0]:indices[1]])

                # Appending index
                indices = indices[0] + 1, indices[1] + 1

                # Sleep for a smoother scroll effect
                time.sleep(LCD_Display.CYCLE_SPEED)
            indices = 0, 16


        self.lcd_command(0x01)  # Clear display

    def print(self, content: str, scroll_count: int = 1):
        """
        Prints content to the LCD, scrolling if necessary.

        :param content: The content to display
        :param scroll_count: The number of scrolls if content exceeds 16 characters
        :type content: str
        :type scroll_count: int
        """
        
        try:
            content = self.check_for_nordics(content)
            if len(content) > 16:
                self.scroll_content(content, scroll_count)
            else:
                self.lcd_string(content)
                time.sleep(LCD_Display.DEFAULT_WAIT)

        except (Exception, KeyboardInterrupt, TypeError) as e:
            print(e)
            self.lcd_command(0x01) # Clear display on intertupt or exception
            
if __name__ == "__main__":
    print("This module should NOT be run directly!")
    
