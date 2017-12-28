from tkinter import filedialog
from tkinter import *
import sys
import os
import math

version = "0.0.1"

try:
    import Beschdlcrypt_dev
except ImportError:
    print("Main script not found. Aborting!")
    sys.exit()
import Beschdlcrypt_dev as parent

######### API stuff
class APIListener:
    isActive = False

    def onPrint(self, *args):
        if self.isActive:
            arglist = []
            for item in args:
                arglist.append(str(item))
            if _type.get() == "Convertion":
                setConvertOutput(" ".join(arglist))
                return;
            t = output_box[0].get("1.0","end")
            if str(t)[0] == "\n":
                t = t[1:len(t)]
            output_box[0].delete("1.0", "end")
            output_box[0].insert("1.0", t + " ".join(arglist))

    def activate(self):
        self.isActive = True

isFileOpen = False

master = Tk()

arrow = PhotoImage("arrow")
arrow.config(height = 11, width = 11)
arrow_text = """#FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #3a3a3a #313131 #313131 #313131 #313131 #313131 #313131 #313131 #313131 #313131 #3a3a3a #050507 #010002 #010002 #010002 #010002 #010002 #010002 #010002 #010002 #010002 #050507 #3f3f3f #030205 #010002 #010002 #010002 #010002 #010002 #010002 #010002 #030205 #3f3f3f #FFFFFF #121212 #020103 #010002 #010002 #010002 #010002 #010002 #020103 #131313 #FFFFFF #FFFFFF #FFFFFF #0b070b #020103 #010002 #010002 #010002 #020103 #0b070b #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #060606 #010002 #010002 #010002 #060606 #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #555555 #040204 #010002 #040204 #7f7f7f #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #FFFFFF #0c0c18 #030305 #0c0c18"""

for a in range(len(arrow_text.split(" "))):
    if arrow_text.split(" ")[a] != "#FFFFFF":
        arrow.put("{" + arrow_text.split(" ")[a] + "}", (a % 11, math.floor(a / 11)))
parent.addListener(APIListener())

_type = StringVar(master)
_type.set("Choose A Method")

_convert_input = StringVar(master)
_convert_input.set("Text")
_convert_output = StringVar(master)
_convert_output.set("Text")
_convert_encoding_input = StringVar(master)
_convert_encoding_input.set(parent.encodings[0])
_convert_encoding_ouput = StringVar(master)
_convert_encoding_ouput.set(parent.encodings[0])

_en = IntVar()

current_file = ""

def chosefile(c):
    global current_file
    current_file = openfile().replace("/", "\\")
    filetext = current_file.split("\\")[-1]
    if len(filetext) > 20:
        filetext = filetext[0:15] + "...." + filetext.split(".")[-1]
    c[0].config(text = filetext)

def isIn(l):
    if _en.get() == 0:
        ende = ":e"
    else:
        ende = ":d"
    return _type.get().lower() in l or _type.get().lower() + ende in l

def setConvertOutput(output):
    conversion_ouput[0].delete("1.0", "end")
    conversion_ouput[0].insert("1.0", str(output))

def convert():
    inp = ""
    if _convert_input.get() == "binary":
        for char in conversion_input[0].get("1.0","end")[0:-1]:
            if char not in ["0", "1", " ", "\n"]:
                setConvertOutput("Malformed Input! '" + char + "' is not a binary character")
                return;
            elif char != " " and char != "\n":
                inp += char
    elif _convert_input.get() == "hex":
        for char in conversion_input[0].get("1.0","end")[0:-1]:
            if char not in list("0123456789ABCDEF \n"):
                setConvertOutput("Malformed Input! '" + char + "' is not a hex character")
                break;
            elif char != " " and char != "\n":
                inp += char
        o = ""
        for char in inp:
            t = str(bin(int(char, 16)).split("0b")[1])
            if len(t) != 4:
                for c in range(4 - len(t)):
                    o += "0"
            o += t
        inp = o
    else:
        for char in conversion_input[0].get("1.0","end")[0:-1]:
            bin_char = bin(int.from_bytes(char.encode(_convert_encoding_input.get()), 'big'))
            bin_char = bin_char[2:len(bin_char)]
            for i in range(8 - len(bin_char)):
                inp += "0"
            inp += bin_char

    if _convert_output.get() == "binary":
        setConvertOutput(inp)
    elif _convert_output.get() == "hex":
        setConvertOutput("".join(hex(int(inp, 2)).upper().split("0X")))
    else:
        out = ""
        for i in range(int(len(inp) / 8)):
            n = int(inp[i*8:(i+1)*8], 2)
            out += n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(_convert_encoding_ouput.get())
        setConvertOutput(out)


def run():

    if _type.get() == "Convertion":
        convert()
        return
    parent.args.encrypt = _en.get() == 0
    parent.args.decrypt = _en.get() == 1
    parent.args.algorithm = _type.get().lower()
    toggleOutIn()

    if _en.get() == 0:
        ende = ":e"
    else:
        ende = ":d"
    if len(current_file) != 0 or isIn(parent.file_input_only_algos):
        parent.args.type = parent.file_input
        parent.args.input = current_file
    else:
        parent.args.input = string_input[0].get("1.0","end")[0:-1]
        parent.args.type = parent.raw_input
    parent.args.output = output_input[0].get("1.0","end")[0:-1]
    parent.args.key = key_input[0].get("1.0","end")
    parent.main()

def toggleOutIn():
    global onOutPutScreen
    output_box[0].delete(1.0, "end")
    onOutPutScreen = not onOutPutScreen

onOutPutScreen = False
algolist = ["Convertion"]
for algo in parent.algos:
    algo1 = algo
    if algo in parent.aliases:
        algo1 = parent.aliases[algo]
    if algo1 not in parent.conversion_algos:
        algolist.append(str(algo).capitalize())

