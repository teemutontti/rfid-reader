# RFID Reader - Raspberry Pi Pico

This repository contains the code for a Raspberry Pi Pico project that utilizes an RFID reader (RC522) and displays the corresponding data on an LCD display. The project is designed to read RFID tags and show the tag's data in ASCII letters on a 16x2 LCD display.

![IMG20250206005514](https://github.com/user-attachments/assets/338e595d-b9d7-451e-88a1-fe2f7cfb9f18)
*The current (not pretty) setup. The goal of this project is to **design and 3D print a custom case** that will house the components securely, making it more portable and professional-looking.*

## Hardware Setup

### Components
- **Raspberry Pi Pico**: The microcontroller used for the project.
- **RFID Reader**: A module for reading RFID tags.
- **LCD Display (16x2)**: A standard LCD screen for displaying the data.
- **Potentiometer**: A potentiometer to control LCD backlight brightness.
- **Transistor**: A transistor to toggle the LCD on/off.
- **LED's**: LED's to show the status of the reader.
- **Resistors**: Resistors to control the current to LED's.
- **Connecting Wires**: For wiring the components together.
- **Breadboard**: For connecting the wirings.

### Pin Connections:
- **RFID Reader**: The RFID reader module is connected to the Raspberry Pi Pico via pins:
  - VCC (from RFID) -> 3V3 (to Pico)
  - RST -> GPIO 9
  - GND -> GND
  - MISO -> GPIO 12
  - MOSI -> GPIO 15
  - SCK -> GPIO 14
  - NSS -> GPIO 13

- **LCD Display**: The LCD Display is connected via pins:
  - VSS (from LCD) -> GND (to Pico)
  - VCC -> VSYS (5v)
  - V0 -> potentiometer Signal Out
  - RS -> GPIO 22
  - R/W -> GND
  - E -> GPIO 21
  - D4 -> GPIO 17
  - D5 -> GPIO 18
  - D6 -> GPIO 19
  - D7 -> GPIO 20
  - LED+ -> adequate resistor -> VSYS (5V)
  - LED- -> transistor collector
 
- **Potentiometer**: The potentiometer is connected via pins:
  - GND (from potentiometer) -> GND (to Pico)
  - Signal Out -> V0 (to LCD)
  - VCC -> VSYS (to Pico)

- **Transistor**: The transistor is connected via pins:
  - Emitter (from transistor) -> GND (to Pico)
  - Base -> adequate resistor -> GPIO 28
  - Collector -> LED- (to LCD)
 
- **LED's**: The leds are connected via pins:
  - Green LED+ -> GPIO 6 (to Pico)
  - Yellow LED+ -> GPIO 7
  - Red LED+ -> GPIO 8
  - Green, Yellow, Red LED- -> adequate resistor -> GND

## Software Requirements

This project uses **MicroPython** for programming the Raspberry Pi Pico. You will need following libraries:
- `machine`: For controlling GPIO pins.
- `time`: For controlling timing and delays.
- `mfrc522`: For interfacing with the RFID reader. Note that the **MFRC522** RFID library used in this project is not written by me but is taken from [How2electronics](https://how2electronics.com/using-rc522-rfid-reader-module-with-raspberry-pi-pico/) and integrated into this project. The needed code is included in this repo.

You can install MicroPython on the Raspberry Pi Pico by following the official guide from [MicroPython's website](https://micropython.org/).

## Usage

1. Connect the components as described in the `Hardware Setup` section.
2. Flash the Raspberry Pi Pico with the code from this repository.
3. The RFID reader will scan any RFID tags in range.
4. The LCD display will show the data of the tag in ASCII format.

## Example:

When a RFID tag is scanned, the yellow LED is triggered until it reads the data and blinks green, or an error occurs and the red LED blinks. When the data read is successful something like `RFID TAG #35` is printed to the LCD screen.

## Known Issues

There is a known issue with **sequential RFID reads** where multiple reads cause the reader not being able to read any more tags. Currently this issue is "fixed" by **resetting the system** after each RFID tag is scanned. This solution is not optimal, as it introduces a delay, but it prevents this issue for now.

## 3D Printed Case

This project is intended to be used in

## Author

Teemu Tontti
 
