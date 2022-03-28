import tkinter as tk
from tkinter import Button, ttk
import internetarchive
import os
from os.path import exists
from internetarchive import configure, upload, download
from tkinter import filedialog


def checkusernameexists():
    path = f"C:\\Users\\{os.getlogin()}\\.config\\internetarchive\\ia.ini"
    if (os.path.exists(path)):
        return 1

    return 0



class la:

    def __init__(self) -> None:

        self.root = tk.Tk()
        
        self.frm = ttk.Frame(self.root).grid()
        self.root.title('IA GUI')
        self.root.geometry('800x400')

        self.name_var = tk.StringVar()
        self.passw_var = tk.StringVar()
        self.upload_var = tk.StringVar()
        self.download_var = tk.StringVar()
        self.upload_filevar = tk.StringVar()
        self.download_filevar = tk.StringVar()
        self.identifier = tk.StringVar()

        self.welcome = ttk.Label(
            self.frm, text="Hello! You are using GUI of \n      Internet Archieve", font=('calibre', 20, 'bold'))
        self.welcome.place(x=200, y=100)
        self.loginbutton = Button(
            self.frm, text="Next", command=self.loginclicked)
        self.loginbutton.place(x=350, y=200)
        

    def loginclicked(self):
        self.loginbutton.destroy()
        self.welcome.destroy()
        print(checkusernameexists())
        if not checkusernameexists():

            self.name_label = tk.Label(self.root, text='Mail ID : ', font=('calibre', 10, 'bold'))
            self.name_entry = tk.Entry(self.root, textvariable=self.name_var, font=('calibre', 10, 'normal'))
            self.passw_label = tk.Label(self.root, text='Password :', font=('calibre', 10, 'bold'))
            self.passw_entry = tk.Entry(self.root, textvariable=self.passw_var, font=('calibre', 10, 'normal'))
            self.sub_btn = tk.Button(self.root, text='Login', command=self.submit)
            
            self.name_label.place(x=200, y=100)
            self.name_entry.place(x=300, y=100)
            self.passw_label.place(x=200, y=150)
            self.passw_entry.place(x=300, y=150)
            self.sub_btn.place(x=350, y=200)

       
        else :
            self.home()

    def submit(self):
        self.name = self.name_entry.get()
        self.password = self.passw_entry.get()
        print(self.name, self.password)
        try :
            configure(self.name, self.password)
            self.home()
        except:
            self.wrong = tk.Label(self.root, text='INVALID PASS OR USERNAME', font=('calibre', 10, 'bold')).place(x=280, y=250)
            self.name_var.set("")
            self.passw_var.set("")


    def mainloop(self):
        self.root.mainloop()
    
    def home(self):
        self.root.destroy()
        self.root1 = tk.Tk()
        self.root1.title('IA GUI')
        self.root1.geometry('800x400')
        self.uploadbutton = Button(self.frm, text="Upload", command=self.uploadclicked)
        self.uploadbutton.place(x=300, y=150)
        self.downloadbutton = Button(self.frm, text="Download", command=self.downloadclicked)
        self.downloadbutton.place(x=350, y=150)

    def browseFiles(self):
        self.upload_filevar = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files","*.txt*"),("all files", "*.*")))
                                                       
      
        tk.Label(self.root1, text=self.upload_filevar, font=('calibre', 10, 'bold')).grid(row=1, column=3)

    def uploadclicked(self):
        self.uploadbutton.destroy()
        self.downloadbutton.destroy()

        self.identifier.set("")

        self.upload_label = tk.Label(self.root1, text='Identifier/name', font=('calibre', 10, 'bold'))
        self.identifierg = tk.Entry(self.root1, textvariable=self.identifier, font=('calibre', 10, 'normal'))
        self.nxt_btn = tk.Button(self.root1, text='Upload', command=self.nxt)
        self.upload_filelabel = tk.Label(self.root1, text='File name', font=('calibre', 10, 'bold'))

        self.next_btn = tk.Button(self.root1, text='select file', command=self.browseFiles)
        self.next_btn.grid(row=5, column=4)
        
        self.upload_label.grid(row=4, column=3)
        self.identifierg.grid(row=4, column=4)
        self.nxt_btn.grid(row=6, column=4)
        self.upload_filelabel.grid(row=5, column=3)
        
        
        
    def downloadclicked(self):
        self.uploadbutton.destroy()
        self.downloadbutton.destroy()
        self.download_var.set("ddcdcds")
        self.download_label = tk.Label(self.root1, text='Link', font=('calibre', 10, 'bold'))
        self.download_entry = tk.Entry(self.root1, textvariable=self.download_var,font=('calibre', 10, 'normal'))
        self.next_btn = tk.Button(self.root1, text='Download', command=self.next)

        print(self.download_var)
        self.download_label.grid(row=0, column=0)
        self.download_entry.grid(row=0, column=1)
        self.next_btn.grid(row=2, column=1)

    def nxt(self):

        self.idname = self.identifierg.get()
        print(self.idname)
        self.upload_filevar.replace("\/" , "\\")
        print(self.idname, self.upload_filevar) 
        print(self.identifier.get())
        self.h = f'start cmd /k ia upload {self.idname} "{self.upload_filevar}"'
        print(self.h)
        r = os.system(self.h)
 

    def next(self):
        print(self.download_var)
        self.down = self.download_entry.get()
        print(self.down)
        self.h = f'start cmd /k ia download {self.down}'
        print(self.h)
        r = os.system(self.h)


root = la()
root.mainloop()
