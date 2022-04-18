from cProfile import label
from cgitb import text
from logging import root
from tkinter import*
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from turtle import bgcolor, left, right, width
import tkinter as tk
import json
from tkinter import messagebox
from nbformat import write
import hashlib
import random 
import rsa
import socket
import os

HOST_IP = "localhost"
Port_NO = 9999

#mainpage you can select either send or recieve
class mainpage(Tk):
    def __init__(self,user):
        #create screen layout
        super().__init__()
        self.user=user
        self.geometry("650x600")
        self.title('Main page')
        self.config(bg='#669BBC')
        self.resizable(False,False)
        frame = Frame(self,bg='#669BBC')
        frame.place(x=120,y=50,width=650,height=600)
        #create buttones
        headline = Label(frame, text='Please select option.', fg='white',bg='#669BBC',font=('Courier',30,'bold'),pady=0).place(x=0,y=50)
        btn_send = Button(frame,text='Send',bg='#F3A712',bd=0,font=('Courier',18),command=self.send).place(x=50,y=120,width=350,height=50)
        btn_recive = Button(frame,text='Receive',bg='#F3A712',bd=0,font=('Courier',18),command=self.recieve).place(x=50,y=200,width=350,height=50)
        btn_back = Button(frame,text='Back',bg='#F3A712',bd=0,font=('Courier',10),command=self.back_btn).place(x=0,y=0,width=60,height=30)
        #back to previous page
    def back_btn(self):
        login()
        self.destroy()
        #go to send page
    def send(self):
        sender(self.user)
        self.destroy()
        #go to recieve page
    def recieve(self):
        reciever(self.user)
        self.destroy()


class sender(Tk):
    def __init__(self,user):
        #create screen layout
        super().__init__()
        self.user=user
        self.geometry("650x600")
        self.title('Send')
        self.config(bg='#669BBC')
        self.resizable(False,False)
        frame = Frame(self,bg='#669BBC')
        frame.place(x=120,y=50,width=650,height=600)
        #create buttones       
        headline = Label(frame, text='What you want to send.', fg='white',bg='#669BBC',font=('Courier',25,'bold'),pady=0).place(x=0,y=50)
        btn_send = Button(frame,text='Send file',bg='#F3A712',bd=0,font=('Courier',18),command=self.file).place(x=50,y=150,width=350,height=50)
        btn_send2 = Button(frame,text='Send Text',bg='#F3A712',bd=0,font=('Courier',18),command=self.text).place(x=50,y=250,width=350,height=50)
        btn_back = Button(frame,text='Back',bg='#F3A712',bd=0,font=('Courier',10),command=self.back_btn).place(x=0,y=0,width=60,height=30)
        #back to previous page        
    def back_btn(self):
        mainpage(self.user)
        self.destroy()
        #go to send file page
    def file(self):
        send_file(self.user)
        self.destroy()
        #go to send txt page
    def text(self):
        send_text(self.user)
        self.destroy()

class send_file(Tk):
    def __init__(self,user):
         #create screen layout       
        super().__init__()
        self.user=user
        self.geometry("650x600")
        self.title('Send File')
        self.config(bg='#669BBC')
        self.resizable(False,False)
        frame = Frame(self,bg='#669BBC')
        frame.place(x=120,y=50,width=650,height=600)
        #create buttones 
        headline = Label(frame, text='Upload File.', fg='white',bg='#669BBC',font=('Courier',25,'bold'),pady=0).place(x=100,y=50)
        btn_dir = Button(frame,text='Choose file',bg='#F3A712',bd=0,font=('Courier',18),command=self.dialoge).place(x=50,y=50,width=350,height=50)
        btn_send = Button(frame,text='Send',bg='#F3A712',bd=0,font=('Courier',10),command=self.send_to).place(x=180,y=150,width=100,height=40)
        self.path_lbl = Label(frame, fg='red',bg='white',relief=RAISED)
        self.path_lbl.pack(pady=110)
        self.path_lbl.place(x=130,y=110)
        btn_back = Button(frame,text='Back',bg='#F3A712',bd=0,font=('Courier',10),command=self.back_btn).place(x=0,y=0,width=60,height=30)
        #back to previous page       
    def back_btn(self):
        sender(self.user)
        self.destroy()
        # open file ecplorer to chooce file
    def dialoge(self):
        self.file_path = filedialog.askopenfilename(filetypes=[('All types','*.*')]) #file path
        self.path_lbl.config(text=self.file_path)
        #send the file to reciever
    def send_to(self):
        reciever(self.user).fi_not()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST_IP, Port_NO))
        self.server.listen()
        self.client_socket, self.address = self.server.accept()
        #send file name
        self.client_socket.send(self.file_path.encode())
        #open and read the file 
        with open(self.file_path,"rb") as file:
            self.data = file.read(1024)
            self.client_socket.sendall(self.data)
        self.client_socket.close()



