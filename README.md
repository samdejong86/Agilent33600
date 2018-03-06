# Agilent (Keysight) 33600A Waveform Generator programmer

## Description

There are two scripts in this repository: AgilentControl.py and UploadArb.py


This AgilentControl.py programs an Agilent 33600A arbitrary waveform generator by sending a series of [SCPI](https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments) commands via TCP. It should be straightforward to modify this for other devices which use SCPI

Information on the SCPI interface for the Agilent 33600A can be found on page 192 of [this document](https://literature.cdn.keysight.com/litweb/pdf/33500-90901.pdf?id=2197440)

UploadArb.py uploads a specified arbitrary wavefrom to the device and saves it to the device's memory.


## Requirements

Install the pyVISA back and front end:

    pip install pyvisa-py

## Usage

   AgilentControl.py [-h] [-f FILENAME] [-a ADDRESS]

      Send a list of messages to an Agilent 33600 AWG

      optional arguments:
        -h, --help            show this help message and exit
        -f FILENAME, --filename FILENAME
                              File containing SCPI commands
        -a ADDRESS, --address ADDRESS
                              Address of device

   UploadArb.py [-h] -f FILENAME [-a ADDRESS] [-v PULSEHEIGHT]

      Upload an arbitrary waveform to an Agilent 33600 AWG

      optional arguments:
        -h, --help            show this help message and exit
	-f FILENAME, --filename FILENAME
                              File containing arbitrary waveform
        -a ADDRESS, --address ADDRESS
                              Address of device
        -v PULSEHEIGHT, --pulseheight PULSEHEIGHT
                              Pulse height of arb
 


## Files

    freqSweep.awg
       Sets a frequency sweep on channel 2

    arb.awg
       Loads the atlas calibration arb

    arbLoad.awg
	Loads the atlas calibration arb into volatile memory

    squareWave.awg
       Generates a square wave

    triangleWave.awg
	Generates a triangle wave

    ATLASCALIB.dat
        Atlas calibration wave
