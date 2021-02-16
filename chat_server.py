import socket
import threading

class chat_server():
    def __init__(self,bind_address,bind_port=1234,address_type=socket.AF_INET,protocol=socket.SOCK_DGRAM):
        # Address Type Where this program will get and recieve data By default it will use ipv4 address type because we already give 'soket.AF_INET'
        # 'socket.AF_INET' is for ipv4 address
        self.address_type = address_type
        # Program will use by default UDP (User Diagram Protocol) 'soket.SOCK_DGRAM' is for UDP
        self.protocol = protocol
        # Address 
        chat_server.bind_address = bind_address
        # Port where this program will work
        chat_server.bind_port = bind_port
        self.platform = socket.socket(self.address_type,self.protocol)
        self.platform.bind((bind_address,bind_port))
        # This  chat_server.stop_sending variable decide that Program will ask for next IP for chat
        chat_server.stop_sending = True
        chat_server.msg_receive = threading.Thread(target=self.receive,args=())
        chat_server.msg_receive.start()
        
    def UserCreation(self,ip):
        if ip not in chat_server.msg.keys():
            chat_server.msg[ip] ={"chat":[],"pending":[]}
        
    def receive(self):
        chat_server.msg={}
        while True:
            try:
                self.UserCreation(chat_server.current_user_ip)
                msg = self.platform.recvfrom(1024)
                if msg[1][0] == chat_server.bind_address:
                    break
                self.UserCreation(msg[1][0])
                chat_msg = "{0} : {1}".format(msg[1][0],msg[0].decode())
                if chat_server.current_user_ip == msg[1][0]:
                    print(chat_msg)
                    chat_server.msg[chat_server.current_user_ip]["chat"].append(chat_msg)
                else:
                    chat_server.msg[msg[1][0]]["pending"].append(chat_msg)
            except AttributeError:
                pass

    def start_session(self,dest_ip,dest_port=1234):
        chat_server.current_user_ip = dest_ip
        chat_server.current_user_port = dest_port
        chat_server.msg_send = threading.Thread(target=self.send,args=())
        self.UserCreation(chat_server.current_user_ip)
        if dest_ip == chat_server.bind_address:
            self.platform.sendto("Exit".encode(),(chat_server.current_user_ip,chat_server.current_user_port))
        else:
            # If condition Code Will Print previous Chat Server and Pending Messages , Messages which recieve for a user when program will bus to see another user messages
            if chat_server.current_user_ip in chat_server.msg.keys():
                if len(chat_server.msg[chat_server.current_user_ip]["chat"]) !=0:
                    print("\n".join(chat_server.msg[chat_server.current_user_ip]["chat"]))
                if len(chat_server.msg[chat_server.current_user_ip]["pending"]) !=0:
                    print("\n".join(chat_server.msg[chat_server.current_user_ip]["pending"]))
                    chat_server.msg[chat_server.current_user_ip]["chat"] = chat_server.msg[chat_server.current_user_ip]["chat"] + chat_server.msg[chat_server.current_user_ip]["pending"]
                    chat_server.msg[chat_server.current_user_ip]["pending"] = []
            chat_server.msg_send.start()
    def send(self):
            # This function if for sending data to public world
            while True:
                send_msg = input()
                if send_msg != "close":
                    self.platform.sendto(send_msg.encode(),(chat_server.current_user_ip,chat_server.current_user_port))
                    chat_server.msg[chat_server.current_user_ip]["chat"].append(send_msg)
                else:
                    chat_server.stop_sending = True
                    print("** >> CLOSE SESSION FOR "+chat_server.current_user_ip)
                    break
# '192.168.43.145' is address and 1234 is port number for this system  
# At these Address and Port we will send and receive data
users={}
base_os_address = "192.168.43.145"
base_os_port = 1234
session= chat_server(base_os_address,base_os_port)
# send_data variable will decide that it will run "start_session" method of class 'chat_server'
send_data = True
while True:
    if chat_server.stop_sending ==True:
        chat_server.stop_sending = False
        print("\nUSER - \n")
        i = 1
        for user in chat_server.msg.keys():
            if len(chat_server.msg[user]["pending"]) == 0:
                print("{0}). {1}".format(i,user))    
            else:
                print("{0}). {1} **".format(i,user))
            users[str(i)]=user
            i+=1
        print("")
        send_data = True
        action = input("Enter IP or Available Above IP or Index 'Otherwise type exit ' : ")
    if send_data == True:
        send_data = False
        if action in users.keys():
            print("Please Start Chat \n")
            session.start_session(users[action])
        elif action == "exit" :
            print("EXIT")
            # To Finish Receive Method Thread ( A small Trick )
            session.start_session(base_os_address,base_os_port)
            exit()
        else:
            print("Please Start Chat \n")
            session.start_session(action)
