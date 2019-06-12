from tkinter import *
import sqlite3
import os
import pyttsx3

conn = sqlite3.connect('db.db')
c = conn.cursor()
number = []
patients = []
sql = "SELECT ap.id, cl.Name FROM Applications as ap JOIN Clients as cl on ap.Client=cl.id Where ap.Status Not Like ?"
res = c.execute(sql, ("Processed", ))
for r in res:
    ids = r[0]
    name = r[1]
    number.append(ids)
    patients.append(name)
class Application:
    def __init__(self, master):
        self.master = master
        self.x = 0
        self.heading = Label(master, text="Now is bleeding", font=('arial 100 bold'))
        self.heading.place(x=200, y=0)

        self.change = Button(master, text="Next Patient", width=25, height=2, command=self.next_func, bg='#CBE724')
        self.change.place(x=520, y=600)

        self.n=Label(master, text="", font=('arial 200 bold'))
        self.n.place(x=500, y=150)

        self.pname=Label(master, text="", font=('arial 80 bold'))
        self.pname.place(x=480, y=420)

    def next_func(self):
        sql2 = "UPDATE Applications SET Status=? WHERE id like ?"
        c.execute(sql2, ('Processed', number[self.x-1],))
        conn.commit()
        sql3 = "UPDATE Applications SET Status=? WHERE id like ?"
        c.execute(sql3, ('In process', number[self.x],))
        conn.commit()
        self.n.config(text=str(number[self.x]))
        self.pname.config(text=str(patients[self.x]))
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-50)
        engine.say('Client № ' + str(number[self.x]) + str(patients[self.x]))
        engine.runAndWait()
        self.x +=1
root = Tk()
b = Application(root)

root.title("Display")
root.geometry("1360x800+0+0")
root.resizable(False, False)

imgicon = PhotoImage(file=os.path.join('./Images/index4.png'))
root.tk.call('wm', 'iconphoto', root._w, imgicon)
root.mainloop()