conversion_list = ["Text"]
for algo in parent.conversion_algos:
    conversion_list.append(str(algo).capitalize())

mainscreen = OptionMenu(master, _type, *algolist), 0.4, 0.1, 0.2, 0.1
en_sel = Radiobutton(master, text = "Encrypt", variable=_en, value=0), 0.7, 0.4, 0.1, 0.05
de_sel = Radiobutton(master, text = "Decrypt", variable=_en, value=1), 0.7, 0.45, 0.1, 0.05
string_input = Text(master, bg = "#FFFFFF"), 0.2, 0.4, 0.4, 0.2
file_button = Button(master, text="Choose File", command = lambda: chosefile(file_text)), 0.2, 0.4, 0.1, 0.05
file_text = Label(master, text = "No file Chosen", bg = "#FFFFFF", anchor = W), 0.3, 0.4, 0.2, 0.05
text_file_button = Button(master, text="Choose File", command = lambda: chosefile(text_file_text)), 0.2, 0.7, 0.1, 0.05
text_file_text = Label(master, text = "No file Chosen", bg = "#FFFFFF", anchor = W), 0.3, 0.7, 0.2, 0.05
key_input_text = Label(master, text = "key:", bg = "#FFFFFF", anchor = W), 0.67, 0.5, 0.1, 0.05
key_input = Text(master), 0.7, 0.5, 0.2, 0.1
finalize_button = Button(master, text = "Encrypt", command = run), 0.4, 0.8, 0.2, 0.1
output_input = Text(master), 0.7, 0.6, 0.2, 0.1
output_input_text = Label(master, text = "output file:", bg = "#FFFFFF", anchor = W), 0.62, 0.6, 0.07, 0.05

conversion_input = Text(master, bg = "#FFFFFF"), 0.05, 0.4, 0.4, 0.3
conversion_ouput = Text(master, bg = "#FFFFFF"), 0.55, 0.4, 0.4, 0.3
conversion_input_type = OptionMenu(master, _convert_input, *conversion_list), 0.048, 0.3, 0.2, 0.1
conversion_output_type = OptionMenu(master, _convert_output, *conversion_list), 0.752, 0.3, 0.2, 0.1
conversion_input_encoding = OptionMenu(master, _convert_encoding_input, *parent.encodings), 0.252, 0.3, 0.2, 0.1
conversion_output_encoding = OptionMenu(master, _convert_encoding_ouput, *parent.encodings), 0.548, 0.3, 0.2, 0.1

_copyright = Label(master, text = version + "\nWyn Price 2017", bg = "#FFFFFF"), 0.87, 0.9, 0.15, 0.1

output_box = Text(master), 0.1, 0.05, 0.8, 0.7
output_back = Button(master, text = "back", command = toggleOutIn), 0.4, 0.8, 0.2, 0.1
def update():
    componants = [_copyright]
    if _type.get().lower() in parent.aliases:
        _type.set(parent.aliases[_type.get().lower()].capitalize())
    master.after(50, update)
    if _type.get() == "Convertion":
        componants.append(mainscreen)
        componants.append(finalize_button)
        finalize_button[0].config(text = "Convert")
        componants.append(conversion_input)
        componants.append(conversion_ouput)
        componants.append(conversion_input_type)
        componants.append(conversion_output_type)
        if _convert_input.get() == "Text":
            componants.append(conversion_input_encoding)
        if _convert_output.get() == "Text":
            componants.append(conversion_output_encoding)
    elif onOutPutScreen:
        componants.append(output_back)
        componants.append(output_box)
    else:
        componants.append(mainscreen)
        componants.append(finalize_button)
        if _en.get() == 0:
            finalize_button[0].config(text = "Encrypt")
        else:
            finalize_button[0].config(text = "Decrypt")
        if not isIn(parent.non_cript_algos):
            componants.append(en_sel)
            componants.append(de_sel)
        else:
            finalize_button[0].config(text = "Go")

        if not isIn(parent.file_input_only_algos):
            componants.append(string_input)
            componants.append(text_file_button)
            componants.append(text_file_text)
        else:
            componants.append(file_button)
            componants.append(file_text)

        if isIn(parent.require_keys_algos):
            componants.append(key_input)
            componants.append(key_input_text)

        if isIn(parent.require_output_algos):
            componants.append(output_input)
            componants.append(output_input_text)

    for c in componants:
        build(c)
    for c in built_componants:
        if c not in componants:
            remove(c)



built_componants = []
packed_componatns = []

def build(c):
    if c in built_componants: return
    if isinstance(c[0], OptionMenu):
        c[0].config(borderwidth = 1, bg = "white", relief = "solid", highlightbackground = "white", compound='right', image=arrow, indicatoron=0)
        c[0]["menu"].config(bg = "white", fg = "black")
    elif isinstance(c[0], Text):
        c[0].config(relief = "solid")
    elif isinstance(c[0], Button):
        c[0].config(bg = "white", relief = "solid", overrelief = "solid", borderwidth = 1)
    elif isinstance(c[0], Radiobutton):
        c[0].config(bg = "white", activebackground = "white")
    built_componants.append(c)
    if c not in packed_componatns:
        c[0].pack()
        packed_componatns.append(c)
    c[0].place(relx = c[1], rely = c[2], relwidth = c[3], relheight = c[4])


def remove(c):
    if c not in built_componants: return;
    built_componants.remove(c)
    c[0].place(relx = 5, rely = 5)

def openfile():
    return filedialog.askopenfilename(title = "Select file")

build(mainscreen)
build(finalize_button)
build(_copyright)
master.wm_title("Beschdlcrypt")
master.after(50, update)
master.config(width=1000, height=500, bg = "#FFFFFF")
master.mainloop()