class send_text(Tk):
    
    def __init__(self,user):
         #create screen layout    
        super().__init__()
        self.user=user
        self.geometry("650x600")
        self.title('Send Text')
        self.config(bg='#669BBC')
        self.resizable(False,False)
        frame = Frame(self,bg='#669BBC')
        frame.place(x=120,y=50,width=650,height=600)
        #create buttones 
        headline = Label(frame, text='write your text here.', fg='white',bg='#669BBC',font=('Courier',25,'bold'),pady=0).place(x=30,y=50)
        self.txt= tk.Entry(frame,width=35, font = ('arial',18,'bold'))
        self.txt.grid()
        self.txt.place(y=90)
        btn_send = Button(frame,text='Send',bg='#F3A712',bd=0,font=('Courier',10),command=self.send_to).place(x=120,y=150,width=100,height=40)
        btn_clr = Button(frame,text='Clear',bg='#F3A712',bd=0,font=('Courier',10),command=self.clr).place(x=240,y=150,width=100,height=40)
        btn_back = Button(frame,text='Back',bg='#F3A712',bd=0,font=('Courier',10),command=self.back_btn).place(x=0,y=0,width=60,height=30)
        #back to previous page 
    def back_btn(self):
        sender(self.user)
        self.destroy()
        # send text to reciever
    def send_to(self):
        reciever().txt_not()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST_IP, Port_NO))
        self.server.listen()
        self.client_socket, self.address = self.server.accept()
        self.client_socket.send(bytes(self.txt.get(),"utf-8"))
        self.client_socket.close()
        #clear text entery 
    def clr(self):
        self.txt.delete(0,END)
    


class reciever(Tk):
    def __init__(self,user):
         #create screen layout  
        super().__init__()
        self.user=user
        self.geometry("650x600")
        self.title('Recieve')
        self.config(bg='#669BBC')
        self.resizable(False,False)
        frame = Frame(self,bg='#669BBC')
        frame.place(x=120,y=50,width=650,height=600)
        #create buttones 
        headline = Label(frame, text='What you want to receive.', fg='white',bg='#669BBC',font=('Courier',25,'bold'),pady=0).place(x=0,y=50)
        btn_recieve = Button(frame,text='receive file',bg='#F3A712',bd=0,font=('Courier',18),command=self.file).place(x=50,y=120,width=350,height=50)
        btn_recieve2 = Button(frame,text='receive Text',bg='#F3A712',bd=0,font=('Courier',18),command=self.text).place(x=50,y=220,width=350,height=50)
        btn_back = Button(frame,text='Back',bg='#F3A712',bd=0,font=('Courier',10),command=self.back_btn).place(x=0,y=0,width=60,height=30)
        #back to previous page        
    def back_btn(self):
        mainpage(self.user)
        self.destroy()
        #go to recieve file page
    def file(self):
        receive_file(self.user)
        self.destroy()
        #go to recieve text page
    def text(self):
        receive_text(self.user)
        self.destroy()
        #notify if file recieved
    def fi_not(self):
        self.destroy()
        messagebox.showinfo('Recieve msg','You have received one file , please select "Recieve file " and choose the path')
        #notify if text recieved        
    def txt_not(self):
        self.destroy()
        messagebox.showinfo('Recieve msg','You have received one text , please select "Recieve text " and click on Recieve')

