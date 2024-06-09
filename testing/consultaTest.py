import sys

sys.path.append("..")
import pytest
from httpx import AsyncClient
from main import app
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_crear_consulta_valida():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/registrarConsulta/",
            json={
                "medico_id": 1,
                "paciente_id": 1,
                "tratamiento_id": 1,
                "nombre_diagnostico": "VPH Positivo",
                "descripcion": "Paciente diagnosticado con VPH",
                "fecha": (datetime.now() + timedelta(days=1)).isoformat(),
            },
        )
    assert response.status_code == 200
    data = response.json()
    assert data["medico_id"] == 1
    assert data["paciente_id"] == 1
    assert data["tratamiento_id"] == 1
    assert data["nombre_diagnostico"] == "VPH Positivo"
    assert data["descripcion"] == "Paciente diagnosticado con VPH"


@pytest.mark.asyncio
async def test_crear_consulta_id_negativo():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/registrarConsulta/",
            json={
                "medico_id": -1,
                "paciente_id": 1,
                "tratamiento_id": 1,
                "nombre_diagnostico": "VPH Positivo",
                "descripcion": "Paciente diagnosticado con VPH",
                "fecha": (datetime.now() + timedelta(days=1)).isoformat(),
            },
        )
    assert response.status_code == 400
    data = response.json()
    assert (
        data["detail"] == "IDs de médico, paciente y tratamiento deben ser positivos."
    )


@pytest.mark.asyncio
async def test_crear_consulta_fecha_pasada():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/registrarConsulta/",
            json={
                "medico_id": 1,
                "paciente_id": 1,
                "tratamiento_id": 1,
                "nombre_diagnostico": "VPH Positivo",
                "descripcion": "Paciente diagnosticado con VPH",
                "fecha": (datetime.now() - timedelta(days=1)).isoformat(),
            },
        )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "La fecha debe ser futura o la fecha actual."
