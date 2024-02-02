import socket
import json
import asyncio
from typing import Union


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
        self.is_connected: False
    
    
    async def send(self, request: dict) -> bool:
        self.__sock.sendall((json.dumps(request) + "\n").encode("utf-8"))


    async def receive(self) -> Union[dict, bytes]:
        return json.loads(self.__sock.recv(1024).decode("utf-8"))
        

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
        
    
        

# Example usage:
async def main():
    stratum_client = Stratum("sg.ss.btc.com", 1800, "gf", "fg")
    await stratum_client.connect()
    await stratum_client.subscribe()
    print(await stratum_client.receive())
    await stratum_client.authorize()
    print(await stratum_client.receive())

if __name__ == "__main__":
    asyncio.run(main())
    