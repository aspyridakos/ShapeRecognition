import socket
import json

class Sender:

    allowed = set(['S','P','O','A'])

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def send(self, message):
        if len(message) != 5 or not set(message.upper()) <= Sender.allowed:
            raise ValueError("Message is incorrect format")
        message = message.upper()
        print("Sending message:", message, "to", self.address, "port:", self.port)
        self.socket.sendto(json.dumps({"sequence":message}).encode("utf-8"),(self.address, self.port))

def main():
    s = Sender("127.0.0.1",5005)
    s.send("sssss")

if __name__ == "__main__":
    main()
