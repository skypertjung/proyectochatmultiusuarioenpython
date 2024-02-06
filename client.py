import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText

def send_message( client_socket, username, text_widget, entry_widget ):
    message = entry_widget.get()
    client_socket.sendall(f"{username} > {message}".encode())

    entry_widget.delete(0, END)
    text_widget.configure(state='normal')
    text_widget.insert(END, f"{username} > {message}\n")
    text_widget.configure(state='disable')
def recive_message(client_socket, text_widget):
    while True:
        try:
            message = client_socket.recv(1024).encode()
            if not message:
                break
            text_widget.configure(state='normal')
            text_widget.insert(END, message)
            text_widget.configure(state='disable')
        except:
            break

def list_user_request(client_socket):
    client_socket.sendall("!usuarios".encode())

def exit_request(client_socket, username, windows):
    client_socket.sendall(f"\n[!] El usuario {username} ha abandonado el chat\n\n".encode())
    client_socket.close()

    windows.quit()
    windows.destroy()

def client_program():
    host = 'localhost'
    port = 1234
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    username = input(f"\n[+] Introduce tu usuario: ")
    client_socket.sendall(username.encode())

    windows = Tk()
    windows.title("Chat")

    text_widget = ScrolledText(windows, state='disabled')
    text_widget.pack(padx=5, pady=5)

    frame_widget = Frame(windows)
    frame_widget.pack(padx=5, pady=2, fill=BOTH, expand=1)

    entry_widget = Entry(frame_widget)
    entry_widget.bind("<Return>", lambda _: send_message(client_socket, username, text_widget, entry_widget))
    entry_widget.pack(side=LEFT, fill=X, expand=1)


    button_wiget = Button(frame_widget, text="Enviar", command=lambda: send_message(client_socket, username, text_widget, entry_widget))
    button_wiget.pack(side=RIGHT, padx=5)

    user_wiget = Button(frame_widget, text="Listar usuarios", command=lambda: list_user_request(client_socket))
    user_wiget.pack(side=RIGHT, padx=5)

    exit_wiget = Button(frame_widget, text="Salir", command=lambda: exit_request(client_socket, username, windows))
    exit_wiget.pack(side=RIGHT, padx=5)

    thread = threading.Thread(target=recive_message, args=(client_socket, text_widget))
    thread.daemon = True
    thread.start()

    windows.mainloop()
    client_socket.close()

if __name__ == '__main__':
    client_program()