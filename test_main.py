import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_get_all_traffic():
    """
    Тест на получение суммарного трафика по всем клиентам.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/traffic")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "customer_id" in data[0]
    assert "total_traffic" in data[0]


@pytest.mark.asyncio
async def test_filter_by_customer_id():
    """
    Тест на фильтрацию по ID клиента.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/traffic?customer_id=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1  # Должен вернуться один клиент
    assert data[0]["customer_id"] == 1


@pytest.mark.asyncio
async def test_filter_by_date_range():
    """
    Тест на фильтрацию по диапазону дат.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/traffic?start_date=2023-03-01%2016:30:00&end_date=2024-03-01%2012:00:00")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert "customer_id" in item
        assert "total_traffic" in item


@pytest.mark.asyncio
async def test_filter_by_ip():
    """
    Тест на фильтрацию по IP-адресу.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/traffic?ip=192.168.218.159")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert "customer_id" in item
        assert "total_traffic" in item


@pytest.mark.asyncio
async def test_combined_filters():
    """
    Тест на комбинацию фильтров: ID клиента и диапазон дат.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/traffic?customer_id=1&start_date=2023-01-01%2000:00:00&end_date=2023-12-31%2023:59:59"
        )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1  # Один клиент
    assert data[0]["customer_id"] == 1
    assert data[0]["total_traffic"] > 0
