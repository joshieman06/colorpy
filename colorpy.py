import tkinter as tk
import pyperclip as clip
from PIL import ImageTk, ImageEnhance, Image
from pynput import keyboard
from pynput.keyboard import Listener as KeyboardListener
import PIL.ImageGrab
import pyautogui as pag
import time

COMBINATIONS = [
    {keyboard.Key.alt_l, keyboard.KeyCode(char='a')}
]

current = set()
clicked = 0

def execute():
    global w, h, pix
    im = PIL.ImageGrab.grab()
    pix = im.load()
    w, h = im.size
    enhancer = ImageEnhance.Brightness(im)
    im = enhancer.enhance(0.5)
    global window
    window = tk.Tk()
    window.geometry(f"{w}x{h}")
    canvas = tk.Canvas(window,width=w,height=h)
    canvas.configure(background="black")
    window.title("Colorpy")
    window.attributes("-topmost", True)
    window.bind('<Button-1>',on_click)
    window.bind('<Escape>',esc)
    window['bg'] = '#1B1B1B'
    window.attributes('-fullscreen', True)
    window.overrideredirect(True)
    window.config(cursor="tcross")
    im = ImageTk.PhotoImage(im)
    image = canvas.create_image(w/2,h/2,anchor='center',image=im)
    canvas.pack()
    window.after(10, click)
    window.mainloop()

def click():
    pag.click()

def on_click(event):
    if 'window' in globals():
        global clicked, hex
        if clicked == 0:
            clicked = 1
        else:
            clicked = 0
            global fin
            hex = '#%02x%02x%02x' % pix[pag.position()[0], pag.position()[1]]
            window.destroy()
            fin = tk.Tk()
            fin.attributes("-topmost", True)
            fin.overrideredirect(True)
            fin['bg'] = hex
            fin.geometry(f"{round(w/7)}x{round(h/7)}")
            label = tk.Label(fin, background="white", text=hex, font=('Courier', 20))
            label.pack()
            label.place(relx=.5, rely=.5, anchor="c")
            r, g, b = pix[pag.position()[0], pag.position()[1]]
            listrgb = [r, g, b]
            gs = sum(listrgb)/len(listrgb)
            if gs >= 126:
                color = 'black'
            else:
                color = 'white'
            input = tk.Label(fin, background=hex, text="RClick: Copy    LClick: Close", font=('Courier', 10), fg=color)
            input.pack()
            input.place(relx=0.5,rely=1.0,anchor='s')
            fin.bind("<Button-1>",on_click2)
            fin.bind("<Button-3>",on_click3)
            fin.eval(f'tk::PlaceWindow {str(fin)} center')
            fin.mainloop()

def on_click2(event):
    time.sleep(0.1)
    fin.destroy()

def on_click3(event):
    clip.copy(str(hex))
    time.sleep(0.1)
    fin.destroy()

def esc(event):
    global clicked
    time.sleep(0.1)
    window.destroy()
    clicked = 0
    
def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if str(current) == "{'a', <Key.alt_l: <164>>}" or str(current) == "{<Key.alt_l: <164>>, 'a'}":
            execute()
            current.clear()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)


with KeyboardListener(on_press=on_press, on_release=on_release) as kl:
    kl.join()



