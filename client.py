from colorama import Fore, Back, Style, init
init(autoreset=True)

try:
	import socket
	import os
	from tkinter import *
	from tkinter import simpledialog
	from tkinter import ttk
	import tkinter.messagebox
	import threading
	import win32console, win32gui

except Exception as e:
	print(f"{Back.RED}{Fore.WHITE}[-] Modules are missing --> {e}")
	exit()


try:
	os.system('cls')
except:
	os.system('clear')

def hide():
	window = win32console.GetConsoleWindow()
	win32gui.ShowWindow(window, 0)
	return True

def view():
	window = win32console.GetConsoleWindow()
	win32gui.ShowWindow(window, 1)
	return True

hide()

port = 5050
server = "127.0.0.1" # Server's Ip
nbrchangename = 0

window = Tk()
window.title("Chat")
window.geometry('500x250')
window.resizable(width=False, height=False)

name = simpledialog.askstring("Name", "Please enter your name")
if not name:
	view()
	exit()

chatwindow = Toplevel()
chatwindow.title("Chat")
chatwindow.geometry('600x600')
scrollbar = ttk.Scrollbar(chatwindow)
scrollbar.pack(side=RIGHT, fill="y")

chat = Text(chatwindow,height = 500, width = 350, yscrollcommand = scrollbar.set, wrap = "none")
chat.pack(expand=0, fill= BOTH)
chat.tag_config('info', background="blue", foreground="white")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server, port))

def receive():
	while 1:
		try:
			global message
			message = client.recv(1024).decode()
			if message == "NICK":
				client.send(name.encode())
			else:
				chat.insert(END,message + '\n')
				chat.see(END)
				
		except:
			print(f"{Back.RED}{Fore.WHITE}[-] An error occured")
			view()
			client.close()
			break


def write():
	message = msg.get()
	inputmsg.delete(0, END)
	ilegal_char = ["[", "]"]
	for i in ilegal_char:
		message = message.replace(i, '')

	message = f"{name}: {message}"
	client.send(message.encode())

def changename():
	global name
	global nbrchangename
	if nbrchangename <= 1:
		oldname = name
		name = simpledialog.askstring("New Name", "Please enter your new name")

		message = f"[INFO] {oldname} change nickname to {name}"
		client.send(message.encode())

		nbrchangename += 1
	else:
		tkinter.messagebox.showerror(title="Error", message="You can't change nickname")

def quit():
	client.close()
	view()
	exit()

def on_closing():
	client.close()
	view()
	exit()

menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Changename", command=changename)
filemenu.add_command(label="Quit", command=quit)
menubar.add_cascade(label="Settings", menu=filemenu)

msg = StringVar()

Label(window, text = "Chat", font=("Calibri", 15)).pack(pady=5)
Label(window, text = "").pack()
Label(window, text = "Message : ", font=("Calibri", 12)).pack(pady=4)
inputmsg = Entry(window, textvariable = msg, width = 50)
inputmsg.pack(ipady = 4, pady=2)
Label(window, text = "").pack()
Button(window, text = "Send", width = 10, height = 1, command=write, font=("Calibri", 12)).pack(pady=5)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.config(menu=menubar)
window.mainloop()
