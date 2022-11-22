import sys
import os
import argparse
import binascii
import hashlib as h
import math
import importlib
import urllib.request
from binascii import b2a_hex
from base64 import b64decode, b64encode
from binascii import a2b_hex
from base64 import b32decode, b32encode

#Installing Pip cant be in a function. Dont know why -Wyn
oldargs = sys.argv
sys.argv = [sys.argv[0]]

try:
    import pip
except ImportError:
    print("Pip not installed. Installing. The Program will have to restart")
    exec(urllib.request.urlopen("https://bootstrap.pypa.io/get-pip.py").read().decode("utf-8"))
sys.argv = oldargs

def tryimportPIL():
    try:
        import PIL
    except ImportError:
        import pip
        print("Pillow not installed. Installing")
        pip.main(['install', "Pillow"])
        globals()["PIL"] = importlib.import_module("PIL")

def tryimportcryptography():
    try:
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization as crypto_serialization
        from cryptography.hazmat.backends import default_backend as crypto_default_backend
        print(rsa)
    except ImportError:
        import pip
        print("cryptography not installed, installing...")
        try:
            pip.main(["install", "cryptography"])
        except OSError:
            print("Failed to Establish connectiong to server, aborting!")
            try:
                os.system("ping -c 1 4.2.2.2")
            except OSError:
                print("Seems like you don't have an internet connecion please check it")
                sys.exit()
            print("You seem to have internet connection, but the server is not reachable, please try again later")
        globals()["cryptography"] = importlib.import_module("cryptography")
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization as crypto_serialization
        from cryptography.hazmat.backends import default_backend as crypto_default_backend
        
def tryGetLibraries():
    try:
        from Crypto import Random
        from Crypto.Cipher import AES
    except ImportError:
        print("Detected missing libraries, installing...")
        pip.main(['install', "Crypto"])
    else:
        print("Everything important is already installed")
        
        
######### API Stuff

listeners = []

def addListener(listener):
    listener.onPrint("")
    listener.activate()
    listeners.append(listener)

def output(*args):
    if(len(listeners) == 0):
        print(*args)
    for l in listeners:
        l.onPrint(*args)


##### Utils


class Utils:

    def getBinaryInput():
        return Utils.getBinaryFromString(args.input)

    def getBinaryFromString(inp):
        binary = inp
        is_binary = True
        is_hex = True
        bin_out = ""
        for char in binary:
            if char not in ["0", "1", " ", "\n"]:
                is_binary = False
                break;
            elif char != " " and char != "\n":
                bin_out += char
        if not is_binary:
            hex_out = ""
            for char in binary:
                if char not in list("0123456789ABCDEF \n"):
                    is_hex = False
                    break;
                elif char != " " and char != "\n":
                    hex_out+= char
            if is_hex:
                return bin(int(hex_out, 16))
            ascii_binary = ""
            for char in binary:
                bin_char = bin(int.from_bytes(char.encode(args.encoding), 'big'))
                bin_char = bin_char[2:len(bin_char)]
                for i in range(8 - len(bin_char)):
                    ascii_binary += "0"
                ascii_binary += bin_char
            binary = ascii_binary
        else:
            return bin_out
        return binary

    def getStringFromBinary(inp):
        out = ""
        for i in range(int(len(inp) / 8)):
            n = int(inp[i*8:(i+1)*8], 2)
            out += n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(args.encoding)
        return out

    def printBinaryString(bin_input):
        output("Binary Output:")
        output(bin_input)
        output("\n")
        output("String Output:")
        output(Utils.getStringFromBinary(bin_input))

    def openTempAsciiFile(bin_input):
        import os, time
        file = open("output.txt", "w")
        file.write(Utils.getStringFromBinary(bin_input))
        file.close()
        os.startfile("output.txt")
        time.sleep(1)
        os.remove("output.txt")

utils = Utils

########## A free line
if len(sys.argv) != 1:
    output("\n")





########## Variables


