import visa
from time import sleep
import argparse
import struct
import numpy as np
import csv
import os


#parse arguments
parser = argparse.ArgumentParser(description='Send a list of messages to an Agilent 33600 AWG')
parser.add_argument('-f','--filename', help='File containing arbitrary waveform', default="./test.dat", required=True)
parser.add_argument('-a','--address', help="Address of device", default="142.104.60.122", required=False)
parser.add_argument('-v','--pulseheight', help="Pulse height of arb", default="0.1", required=False)

args = parser.parse_args()


name=os.path.splitext(os.path.basename(args.filename))[0]
samplePeriod=0
num=0
tlast=-1

arb=[]
with open(args.filename,'r') as f:
    next(f) # skip headings
    reader=csv.reader(f,delimiter=' ')
    for t,p in reader:
        arb.append(float(p))
        if tlast != -1:
            samplePeriod=samplePeriod+(float(t)-float(tlast))
            num=num+1
        tlast=t

samplePeriod=samplePeriod/num
sRate=str(1/samplePeriod)

sig = np.asarray(arb, dtype='f4')/max(arb)

#load the VISA resource manager
rm = visa.ResourceManager('@py')

#connect to the device
inst = rm.open_resource("TCPIP::"+args.address+"::INSTR")
print(inst.query("*IDN?"))

#sent start control message
message="Uploading\nArbitrary\nWaveform"
inst.write("DISP:TEXT '"+message+"'")


inst.write('FORM:BORD SWAP')
inst.write('SOUR1:DATA:VOL:CLE')

inst.write_binary_values('SOUR1:DATA:ARB '+name+',', sig, datatype='f', is_big_endian=False)

inst.write('*WAI')


inst.write('SOUR1:FUNC:ARB '+name)

inst.write('SOUR1:FUNC:ARB:SRAT ' + sRate)
inst.write('SOUR1:VOLT:OFFS 0')
inst.write('SOUR1:FUNC ARB')
inst.write('SOUR1:VOLT '+args.pulseheight)


inst.write('MMEM:STOR:DATA "INT:\\'+name+'.arb"')

inst.write("DISP:TEXT ''")


inst.write('SYST:ERR?')
instrument_err = inst.read()
print(instrument_err)

inst.close()