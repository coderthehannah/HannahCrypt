import sys
import argparse
import binascii
from binascii import b2a_hex
from binascii import a2b_hex
from base64 import b64decode, b64encode
from base64 import b32decode, b32encode
from math import exp, factorial, log, log10, log2, pi

########## Variables


logo ="\n  _______\n <	 \ \n < 	  \          ________ \n < 	  /         /        \ \n <	  \        /     ____/ \n <	   \      <     / \n <         /      <     \____\n <	  /        \         \ \n <_______/   <>     \________/ <>	\n\n"

version ="0.0.1a dev"

algos = ["base64", "base32", "hex (hexadecimal)"]
######### Error functions

def encDecErr():
    print("ERROR: Something went wrong, check your settings or try again")
    if (args.input==None):
        print("It seems like you didn't specify any input ('--input')")
    
def checkEncDec():
    if (args.encrypt) and (args.decrypt):
        print("ERROR: Please select either encryption or decryption method")
        sys.exit()
    if (args.encrypt==0) and (args.decrypt==0) and not (args.input==None):
        print("Please specify if you want to encrypt or decrypt ('--encrypt/--decrypt' or '-E/-D')")
        sys.exit()
    print("\n")


######### Command-Line Arguments


MyArgsDesc = logo

parser = argparse.ArgumentParser(description="           xXB3schdl_CryptXx \n\n Note, that all Arguments with a double Dash ('--') don't require an aditional input, all with one dash ('-') require one.")



parser.add_argument('--version', '-V', help="Shows version", action="store_true")
parser.add_argument('--logo', '-L', help = "Shows the logo", action="store_true")
parser.add_argument('--encrypt', '-E', help ="Select encryption method", action="store_true")
parser.add_argument('--decrypt', '-D', help ="Select decryption method", action="store_true")
parser.add_argument('-type', '-t', type=int, 
                    help="Selectd Input method: \n 0: Raw Input \n 1: File Input")

parser.add_argument('-list', '-l',
                    help="List possibilities of arguments")


parser.add_argument('-algorithm', '-a',
                    help="Select the algorithm")

parser.add_argument('-input', '-i',
                   help="Input the name here",
                   )

parser.add_argument('-output', '-o',
                    help="This will be the output"
                    )

args = parser.parse_args()



print("\n")


######### Command-Line Argument Functions


if args.list=='algorithms':
    print("   Availabe algorithms:\n")
    for algosTemp in algos:
        print(" - ", algosTemp)


checkEncDec()

if (args.logo):
    print(logo)
    sys.exit()


if (args.version):
    print(logo)
    print("\n")
    print("The actual Version is: ")
    print(version)
    sys.exit()


####### Algorithm functions


class Algorithms:

    class NonKeyEncryptions:

        ### BASE64

        def base64():
            out = ""
            if (args.encrypt):
                #### Here you need bytes
                out = b64encode(bytes(args.input, 'ASCII'))
            elif (args.decrypt):
                out = b64decode(args.input)
            else:
                encDecErr()
            return out

        ### BASE32

        def base32():
            out = ""
            if (args.encrypt):
                #### Here you need bytes
                out = b32encode(bytes(args.input, 'ASCII'))
            elif (args.decrypt):
                out = b32decode(args.input)
            else:
                encDecErr()
            return out
			
		### HEXADECIMAL
			
        def hex():
            out = ""
            if (args.encrypt):
                temp = bytes(args.input, 'ASCII')
                out = b2a_hex(temp)
            elif (args.decrypt):
                out = a2b_hex(args.input)
            return out
				

a = Algorithms
n = a.NonKeyEncryptions



###### This is the guy that switches between the functions




if (args.algorithm=="base64"):
    outp = n.base64()
    print(outp)
elif (args.algorithm=="base32"):
    outp = n.base32()
    print(outp)
elif (args.algorithm=="hex") or (args.algorithm=="hexadecimal"):
    outp = n.hex()
    print(outp)
elif (args.algorithm==None):
    print("Please specify an algorithm")
else:
    print("Your algorithm is not valid, get a list of algorithms with 'Beschdlcrypt.py -list algorithms'; Did you type it wrong?")

class Convert:
    def texttohex():
        if (args.input!="" and args.input!=1):
            temp = bytes(args.input, 'ASCII')
            out = b2a_hex(temp)
            return out
        else:
            print ("ERROR: Please enter a valid string")
            sys.exit()