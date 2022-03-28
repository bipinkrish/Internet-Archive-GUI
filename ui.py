from re import X
import tkinter as tk
from tkinter import Button, ttk
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
        self.root.resizable(False, False)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (800/2))
        y_cordinate = int((screen_height/2) - (400/2))
        self.root.geometry("{}x{}+{}+{}".format(800, 400, x_cordinate, y_cordinate))

        self.name_var = tk.StringVar()
        self.passw_var = tk.StringVar()
        self.upload_var = tk.StringVar()
        self.download_var = tk.StringVar()
        self.upload_filevar = tk.StringVar()
        self.download_filevar = tk.StringVar()
        self.identifier = tk.StringVar()
        self.backcheck = 0

        self.welcome = ttk.Label(
            self.frm, text="Hello! You are using GUI of \n      Internet Archieve", font=('calibre', 20, 'bold'))
        self.welcome.place(x=200, y=100)
        self.loginbutton = Button(
            self.frm, text="Next", command=self.loginclicked, width=10, height=1)
        self.loginbutton.place(x=350, y=200)

    def loginclicked(self):
        self.loginbutton.destroy()
        self.welcome.destroy()
        print(checkusernameexists())
        if not checkusernameexists():

            self.name_label = tk.Label(
                self.root, text='Mail ID : ', font=('calibre', 10, 'bold'))
            self.name_entry = tk.Entry(
                self.root, textvariable=self.name_var, font=('calibre', 10, 'normal'))
            self.passw_label = tk.Label(
                self.root, text='Password :', font=('calibre', 10, 'bold'))
            self.passw_entry = tk.Entry(
                self.root, textvariable=self.passw_var, font=('calibre', 10, 'normal'))
            self.sub_btn = tk.Button(
                self.root, text='Login', command=self.submit)

            self.name_label.place(x=200, y=100)
            self.name_entry.place(x=300, y=100)
            self.passw_label.place(x=200, y=150)
            self.passw_entry.place(x=300, y=150)
            self.sub_btn.place(x=350, y=200)

        else:
            self.home()

    def submit(self):
        self.name = self.name_entry.get()
        self.password = self.passw_entry.get()
        print(self.name, self.password)
        try:
            configure(self.name, self.password)
            self.home()
        except:
            self.wrong = tk.Label(self.root, text='INVALID PASS OR USERNAME', font=(
                'calibre', 10, 'bold')).place(x=280, y=250)
            self.name_var.set("")
            self.passw_var.set("")

    def mainloop(self):
        self.root.mainloop()

    def home(self):
        if not self.backcheck:
            self.root.destroy()
        self.root1 = tk.Tk()
        self.root1.title('IA GUI')
        self.root1.resizable(False, False)
        screen_width = self.root1.winfo_screenwidth()
        screen_height = self.root1.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (800/2))
        y_cordinate = int((screen_height/2) - (400/2))
        self.root1.geometry("{}x{}+{}+{}".format(800, 400, x_cordinate, y_cordinate))

        self.uploadbutton = Button(
            self.frm, text="Upload", command=self.uploadclicked, width=14, height=4)
        self.uploadbutton.place(x=250, y=150)
        self.downloadbutton = Button(
            self.frm, text="Download", command=self.downloadclicked, width=14, height=4)
        self.downloadbutton.place(x=370, y=150)
        self.logoutbutton = Button(
            self.frm, text="Logout", command=self.logout)
        self.logoutbutton.place(x=700, y=350)
        

        with open(f"C:\\Users\\{os.getlogin()}\\.config\\internetarchive\\ia.ini") as f:
            my_list = list(f)

        ename = my_list[5].split("=")[1][1:-1].split(";")[0].replace("%40","@")
        sename = my_list[9].split("=")[1][1:-1]

        tk.Label(self.root1, text="logged in main: " + ename, font=(
            'calibre', 10, 'bold')).place(x=500,y=10)
        tk.Label(self.root1, text="logged in name: " + sename, font=(
            'calibre', 10, 'bold')).place(x=500,y=30)


    def logout(self):
        os.remove(f"C:\\Users\\{os.getlogin()}\\.config\\internetarchive\\ia.ini")
        self.root1.destroy()

    def browseFiles(self):
        self.upload_filevar = filedialog.askopenfilename(
            initialdir="/", title="Select a File", filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))

        tk.Label(self.root1, text=self.upload_filevar, font=(
            'calibre', 10, 'bold')).place(x=400,y=200)

    def uploadclicked(self):
        self.uploadbutton.destroy()
        self.downloadbutton.destroy()

        self.identifier.set("")

        self.upload_label = tk.Label(
            self.root1, text='Identifier/name', font=('calibre', 10, 'bold'))
        self.identifierg = tk.Entry(
            self.root1, textvariable=self.identifier, font=('calibre', 10, 'normal'))
        self.nxt_btn = tk.Button(self.root1, text='Upload', command=self.nxt, height=1, width=10)
        self.upload_filelabel = tk.Label(
            self.root1, text='File name', font=('calibre', 10, 'bold'))
        self.backbutton = Button(
            self.frm, text="Back", command=self.back)
        self.backbutton.place(x=50, y=350)    

        self.next_btn = tk.Button(
            self.root1, text='select file', command=self.browseFiles, width=7, height=1)
        self.next_btn.place(x=320, y=200)

        self.upload_label.place(x=200, y=150)
        self.identifierg.place(x=320, y=150)
        self.nxt_btn.place(x=340, y=250)
        self.upload_filelabel.place(x=200, y=200)

    def downloadclicked(self):
        self.uploadbutton.destroy()
        self.downloadbutton.destroy()
        self.download_var.set("ddcdcds")
        self.download_label = tk.Label(
            self.root1, text='Identifier: ', font=('calibre', 10, 'bold'))
        self.download_entry = tk.Entry(
            self.root1, textvariable=self.download_var, font=('calibre', 10, 'normal'))
        self.next_btn = tk.Button(
            self.root1, text='Download', command=self.next, width=10, height=1)
        self.backbutton = Button(
            self.frm, text="Back", command=self.back)
        self.backbutton.place(x=50, y=350)    

        self.download_label.place(x=250,y=150)
        self.download_entry.place(x=330,y=150)
        self.next_btn.place(x=300,y=200)

    def nxt(self):

        self.idname = self.identifierg.get()
        print(self.idname)
        self.upload_filevar.replace("\/", "\\")
        print(self.idname, self.upload_filevar)
        print(self.identifier.get())

        with open(f"C:\\Users\\{os.getlogin()}\\.config\\internetarchive\\ia.ini") as f:
            my_list = list(f)

        access_key = my_list[1].split("=")[1][1:-1]
        secret_key = my_list[2].split("=")[1][1:-1]

        try:
            upload(identifier=self.idname, files=self.upload_filevar, access_key=access_key,
                   secret_key=secret_key, verbose=1, validate_identifier=1)
        except:
            print("error")

    def next(self):

        self.down = self.download_entry.get()
        download(identifier=self.down)

    def back(self):
        self.backcheck = 1
        self.root1.destroy()
        self.home()
        

root = la()
root.mainloop()