logo ="\n  _______\n <	 \ \n < 	  \          ________ \n < 	  /         /        \ \n <	  \        /     ____/ \n <	   \      <     / \n <         /      <     \____\n <	  /        \         \ \n <_______/   <>     \________/ <>	\n\n"
modules = ["PIL", "pip", "cryptography"]
version ="0.1.2a"
lists = ["algos/algorithms", "non_cript_algos", "lists", "encodings", "key_generating_functionsfunctions", "one_way_functions"]
algos = ["base64", "base32", "hex (hexadecimal)", "md5", "bi (binaryimage)", "x0r / xor", "binary", "sha256", "sha1", "sha512", "crc32", "rsa"] #MUST BE LOWERCASE
aliases =   {
            "generatersakeys": "rsakeys",
            "hexadecimal" : "hex",
            "MessageDigest5": "md5",
            "binaryimage": "bi",
            "xor": "x0r",
            "SecureHashAlgorithm-256": "sha256",
            "SecureHashAlgorithm-1": "sha1",

            ###USED FOR API
            algos[2]: "hex",
            algos[4]: "bi",
            algos[5]: "x0r",

            }
one_way_functions = ["sha256", "sha512", "sha1", "crc32", "md5"]
key_generating_functions = ["rsa"]
conversion_algos = ["hex", "binary"]
non_cript_algos = ["x0r", "md5"]
file_input_only_algos = ["bi:d"]
require_keys_algos = ["x0r"]
require_output_algos = ["bi:e"]
raw_input = 0
file_input = 1

encodings = ["UTF-8", "ASCII", "BIG5", "johab"]

helpinfo = {
            "base64": "Base64 represents binary data in an ASCII string format by translating it into a base-64 representation. This basically means that all kind of characters (ASCII, UTF8, UTF16...) with control characters can be mapped for example in English alphabet a-z, A-Z, 0-9",
            "base32": "Base32 represents binary data in an ASCII string format by translating it into a base-32 representation. This basically means that all kind of characters (ASCII, UTF8, UTF16...) with control characters can be mapped for example in English alphabet a-z and 0-7",
            "hex": "Converts hex to text, and text to hex",
            "md5": "Message Digest 5 (MD5) is a hash function used in cryptography. Developed by Ronald Rivest in 1991, Message Digest 5 produces a 128-bit resulting hash value. Similar to other message-digest algorithms, it was largely developed for digital signature applications which make use of a large compressed file in a secure fashion.",
            "bi": "BinaryImage is used to convert images to binary, and binary to images. It does so be cycling through each binary value, and placing a black pixel if the value is '1', and a white if '0'",
            "x0r": "X0r is a cipher, that converts the input to binary, and the key to binary, then goes through each value of the input XORing each value. Note if the key is shorter than the input, it will be looped.",
            "binary": "Converts the input to binary and vice versa"
            }

######### Error functions

def encDecErr():
    output("ERROR: Something went wrong, check your settings or try again")
    if (args.input==None):
        output("It seems like you didn't specify any input ('--input')")

def checkEncDec():
    if (args.encrypt) and (args.decrypt):
        output("ERROR: Please select either encryption or decryption method")
        sys.exit()
    if (args.encrypt==0) and (args.decrypt==0) and not (args.input==None) and not (args.version) and not (args.logo) and (args.list==None) and not args.algorithm in non_cript_algos and not args.algorithm in key_generating_functions:
        output("Please specify if you want to encrypt or decrypt ('--encrypt/--decrypt' or '-E/-D')")
        sys.exit()
    output("\n")

def checkInput():
    if (args.input==None or len(args.input)==0) and not args.algorithm in key_generating_functions:
        output("Please specify an input with -i")
        sys.exit()


######### Command-Line Arguments


MyArgsDesc = logo

parser = argparse.ArgumentParser(description="           xXB3schdl_CryptXx \n\n Note, that all Arguments with a double Dash ('--') don't require an aditional input, all with one dash ('-') require one.")


parser.add_argument('--installrequisites', '--installprerequisites', '--instreq', '-IR', help="Install needed modules and scripts", action="store_true")
parser.add_argument('--version', '-V', help="Shows version", action="store_true")
parser.add_argument('--logo', '-L', help = "Shows the logo", action="store_true")
parser.add_argument('--info', '-I', help ="Get info on the specified command", action="store_true")
parser.add_argument('--encrypt', '-E', help ="Select encryption method", action="store_true")
parser.add_argument('--decrypt', '-D', help ="Select decryption method", action="store_true")
parser.add_argument('-type', '-t', type=int,
                    help="Select Input method: \n 0: Raw Input \n 1: File Input")
parser.add_argument('-encoding', '-e',
                    help="Select the encoding")
parser.add_argument('-list', '-l',
                    help="List possibilities of arguments")