class receive_file(Tk):
    def __init__(self,user):
         #create screen layout  
        super().__init__()
        self.user=user
        self.geometry("650x600")
        self.title('file recieve')
        self.config(bg='#669BBC')
        self.resizable(False,False)
        frame = Frame(self,bg='#669BBC')
        frame.place(x=120,y=50,width=650,height=600)
        #create buttones 
        headline = Label(frame, text='Select Folder.', fg='white',bg='#669BBC',font=('Courier',25,'bold'),pady=0).place(x=100,y=50)
        btn_dir = Button(frame,text='Choose Folder',bg='#F3A712',bd=0,font=('Courier',18),command=self.dialoge).place(x=50,y=50,width=350,height=50)
        btn_save = Button(frame,text='Save',bg='#F3A712',bd=0,font=('Courier',10),command=self.save_to).place(x=180,y=150,width=100,height=40)
        self.path_lbl = Label(frame, fg='red',bg='white',relief=RAISED)
        self.path_lbl.pack(pady=110)
        self.path_lbl.place(x=170,y=110)
        btn_back = Button(frame,text='Back',bg='#F3A712',bd=0,font=('Courier',10),command=self.back_btn).place(x=0,y=0,width=60,height=30)
       #back to previous page        
    def back_btn(self):
        reciever(self.user)
        self.destroy()
        #open file explorer to choose folder path
    def dialoge(self):
        self.folder = filedialog.askdirectory() #folder path
        self.path_lbl.config(text=self.folder)
        #save the file in folder
    def save_to(self):
        self.client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connection.connect((HOST_IP, Port_NO))
        #recieve file name
        self.filename = self.client_connection.recv(1024).decode()
        #open and write the file
        with open(str(self.folder)+"/"+str(os.path.basename(self.filename)),"wb") as file:
            self.data = self.client_connection.recv(1024)
            file.write(self.data)

        self.client_connection.close()

class receive_text(Tk):
    global_msgb = ""
    def __init__(self,user):
         #create screen layout  
        super().__init__()
        self.user=user
        self.geometry("650x600")
        self.title('login')
        self.config(bg='#669BBC')
        self.resizable(False,False)
        frame = Frame(self,bg='#669BBC')
        frame.place(x=120,y=50,width=650,height=600)
        #create buttones
        headline = Label(frame, text='Cipher Text.', fg='white',bg='#669BBC',font=('Courier',25,'bold'),pady=0).place(x=100,y=50)
        self.txt= Text(frame,width=30,height=0, font = ('arial',20,'bold'))
        self.txt.pack()
        self.txt.place(y=90)
        btn_rec = Button(frame,text='Recieve',bg='#F3A712',bd=0,font=('Courier',10),command=self.rec_to).place(x=120,y=140,width=100,height=40)
        btn_clr = Button(frame,text='Clear',bg='#F3A712',bd=0,font=('Courier',10),command=self.clr).place(x=240,y=140,width=100,height=40)
        headline2 = Label(frame, text='Plain Text.', fg='white',bg='#669BBC',font=('Courier',25,'bold'),pady=0).place(x=100,y=300)
        self.txt2= Text(frame,width=30,height=0, font = ('arial',20,'bold'))
        self.txt2.pack()
        self.txt2.place(y=350)
        btn_rec2 = Button(frame,text='Recieve',bg='#F3A712',bd=0,font=('Courier',10),command=self.rec_to2).place(x=120,y=400,width=100,height=40)
        btn_clr2 = Button(frame,text='Clear',bg='#F3A712',bd=0,font=('Courier',10),command=self.clr2).place(x=240,y=400,width=100,height=40)
        btn_back = Button(frame,text='Back',bg='#F3A712',bd=0,font=('Courier',10),command=self.back_btn).place(x=0,y=0,width=60,height=30)
       #back to previous page           
    def back_btn(self):
        reciever(self.user)
        self.destroy()
        #recieve text and write the cipher text
    def rec_to(self):
        self.client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connection.connect((HOST_IP, Port_NO))
        self.message = self.client_connection.recv(1024).decode()
        self.global_msg=self.message
        self.txt.insert(1.0,self.message)
        self.client_connection.close()
       #clear text  1
    def clr(self):
        self.txt.delete(1.0,END)
        #write plain text 
    def rec_to2(self):
        self.txt2.insert(1.0,self.global_msg)
        #clear text 2
    def clr2(self):
        self.txt2.delete(1.0,END)


