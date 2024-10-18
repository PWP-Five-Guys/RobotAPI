from Login.login import *
import subprocess
from tkinter import Tk

if __name__ == '__main__':
    process = subprocess.Popen(['python', 'api.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    root = Tk()
    login_class = Login(root)
    root.mainloop()