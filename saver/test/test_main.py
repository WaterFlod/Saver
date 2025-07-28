import sys

sys.path.append(sys.path[0][0:-11])

from fastapi.testclient import TestClient

from saver.src.main import app

client = TestClient(app)


def test_get_expense():
    response = client.get("/expenses/0")
    assert response.status_code == 200
    assert response.json() == {
        "id": 0,
        "amount": 110,
        "description": "Cola",
    }
    

def test_create_expense():
    response = client.post(
        "/expenses",
        json={"id": 1, "amount": 150, "description": "Cake"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1, 
        "amount": 150, 
        "description": "Cake",      
    }