import visa
from time import sleep
import argparse

parser = argparse.ArgumentParser(description='Send a list of messages to an Agilent 33600 AWG')
parser.add_argument('-f','--filename', help='File containing SCPI commands', default="./squareWave.awg", required=False)
parser.add_argument('-a','--address', help="Address of device", default="142.104.60.122", required=False)

args = parser.parse_args()

rm = visa.ResourceManager('@py')

inst = rm.open_resource("TCPIP::"+args.address+"::INSTR")
print(inst.query("*IDN?"))

message="Starting control"
inst.write("DISP:TEXT '"+message+"'")
sleep(1)
inst.write("DISP:TEXT ''")

for line in open(args.filename):
    sleep(0.1)
    if line[0] == '#':
        continue;
    inst.write(line.strip())
    print(line.strip())
    



message="Ending control"
inst.write("DISP:TEXT '"+message+"'")
sleep(1)
inst.write("DISP:TEXT ''")
