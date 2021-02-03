from immlib import *
from immutils import *

def main(args):
    imm = Debugger()
    imm.log("[*] Finding key value...")
    imm.run(0x00405107) #FIRST INTO
    imm.stepIn()
    imm.run(0x00402467)

    keyValue = imm.readMemory(0x0040EB8, 8) #PUSH CrackmeC.0040E2B8
    imm.log("[*] I Found the key value !! --> {}".format(keyValue))

    imm.writeMemory(0x00413740, keyValue)
    inputValue = imm.readMemory(0x00413740, 8)
    imm.log("[*] I Wrote th key value {} at 0x{}".format(inputValue, hex(0x00413740)))

    for idx in range(0x00402523, 0x004025D5):
        imm.writeMemory(idx, '\x90')
    
    imm.run()

    return ("[*] Pycommand Executed!!")
