import socket
import json
from typing import Callable, Dict
import time


class Stratum:
    
    __host: str
    __port: int
    __username: str # address.nickname
    __password: str
    __sock: socket.socket
    __buffer: int
    is_connected: bool
    
    
    def __init__(self, host: str, port: int, username: str = None, password: str = None):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__sock = None
        # self.__buffer = 1024 # 4096
        self.__buffer = 4096
        self.is_connected = False
    
    
    def send(self, request: dict) -> bool:
        self.__sock.sendall((json.dumps(request) + "\n").encode("utf-8"))


    def onReceive(self, stratum: 'Stratum', callback: Callable[['Stratum', Dict[str, any]], None]) -> None:
        while True:
            data = self.__sock.recv(self.__buffer).decode("utf-8")
            json_strings = [chunk for chunk in data.split('\n') if chunk]
            for d in json_strings:
                response = json.loads(d)
                callback(stratum, response)

        

    def connect(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((self.__host, self.__port))
        self.is_connected = True
        
    
    def subscribe(self):
        self.send({"id": 1, "method": "mining.subscribe", "params": []})
        
        
    def authorize(self):
        self.send({"id": 2, "method": "mining.authorize", "params": [self.__username, self.__password]})
        
        
    def submit(self, jobID):
        self.send({
            "id": 1, "method": "mining.submit",
            "params": [
                self.__username,
                jobID,
                "fe36a31b",
                "504e86ed",
                "e9695791"
            ]
        })
        

def handleReceive(stratum: Stratum, response: Dict[str, any]) -> None:
    
    print(response)
    id = response.get("id", 0)
    
    if id == 1:
        stratum.authorize()
    
        

def main():
    # stratum_client = Stratum("ap.luckpool.net", 3956, "RQpWNdNZ4LQ5yHUM3VAVuhUmMMiMuGLUhT.pystratum", "x")
    stratum_client = Stratum("us.ss.btc.com", 1800, "RQpWNdNZ4LQ5yHUM3VAVuhUmMMiMuGLUhT.pystratum", "x")
    stratum_client.connect()
    stratum_client.subscribe()
    stratum_client.onReceive(stratum_client, handleReceive)
   
        

if __name__ == "__main__":
    main()