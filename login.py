from logging import root
from tkinter import*
from tkinter import ttk
from tkinter import font
from turtle import bgcolor, left, right, width
import tkinter as tk
import json
from tkinter import messagebox
from nbformat import write
import hashlib
import random 


class signinpage(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("650x600")
        self.title('Sign-in')
        self.config(bg='#669BBC')
        self.resizable(False,False)

        frame2 = Frame(self,bg='#669BBC')
        frame2.place(x=120,y=50,width=550,height=500)

        headline2 = Label(frame2, text='Sign-in', fg='white',bg='#669BBC',font=('Courier',55,'bold'),pady=20).place(x=100)

        txt_email2 = self.labels2(frame2,"Email",120)
        self.email2 = self.entrys2(frame2,185)

        txt_pass2 = self.labels2(frame2, 'Password',240)
        self.password2 = self.entrys2(frame2,300)

        

        btn_login = Button(frame2,text='Register',bg='#F3A712',bd=0,font=('Courier',18),command=self.register).place(x=30,y=380,width=350,height=50)

    def labels2(self,pos,text,y):
        Label(pos,text=text,fg='white',bg='#669BBC',font=('Courier',18),pady=20).place(x=30,y=y)

    def entrys2(self,pos,y):
        entry_obj = Entry(pos,font=('Courier',18,'bold'))
        entry_obj.place(x=30,y=y,width=350,height=45)
        return entry_obj 

    def register(self):
        self.ran = random.randint(0,100)
        email_in = str(self.email2.get())
        pass_in = str(self.password2.get()+str(self.ran))

        hash_obj = hashlib.md5(pass_in.encode())
        md5_hash = hash_obj.hexdigest()

    # python object to be appended
        y = [ {  "password": md5_hash, "salt": self.ran  } ]
        write_json(y,str(email_in))
        self.destroy()
        login()

# function to add to JSON
def write_json(new_data,d, filename='users_data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[d]=(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)


    
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

        txt_email = self.labels(frame,"Email",120)
        self.email = self.entrys(frame,185)

        txt_pass = self.labels(frame, 'Password',240)
        self.password = self.entrys(frame,300)

        btn_login = Button(frame,text='Login',bg='#F3A712',bd=0,font=('Courier',18),command=self.login).place(x=30,y=380,width=350,height=50)
        btn_signin = Button(frame,text='Sign-in',bg='#F3A712',bd=0,font=('Courier',10),command=self.signin).place(x=160,y=450,width=100,height=40)
        

    def labels(self,pos,text,y):
        Label(pos,text=text,fg='white',bg='#669BBC',font=('Courier',18),pady=20).place(x=30,y=y)

    def entrys(self,pos,y):
        entry_obj = Entry(pos,font=('Courier',18,'bold'))
        entry_obj.place(x=30,y=y,width=350,height=45)
        return entry_obj 

    def signin(self):
        signinpage()
        self.destroy()


    def login(self):
        record1 = json.load(open("users_data.json"))          
        pass_list = [ d["password"] for d in record1[str(self.email.get())] ]
        salt_list = [ d["salt"] for d in record1[str(self.email.get())] ]
        for i in salt_list:   
            self.currpass=self.password.get()+str(i)
            hash_obj = hashlib.md5(self.currpass.encode())
            md5_hash = hash_obj.hexdigest()

            if (md5_hash) in pass_list:
                self.destroy()
                root = Tk()
                
            else:
                messagebox.showerror("Error", "Incorrect Email or Password, Please Try Again.")


if __name__ == "__main__":
    obj = login()
    obj.mainloop()