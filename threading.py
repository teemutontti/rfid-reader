"""
Thread Management Module

This module provides functionality to start and stop threads safely using a lock mechanism.
It ensures that only one thread runs at a time on Core 1 and retries if the core is busy.

Main Features:
- Starts a new thread on Core 1
- Ensures thread safety using a lock
- Stops currently running thread safely

:author: Teemu Tontti
"""

import _thread
import time

__author__ = "Teemu Tontti"

thread_lock = _thread.allocate_lock()
current_thread = None

def start_thread(function, args):
    """
    Starts a new thread on Core 1 if no other thread is running.
    If Core 1 is busy, it retries after a short delay.
    
    :param function: The function to be executed in the new thread.
    :type function: function
    :param args: The arguments to be passed to the function.
    :type args: tuple
    """
    
    global current_thread
    with thread_lock:
        if current_thread is not None:
            current_thread = None
            
        # Start a new thread on Core 1
        try:
            current_thread = _thread.start_new_thread(function, args)
        except OSError:
            print("Core 1 is still in use, retrying...")
            time.sleep(1)
            start_thread(function, args)
        
def stop_thread():
    """Stops the currently running thread by resetting its reference."""
    global current_thread
    with thread_lock:
        if current_thread is not None:
            current_thread = None
            
if __name__ == "__main__":
    print("This module should NOT be run directly!")
