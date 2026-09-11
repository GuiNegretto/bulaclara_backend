"""Testes do endpoint POST /medicamentos/consulta (Fase 1)."""

from fastapi.testclient import TestClient

from app.main import app


def test_consulta_por_nome_retorna_bula_estruturada():
    with TestClient(app) as client:
        response = client.post("/medicamentos/consulta", json={"nome": "Dipirona"})
        assert response.status_code == 200
        body = response.json()
        assert body["nome"] == "Dipirona"
        assert "contraindicacoes" in body["bula_simplificada"]
        assert "efeitos_colaterais" in body["bula_simplificada"]
        assert "posologia" in body["bula_simplificada"]


def test_consulta_por_gtin_retorna_gtin():
    with TestClient(app) as client:
        response = client.post(
            "/medicamentos/consulta",
            json={"gtin": "7891234567890"},
        )
        assert response.status_code == 200
        assert response.json()["gtin"] == "7891234567890"


def test_consulta_sem_campos_rejeitada():
    with TestClient(app) as client:
        response = client.post("/medicamentos/consulta", json={})
        assert response.status_code == 422


def test_gtin_invalido_rejeitado():
    with TestClient(app) as client:
        response = client.post("/medicamentos/consulta", json={"gtin": "abc"})
        assert response.status_code == 422