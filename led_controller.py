"""
LED Controller Module

This module provides a class to control LED indicators for success, progress, and error
states using a Raspberry Pi Pico.

:author: Teemu Tontti
"""

from machine import Pin
import time

__author__ = "Teemu Tontti"

class LED_Controller:
    """
    A class to manage LED indicators for different statuses.
    """
    
    def __init__(self, success=8, progress=6, error=7) -> None:
        """
        Initializes the LED_Controller with the specified GPIO pins.
    
        :param success: GPIO pin for the success LED (default: 8).
        :param progress: GPIO pin for the progress LED (default: 6).
        :param error: GPIO pin for the error LED (default: 7).
        :type success, progress, error: int
        """
        
        self.success = Pin(success, Pin.OUT)
        self.progress = Pin(progress, Pin.OUT)
        self.error = Pin(error, Pin.OUT)
        self.__initialize()
        
    def __initialize(self):
        """
        Runs an initialization sequence by turning each LED on and off in sequence.
        """
        
        for x in range(2):
            print(x)
            for led in [self.success, self.progress, self.error]:
                led.high() if x == 0 else led.low()
                time.sleep(0.05)
        
    def blink(self, led, wait_time=0.5, times=1):
        """
        Blinks the specified LED a given number of times.
        
        :param led: The LED Pin object to blink.
        :type led: Pin
        :param wait_time: Time in seconds to wait between toggles (default: 0.5s).
        :type wait_time: float
        :param times: Number of times to blink the LED (default: 1).
        :type times: int
        """
        
        for i in range(times):
            led.high()
            time.sleep(wait_time)
            led.low()
            
            if i < times:
                time.sleep(wait_time)
                
if __name__ == "__main__":
    print("This module should NOT be run directly!")
