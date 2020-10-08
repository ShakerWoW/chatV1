from colorama import Fore, Back, Style, init
init(autoreset=True)

try:
	import socket
	import time
	import os
	import threading
except Exception as e:
	print(f"{Back.RED}{Fore.WHITE}[-] Modules are missing --> {e}")
	exit()


try:
	os.system('cls')
except:
	os.system('clear')

port = 5050
server = "192.168.1.109"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen()
print(f"{Back.GREEN}{Fore.WHITE}[+] Server is listening on {server}")

clients = []
nicknames = []

def broadcast(message):
	for client in clients:
		client.send(message)

def handle(client):
	while 1:
		try:
			message = client.recv(1024)
			broadcast(message)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			broadcast(f"{nickname} left the chat".encode())
			nicknames.remove(nickname)
			break

def receive():
	while 1:
		client, addr = s.accept()
		print(f"{Back.GREEN}{Fore.WHITE}[+] New Connection with {str(addr)}")

		client.send("NICK".encode())
		nickname = client.recv(1024).decode()
		nicknames.append(nickname)
		clients.append(client)

		print(f"{Back.BLUE}{Fore.WHITE}[INFO] Nickname of the client is {nickname}")
		broadcast(f"{nickname} joined the chat".encode())
		client.send("Connected to the server".encode())

		thread = threading.Thread(target=handle, args=(client,))
		thread.start()
		print(f"{Back.BLUE}{Fore.WHITE}[INFO] Active connection : {threading.activeCount() - 1}")

receive()