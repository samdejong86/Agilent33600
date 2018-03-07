import visa
from time import sleep
import argparse

#parse arguments
parser = argparse.ArgumentParser(description='Send a list of messages to an Agilent 33600 AWG')
parser.add_argument('-f','--filename', help='Macro file containing SCPI commands', default="./squareWave.awg", required=True)
parser.add_argument('-a','--address', help="Address of device", default="142.104.60.122", required=False)

args = parser.parse_args()


#load the VISA resource manager
rm = visa.ResourceManager('@py')

#connect to the device
inst = rm.open_resource("TCPIP::"+args.address+"::INSTR")
print(inst.query("*IDN?"))

#sent start control message
message="Controlling\nRemotely"
inst.write("DISP:TEXT '"+message+"'")


#clear any sweeps
inst.write("SOURCE2:FREQUENCY:MODE FIX")

#sent commands to device
for line in open(args.filename):
    sleep(0.1)
    #ignore commented lines
    if line[0] == '#':
        continue;
    inst.write(line.strip())
    print(line.strip())


inst.write("DISP:TEXT ''")

instrument_err = "error"
while instrument_err != '+0,"No error"\n':
    inst.write('SYST:ERR?')
    instrument_err = inst.read()
    if instrument_err[:2] == "+0":
        continue;
    print(instrument_err)


inst.close()
