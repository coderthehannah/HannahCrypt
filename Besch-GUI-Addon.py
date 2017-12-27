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
            t = output_box[0].get("1.0","end")
            if str(t)[0] == "\n":
                t = t[1:len(t)]
            output_box[0].delete("1.0", "end")
            arglist = []
            for item in args:
                arglist.append(str(item))
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

_en = IntVar()

current_file = ""

def chosefile(c):
    global current_file
    current_file = openfile().replace("/", "\\")
    filetext = current_file.split("\\")[-1]
    if len(filetext) > 20:
        filetext = filetext[0:15] + "...." + filetext.split(".")[-1]
    c[0].config(text = filetext)

def run():
    toggleOutIn()
    parent.args.algorithm = _type.get()
    if _en.get() == 0:
        ende = ":e"
    else:
        ende = ":d"
    if len(string_input[0].get("1.0","end")[0:-1]) == 0 or _type.get() in parent.file_input_only_algos or _type.get() + ende in parent.file_input_only_algos:
        parent.args.type = parent.file_input
        parent.args.input = current_file
    else:
        parent.args.input = string_input[0].get("1.0","end")[0:-1]
        parent.args.type = parent.raw_input
    parent.args.output = output_input[0].get("1.0","end")[0:-1]
    parent.args.key = key_input[0].get("1.0","end")
    parent.args.encrypt = _en.get() == 0
    parent.args.decrypt = _en.get() == 1
    parent.main()

def toggleOutIn():
    global onOutPutScreen
    output_box[0].delete(1.0, "end")
    onOutPutScreen = not onOutPutScreen

onOutPutScreen = False

mainscreen = OptionMenu(master, _type, *parent.algos), 0.4, 0.1, 0.2, 0.1
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
_copyright = Label(master, text = version + "\nWyn Price 2017", bg = "#FFFFFF"), 0.87, 0.9, 0.15, 0.1

output_box = Text(master), 0.1, 0.05, 0.8, 0.7
output_back = Button(master, text = "back", command = toggleOutIn), 0.4, 0.8, 0.2, 0.1
def update():
    componants = [_copyright]
    if _type.get() in parent.aliases:
        _type.set(parent.aliases[_type.get()])
    master.after(50, update)
    if onOutPutScreen:
        componants.append(output_back)
        componants.append(output_box)
    else:
        componants.append(mainscreen)
        componants.append(finalize_button)
        if _en.get() == 0:
            finalize_button[0].config(text = "Encrypt")
        else:
            finalize_button[0].config(text = "Decrypt")
        if _en.get() == 0:
            ende = ":e"
        else:
            ende = ":d"
        if _type.get() not in parent.non_cript_algos and _type.get() + ende not in parent.non_cript_algos:
            componants.append(en_sel)
            componants.append(de_sel)
        else:
            finalize_button[0].config(text = "Go")

        if _type.get() not in parent.file_input_only_algos and _type.get() + ende not in parent.file_input_only_algos:
            componants.append(string_input)
            componants.append(text_file_button)
            componants.append(text_file_text)
        else:
            componants.append(file_button)
            componants.append(file_text)

        if _type.get() in parent.require_keys_algos or _type.get() + ende in parent.require_keys_algos:
            componants.append(key_input)
            componants.append(key_input_text)

        if _type.get() in parent.require_output_algos or _type.get() + ende in parent.require_output_algos:
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