parser.add_argument('-keysize', '-bitlength', '-bitsize', '-keylength', '-ks',
                    help=argparse.SUPPRESS,                                           #help="Input the size of the key you want to create (In Bits)",
                    type=int)
parser.add_argument('-algorithm', '-a',
                    help="Select the algorithm")

parser.add_argument('-input', '-i',
                   help="Input the name here",
                   )

parser.add_argument('-key', '-k',
                   help="The key, if needed"
)

parser.add_argument('-output', '-o',
                    help="This will be the output"
                    )

args = parser.parse_args()

if args.encoding==None:
    args.encoding="ASCII"
if args.type==None:
    args.type=raw_input
if args.algorithm in aliases:
    args.algorithm = aliases[args.algorithm]
if args.keysize==None and args.algorithm in  key_generating_functions:
    args.keysize=2048

######### Command-Line Argument Functions

#Cant print anything if sys args are empty, as importing the file as an API will also run it

def imports():
    tryimportPIL()
    tryimportcryptography()
    tryGetLibraries()
    from Crypto import Random
    from Crypto.Cipher import AES

def commandLineChecks():

    if (args.installrequisites):
        imports()

    if args.list=="Algorithms" or args.list=="algos":
        output("   Availabe algorithms:\n")
        for Temp in algos:
            output(" - ", Temp)
        sys.exit()
    elif args.list=="encodings":
        output("   Availabe algorithms:\n")
        for Temp in encodings:
            output(" - ", Temp)
        output("\nThese are not the only encodings, you can choose others, that are supported")
        sys.exit()
    elif args.list=="key_generating_functions":
        output("   Availabe key generating functions:\n")
        for Temp in key_generating_functions:
            output(" - ", Temp)
        sys.exit()
    elif args.list=="lists":
        output("   Availabe lists\n")
        for Temp in lists:
            output(" - ", Temp)
        sys.exit()
    elif not (args.list==None):
        output("You did not select a valid list")
        sys.exit()

    if args.info:
        if args.algorithm == None:
            output("there was no algorithm selected")
            sys.exit()
        output(helpinfo[args.algorithm])
        sys.exit()
    if (args.logo):
        output(logo)
        sys.exit()

    if (args.version):
        print("{}\nThe actual Version is: {}".format(logo, version))
        sys.exit()
    checkEncDec()
    checkInput()

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
            return str(out)[2:len(out) + 2]

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
            return str(out)[2:len(out) + 2]


        ### BINARYIMAGE

        def binaryimage():
            tryimportPIL()
            from PIL import Image
            if(args.decrypt):
                try:
                    im = Image.open(args.input)
                except FileNotFoundError:
                    output("Image '" + args.input + "' cannot be found")
                    return;
                pix = im.load()
                errored_colors = False
                binary_output = ""
                for y in range(im.size[0]):
                    for x in range(im.size[1]):
                        pix_color = pix[x,y]
                        pix_white = pix_color[0] == 255
                        if pix_color[0] != pix_color[1] or pix_color[1] != pix_color[2]:
                            if not errored_colors:
                                output("Image has color values. Assuming all colored pixels are black")
                                errored_colors = True
                            pix_white = False
                        if pix_white: binary_output += "0"
                        else: binary_output += "1"
                utils.printBinaryString(binary_output)



            if(args.encrypt):
                if args.output == None or len(args.output) == 0:
                    output("Please specify an output with -o")
                    return
                binary = "".join(utils.getBinaryInput().split(" "))
                size = math.ceil(math.sqrt(len(binary)))
                im = Image.new("RGB", (size, size))
                pix = im.load()
                for i in range(size*size):
                    color = 0
                    if i >= len(binary) or binary[i] == "0":
                        color = 255
                    pix[i % size, math.floor(i / size)] = (color, color, color, 255)
                imloc = args.output + ".png"
                if len(args.output.split(".")) > 1:
                    imloc = args.output
                try:
                    im.save(imloc)
                    output("File saved to: " + "\\".join(sys.argv[0].split("\\")[0:-1]) + "\\" + imloc)
                except ValueError:
                    output("Unknown file extension: ." + imloc.split(".")[-1])


    class OneWayFunctions:

        ### MessageDigest 5 (MD5)
        def md5():
            output(h.md5(args.input.encode(args.encoding)).hexdigest())
        ### MessageDigest 4 (MD4)
        def sha512():
            output(h.sha512(args.input.encode(args.encoding)).hexdigest())
        ### SecureHashAlgorithm-256 (SHA-256)
        def sha256():
            output(h.sha256(args.input.encode(args.encoding)).hexdigest())

        ### SecureHashAlgorithm-1 (SHA-1)
        def sha1():
            output(h.sha1(args.input.encode(args.encoding)).hexdigest())
        ### CyclicReadunancyCheck32 (CRC32)
        def crc32():
            temp = binascii.crc32(bytes(args.input.encode(args.encoding))) & 0xFFFFFFFF
            output("%08X" % temp)
        ###
    class KeyEncryptions:

        ###X0R

        def x0r():
            data = utils.getBinaryInput()
            if args.key == None:
                output("There was no key specified")
                return;
            data = utils.getBinaryInput()
            if args.type == raw_input:
                key = utils.getBinaryFromString(args.key)
            elif args.type == file_input:
                key = utils.getBinaryFromString(open(args.key, "r").read())
            key = utils.getBinaryFromString(args.key)
            original_key = key
            while len(key) < len(data): key += original_key
            binary_output = ""
            for i in range(len(data)):
                is_1 = data[i] != key[i]
                if(is_1): binary_output += "1"
                else: binary_output += "0"
            utils.printBinaryString(binary_output)
            if args.type == file_input:
                utils.openTempAsciiFile(binary_output)

    class Conversions:

        ### HEXADECIMAL

        def hex():
            out = ""
            if (args.encrypt):
                out = "".join(hex(int(utils.getBinaryInput(), 2)).upper().split("0X"))
            elif (args.decrypt):
                out = a2b_hex(args.input)
            else:
                encDecErr()
            return out

        ### BINARY

        def binary():
            out= ""
            if (args.encrypt):
                out = utils.getBinaryFromString(args.input)
            elif (args.decrypt):
                for char in args.input:
                    if char not in "01 ":
                        output("You need to give a valid binary input\n")
                        sys.exit()
                out = utils.getStringFromBinary(args.input)
            else :
                encDecErr()
            return out

    class Miscelanious:
        def rsa():
            tryimportcryptography()
            from cryptography.hazmat.primitives import serialization as crypto_serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.backends import default_backend as crypto_default_backend
            key = rsa.generate_private_key(
                backend=crypto_default_backend(),
                public_exponent=65537,
                key_size=args.keysize
            )

            output("Your private key is (very private):")
            private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
                crypto_serialization.PrivateFormat.PKCS8,
                crypto_serialization.NoEncryption())
            output(private_key.decode(args.encoding))
            output("\n\n\n")
            output("Your public key is:\n")
            public_key = key.public_key().public_bytes(
                crypto_serialization.Encoding.OpenSSH,
                crypto_serialization.PublicFormat.OpenSSH)
            output(public_key.decode(args.encoding).replace('ssh-rsa ', ''))