class signinpage(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("650x600")
        self.title('Sign-in')
        self.config(bg='#669BBC')
        self.resizable(False,False)

        self.frame2 = Frame(self,bg='#669BBC')
        self.frame2.place(x=120,y=50,width=550,height=500)

        self.headline2 = Label(self.frame2, text='Sign-in', fg='white',bg='#669BBC',font=('Courier',55,'bold'),pady=20).place(x=100)

        self.txt_email2 = Label(self.frame2,text='Username',fg='white',bg='#669BBC',font=('Courier',18),pady=20).place(x=30,y=120)
        self.email2 = Entry(self.frame2,font=('Courier',18,'bold'))
        self.email2.place(x=30,y=185,width=350,height=45)

        self.txt_pass2 = Label(self.frame2,text='Password',fg='white',bg='#669BBC',font=('Courier',18),pady=20).place(x=30,y=240)
        self.password2 = Entry(self.frame2,font=('Courier',18,'bold'))
        self.password2.place(x=30,y=300,width=350,height=45)

        self.btn_login = Button(self.frame2,text='Register',bg='#F3A712',bd=0,font=('Courier',18),command=self.register).place(x=30,y=380,width=350,height=50)


    def register(self):

        self.ran = random.randint(0,100)
        self.email_in = str(self.email2.get())
        self.pass_in = str(self.password2.get()+str(self.ran))

        self.hash_obj = hashlib.md5(self.pass_in.encode())
        self.md5_hash = self.hash_obj.hexdigest()

    # python object to be appended
        self.data = [ {  "password": self.md5_hash, "salt": self.ran  } ]
        self.write_json(self.data,str(self.email_in),'users_data.json')
        self.generate_keys()
        self.destroy()
        login()

    # function to add to JSON
    def write_json(self,new_data,email, filename):
        with open(filename,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data[email]=(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
    
    def generate_keys(self):
        #create pri and pub keys
        (self.publickey,self.privatekey) = rsa.newkeys(1025)
        print(type(self.publickey))

        #write pub key in file
        self.pubkey = open(f"{self.email_in}PublicKey.key",'wb')
        self.pubkey.write(self.publickey.save_pkcs1('PEM'))
        self.pubkey.close()

        #write pri key in file
        self.prikey = open(f"{self.email_in}PrivateKey.key",'wb')
        self.prikey.write(self.privatekey.save_pkcs1('PEM'))
        self.prikey.close()
        


    
class login(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("650x600")
        self.title('login')
        self.config(bg='#669BBC')
        self.resizable(False,False)

        frame = Frame(self,bg='#669BBC')
        frame.place(x=120,y=50,width=550,height=500)

        headline = Label(frame, text='Login', fg='white',bg='#669BBC',font=('Courier',55,'bold'),pady=20).place(x=100)

        txt_email = Label(frame,text="Username",fg='white',bg='#669BBC',font=('Courier',18),pady=20).place(x=30,y=120)
        self.email = Entry(frame,font=('Courier',18,'bold'))
        self.email.place(x=30,y=185,width=350,height=45)

        txt_pass = Label(frame,text='Password',fg='white',bg='#669BBC',font=('Courier',18),pady=20).place(x=30,y=240)
        self.password = Entry(frame,font=('Courier',18,'bold'))
        self.password.place(x=30,y=300,width=350,height=45)

        btn_login = Button(frame,text='Login',bg='#F3A712',bd=0,font=('Courier',18),command=self.login).place(x=30,y=380,width=350,height=50)
        btn_signin = Button(frame,text='Sign-in',bg='#F3A712',bd=0,font=('Courier',10),command=self.signin).place(x=160,y=450,width=100,height=40)

    def signin(self):
        signinpage()
        self.destroy()

    # this function will check if the user registered or not if it is register it will login into home page
    def login(self):
        record1 = json.load(open("users_data.json"))          
        pass_list = [ d["password"] for d in record1[str(self.email.get())] ]
        salt_list = [ d["salt"] for d in record1[str(self.email.get())] ]
        for i in salt_list:   
            self.currpass=self.password.get()+str(i)
            hash_obj = hashlib.md5(self.currpass.encode())
            md5_hash = hash_obj.hexdigest()

            if (md5_hash) in pass_list:
                self.user=self.email.get()
                self.destroy()
                mainpage(self.user)
                
            else:
                messagebox.showerror("Error", "Incorrect Email or Password, Please Try Again.")


if __name__ == "__main__":
    obj = login()
    obj.mainloop()

