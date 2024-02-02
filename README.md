# PYStratum
stratum client with python

### Example

Install
```shell
pip install git+https://github.com/mantvmass/pystratum.git
```

Using
```python
from pystratum import Stratum


def handleReceive(stratum: Stratum, response: Dict[str, any]) -> None:
    print(response)
    id = response.get("id", 0)
    if id == None:
        pass
    elif id == 1:
        stratum.authorize()
    
        
def main():
    stratum_client = Stratum("ap.luckpool.net", 3956, "RQpWNdNZ4LQ5yHUM3VAVuhUmMMiMuGLUhT.pystratum", "x")
    stratum_client.connect()
    stratum_client.subscribe()
    stratum_client.onReceive(stratum_client, handleReceive)
   
        

if __name__ == "__main__":
    main()
```