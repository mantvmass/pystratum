import socket
import json
import asyncio
from typing import Union
import time


class Stratum:
    
    __host: str
    __port: int
    __username: str # address.nickname
    __password: str
    __sock: socket.socket
    is_connected: bool
    
    
    def __init__(self, host: str, port: int, username: str = None, password: str = None):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__sock = None
        self.is_connected = False
    
    
    async def send(self, request: dict) -> bool:
        self.__sock.sendall((json.dumps(request) + "\n").encode("utf-8"))


    # async def receive(self) -> Union[dict, bytes]:
    async def receive(self) -> dict:
        print("==================================================================================")
        
        # json_objects = [json.loads(obj) for obj in self.__sock.recv(1024).decode("utf-8").split('\n') if obj.strip()]
        
        json_objects = json.loads(self.__sock.recv(1024).decode("utf-8"))
    
        # json_objects = self.__sock.recv(1024)
        
        print(json_objects)
        return json_objects

        

    async def connect(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((self.__host, self.__port))
        self.is_connected = True
        
    
    async def subscribe(self):
        await self.send({"id": 1, "method": "mining.subscribe", "params": []})
        
        
    async def authorize(self):
        await self.send({"id": 2, "method": "mining.authorize", "params": [self.__username, self.__password]})
        
        
    async def submit(self, jobID):
        await self.send({
            "id": 1, "method": "mining.submit",
            "params": [
                self.__username,
                jobID,
                "fe36a31b",
                "504e86ed",
                "e9695791"
            ]
        })
        
    
        

async def main():
    # stratum_client = Stratum("sg.ss.btc.com", 1800, "gf", "fg")
    # await stratum_client.connect()
    
    # await stratum_client.subscribe()
    
    # while True:
        
    #     result = await stratum_client.receive()
        
    #     print(result)

    #     if result["id"] == 1:
    #         await stratum_client.authorize()
        
    #     time.sleep(2)
    
    from pprint import pprint
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("ap.luckpool.net", 3956))
    client_socket.sendall((json.dumps({"id": 1, "method": "mining.subscribe", "params": []}) + "\n").encode("utf-8"))
    print(client_socket.recv(1028).decode("utf-8"))
    client_socket.sendall((json.dumps({"id": 2, "method": "mining.authorize", "params": ["dsfgd", "x"]}) + "\n").encode("utf-8"))
    print(client_socket.recv(1028).decode("utf-8"))
    while 1:
        
        # pprint(json.loads(client_socket.recv(1028).decode("utf-8")))
        # print(client_socket.recv(1028).decode("utf-8"))
        
        
        data = client_socket.recv(1028).decode("utf-8")
        
        
        # แยก JSON strings
        json_strings = [chunk for chunk in data.split('\n') if chunk]
        
        for i in json_strings:
            pprint(json.loads(i))
            print("===================================================================================")
    
   
        

if __name__ == "__main__":
    asyncio.run(main())
    pass