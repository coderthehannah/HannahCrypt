import sys
import argparse
import binascii
import hashlib
from binascii import b2a_hex
from binascii import a2b_hex
from base64 import b64decode, b64encode
from base64 import b32decode, b32encode
from math import exp, factorial, log, log10, log2, pi

########## A free line
print("\n")
########## Variables


logo ="\n  _______\n <	 \ \n < 	  \          ________ \n < 	  /         /        \ \n <	  \        /     ____/ \n <	   \      <     / \n <         /      <     \____\n <	  /        \         \ \n <_______/   <>     \________/ <>	\n\n"

version ="0.0.1a"

algos = ["base64", "base32", "hex (hexadecimal), md5"]


encodings = ["UTF-8", "ASCII", "BIG5", "johab"]

######### Error functions

def encDecErr():
    print("ERROR: Something went wrong, check your settings or try again")
    if (args.input==None):
        print("It seems like you didn't specify any input ('--input')")
    
def checkEncDec():
    if (args.encrypt) and (args.decrypt):
        print("ERROR: Please select either encryption or decryption method")
        sys.exit()
    if (args.encrypt==0) and (args.decrypt==0) and not (args.input==None) and not (args.version) and not (args.logo) and (args.list==None):
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
parser.add_argument('-encoding', '-e', 
                    help="Select the encoding")
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

if (args.encoding==None):
    args.encoding="ASCII"



######### Command-Line Argument Functions


if args.list=="Algorithms" or args.list=="algos":
    print("   Availabe algorithms:\n")
    for Temp in algos:
        print(" - ", Temp)
        
elif args.list=="encodings":
    print("   Availabe algorithms:\n")
    for Temp in encodings:
        print(" - ", Temp)
    print("\nThese are not the only encodings, you can choose others, that are supported")
elif not (args.list==None):
    print("You did not select a valid list")

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
                out = b64encode(bytes(args.input, args.encoding))
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
                out = b32encode(bytes(args.input, args.encoding))
            elif (args.decrypt):
                out = b32decode(args.input)
            else:
                encDecErr()
            return out
			
		### HEXADECIMAL
			
        def hex():
            out = ""
            if (args.encrypt):
                temp = bytes(args.input, args.encoding)
                out = b2a_hex(temp)
            elif (args.decrypt):
                out = a2b_hex(args.input)
            else:
                encDecErr()
            return out
            
				
    class OneWayFunctions:
        
        ### MessageDigest 5 (MD5)
        def md5():      
            if (args.encrypt):
                m = hashlib.md5(args.input.encode(args.encoding))
                out = m.hexdigest()
            elif (args.decrypt):
                print("ERROR: This is a OneWayFunction, you can only Encrypt stuff")
            else:
                encDecErr()
            print(out)
                
a = Algorithms
n = a.NonKeyEncryptions
o = a.OneWayFunctions


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
elif (args.algorithm=="md5") or (args.algorithm=="MessageDigest5"):
    o.md5()
elif not (args.algorithm==None):
    print("Your algorithm is not valid, get a list of algorithms with 'Beschdlcrypt.py -list algorithms'; Did you type it wrong?")

class Convert:
    def texttohex():
        if (args.input!="" and args.input!=1):
            temp = bytes(args.input, args.encoding)
            out = b2a_hex(temp)
            return out
        else:
            print ("ERROR: Please enter a valid string")
            sys.exit()
            
