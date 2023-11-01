from fastapi.testclient import TestClient
from server.ml_api.main import app
from unittest.mock import patch

client = TestClient(app)


def test_read_dataframe_info():
    test_dataframe_id = "some_dataframe_id"
    test_user = {"username": "testuser", "email": "testuser@example.com"}

    with patch("путь_к_модулю_зависимостей.current_active_user",
               return_value=test_user):
        response = client.get(
            f"/dataframe/metadata?dataframe_id={test_dataframe_id}")

    assert response.status_code == 200
    # Проверяем структуру ответа на соответствие ожидаемой
    assert "some_key" in response.json()
    # Другие проверки...
