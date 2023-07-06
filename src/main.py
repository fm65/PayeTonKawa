#from revendeurs import server
from webshop import server

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server.app)