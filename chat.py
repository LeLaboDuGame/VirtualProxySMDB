import socket
import threading
import time


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# THREAD RECEIVE
class ReceiveThreading(threading.Thread):
    def __init__(self, conn, send_thread=None, storage=None, is_server=False, pseudo_exist=None):
        threading.Thread.__init__(self)
        self.send_thread = send_thread
        self.storage = storage
        self.is_server = is_server
        self.conn = conn
        self.pseudo_exist = pseudo_exist

    def run(self):
        while True:
            data = self.conn.recv(1024)
            data = data.decode("utf8")
            print(data)
            data = data.split("¤¤¤")
            info = data[0]
            msg = data[1]

            if self.storage is not None:
                self.storage.set_data([info, msg])
            if info[0] == "|":
                if self.is_server and info == "|SET_USER_PSEUDO|":
                    if self.pseudo_exist(msg):
                        self.conn.send(f"|ERROR|¤¤¤NAME_ALREADY_EXIST".encode("utf8"))
                    else:
                        self.conn.send(f"|USER_PSEUDO_ACCEPT|¤¤¤{msg}".encode("utf8"))
                if not self.is_server and info == "|ERROR|":
                    print(f"{bcolors.FAIL}ERROR : {bcolors.ENDC}{msg}")

            else:
                print(f"\n{bcolors.OKBLUE}{info}{bcolors.ENDC} : {msg}")

                if self.is_server:
                    self.send_thread.send_msg(info, msg)


# THREAD SEND
class SendThreading(threading.Thread):
    def __init__(self, server, is_server=False):
        threading.Thread.__init__(self)
        self.is_server = is_server
        self.server = server
        self.conns = []
        self.pseudo = "ANONYMOUS"

    def set_pseudo(self, storage):
        if not self.is_server:
            pseudo = ""
            while storage.get_data()[0] != "|USER_PSEUDO_ACCEPT|" and storage.get_data()[1] != self.pseudo:
                pseudo = input(f"Entrer votre {bcolors.OKBLUE}pseudo{bcolors.ENDC} >>> ")
                self.server.sendall(f"|SET_USER_PSEUDO|¤¤¤{pseudo}".encode("utf8"))
            self.pseudo = pseudo
            print(f"\n##########################{bcolors.WARNING}BIENVENUE{bcolors.ENDC}##########################"
                  f"\n\n# Bienvenue sur le chat {bcolors.OKGREEN}{pseudo}{bcolors.ENDC}. Veuillez ne pas employer un "
                  f"language {bcolors.FAIL}vulgaire{bcolors.ENDC}.\n"
                  f"# Sachez que ce programme n'est pas parfait et ne fonctionne pas très bien mdr.\n"
                  f"# De plus je vous déconseille de l'utiliser {bcolors.WARNING}pendant les cours{bcolors.ENDC}.\n"
                  f"# Le programme ne fonctionne que en {bcolors.OKCYAN}réseau local{bcolors.ENDC} c'est à dire "
                  f"{bcolors.OKCYAN}lan{bcolors.ENDC} c'est à dire que sur \n"
                  f"le meme {bcolors.OKCYAN}wifi{bcolors.ENDC}.\n"
                  f"# {bcolors.WARNING}Si vous n'êtes pas connecter au wifi de l'enceinte du bâtiment (ou autre réseau local),\n"
                  f"la connexion n'aboutira pas.{bcolors.ENDC}"
                  f"\n#############################{bcolors.FAIL}MERCI{bcolors.ENDC}#############################\n")
        else:
            self.pseudo = input(f"Entrer votre {bcolors.OKBLUE}pseudo{bcolors.ENDC} >>> ")

    def send_msg(self, info, msg):
        if self.is_server:
            for conn in self.conns:
                conn.send(f"{info}¤¤¤{msg}".encode("utf8"))
        else:
            self.server.send(f"{info}¤¤¤{msg}".encode("utf8"))

    def start_send_msg(self):
        msg = ""
        while msg != "STOP":
            time.sleep(0.2)
            msg = input("Entrer votre msg >>> ")
            if self.is_server:
                print(f"\n{bcolors.OKBLUE}{self.pseudo}{bcolors.ENDC} : {msg}")
            self.send_msg(self.pseudo, msg)
        self.server.close()

    def run(self):
        self.start_send_msg()


# SERVER
def start_server(server):
    host, port = ('', 33)
    server.bind((host, port))
    print("Le serveur est bien démarré !")

    # Start du thread en charge d'envoyer des msg
    send_thread = SendThreading(server, is_server=True)
    send_thread.set_pseudo(None)
    send_thread.start()

    pseudos = []

    def pseudo_exist(pseudo):
        print(f";{pseudo};")
        if pseudo in pseudos:
            return True
        else:
            pseudos.append(pseudo)

    while True:
        server.listen(20)
        conn, addr = server.accept()
        send_thread.conns.append(conn)

        print(f"\n{bcolors.OKBLUE}{addr[1]} {bcolors.ENDC}:{bcolors.OKBLUE} connected !{bcolors.ENDC}")

        # Start du thread en charge de recevoir les msg
        rcv_thread = ReceiveThreading(conn, send_thread=send_thread, is_server=True, pseudo_exist=pseudo_exist)
        rcv_thread.start()

    server.close()
    conn.close()


class Storage:
    def __init__(self, data=None):
        self.data = data

    def set_data(self, data):
        self.data = data

    def get_data(self):
        time.sleep(0.3)
        return self.data


# ------------------------------------------------------------------------------------

# Test si un server est déjà existant
try:
    # CLIENT
    print("En recherche d'un serveur déjà existant...")
    host, port = ('https://virtualproxysmdb.onrender.com', 33)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, port))
    print("Client connecté !")
    # Start du thread en charge de recevoir les msg

    storage = Storage(["", ""])

    rcv_thread = ReceiveThreading(server, storage=storage)
    rcv_thread.start()

    # Start du thread en charge d'envoyer des msg
    send_thread = SendThreading(server)
    send_thread.set_pseudo(storage=storage)
    send_thread.start()
except:  # Sinon start le server
    print("\nServer non trouvé\nCréation du server...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    start_server(server)
