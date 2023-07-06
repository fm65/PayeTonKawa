from fastapi import FastAPI
from fastapi.testclient import TestClient
import unittest

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

client = TestClient(app)

class TestAPI(unittest.TestCase):

    def test_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World"})

if __name__ == '__main__':
    unittest.main()
