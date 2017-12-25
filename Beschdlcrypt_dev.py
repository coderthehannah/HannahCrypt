from tkinter import *
import sys
import os


try:
    import Beschdlcrypt_start
except ImportError:
    print("Main script not found. Aborting!")
    sys.exit()
import Beschdlcrypt_start as parent

######### API stuff
class APIListener:
    isActive = False
    def onPrint(self, *args):
        print(*args)

    def activate(self):
        isActive = True


parent.addListener(APIListener())
master = Tk()

_type = StringVar(master)
_type.set("Choose A Method")

_ende = StringVar(master)
_ende.set("Encrypt")

mainscreen = OptionMenu(master, _type, *parent.algos), 0.4, 0.1, 0.2, 0.1
en_de_select = OptionMenu(master, _ende, "Encrypt", "Decrypt"), 0.7, 0.5, 0.15, 0.1


def update():
    master.after(50, update)
    if _type.get() not in parent.non_cript_algos:
        build(en_de_select)
    else:
        remove(en_de_select)

built_componants = []
packed_componatns = []

def build(c):
    if c in built_componants: return
    built_componants.append(c)
    if c not in packed_componatns:
        c[0].pack()
        packed_componatns.append(c)
    c[0].place(relx = c[1], rely = c[2], relwidth = c[3], relheight = c[4])

def remove(c):
    if c not in built_componants: return;
    built_componants.remove(c)
    c[0].place(relx = 5, rely = 5)

build(mainscreen)
master.wm_title("Beschdlcrypt")
master.after(50, update)
master.config(width=1000, height=500, bg = "#f49e42")
master.mainloop()