a = Algorithms
n = a.NonKeyEncryptions
o = a.OneWayFunctions
k = a.KeyEncryptions
c = a.Conversions
m = a.Miscelanious


###### This is the guy that switches between the functions



def main():
    imports()
    if args.algorithm not in file_input_only_algos:
        try:
            args.input = open(args.input, "r").read()
        except Exception:
            pass;
    if (args.algorithm=="base64"):
        outp = n.base64()
        output(outp)
    elif (args.algorithm=="base32"):
        outp = n.base32()
        output(outp)
    elif args.algorithm=="hex":
        outp = c.hex()
        output(outp)
    elif args.algorithm=="md5":
        o.md5()
    elif args.algorithm=="sha256":
        o.sha256()
    elif args.algorithm=="sha1":
        o.sha1()
    elif args.algorithm=="crc32":
        o.crc32()
    elif args.algorithm=="sha512":
        o.sha512()
    elif args.algorithm=="bi":
        n.binaryimage()
    elif args.algorithm=="x0r":
        k.x0r()
    elif args.algorithm=="rsa":
        m.rsa()
    elif args.algorithm=="binary":
        outp = c.binary()
        output(outp)
    elif not (args.algorithm==None):
        output("Your algorithm is not valid, get a list of algorithms with 'Beschdlcrypt.py -list algorithms'; Did you type it wrong?")

if(len(sys.argv) != 1):
    commandLineChecks()
    main()
