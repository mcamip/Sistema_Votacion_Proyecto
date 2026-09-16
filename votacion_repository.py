"""
Repositorios adicionales necesarios para la página web (votar y ver resultados).

Este archivo es INDEPENDIENTE de repositories.py: no modifica ni reemplaza
nada de ese archivo. Solo usa los modelos que ya existían en models.py
(VotoAuditoriaModel y ConteoResultadosModel), que no tenían todavía
un repositorio asociado.
"""

import hashlib
import secrets
from datetime import datetime, timezone

from sqlalchemy.orm import Session, joinedload

from models import (
    CandidatoModel,
    EstudianteModel,
    VotoAuditoriaModel,
    ConteoResultadosModel,
)


class CandidatoConsultaRepository:
    """Consultas de lectura adicionales sobre Candidato (no altera CandidatoRepository)."""

    def __init__(self, db: Session):
        self.db = db

    def obtener_todos_con_estudiante(self):
        """Devuelve tuplas (candidato, estudiante) para mostrar a quién representa cada tarjetón."""
        return (
            self.db.query(CandidatoModel, EstudianteModel)
            .join(EstudianteModel, CandidatoModel.id_estudiante == EstudianteModel.id_estudiante)
            .all()
        )


class VotoAuditoriaRepository:
    """Registra los votos y evita que un mismo estudiante vote dos veces."""

    def __init__(self, db: Session):
        self.db = db

    def ya_voto(self, id_estudiante: int) -> bool:
        return self.db.query(VotoAuditoriaModel).filter(
            VotoAuditoriaModel.id_estudiante == id_estudiante
        ).first() is not None

    def registrar_voto(self, id_estudiante: int, id_candidato: int):
        if self.ya_voto(id_estudiante):
            raise ValueError("Este estudiante ya ha ejercido su voto.")

        hash_verificacion = hashlib.sha256(
            f"{id_estudiante}-{id_candidato}-{datetime.now(timezone.utc)}-{secrets.token_hex(8)}".encode()
        ).hexdigest()

        voto = VotoAuditoriaModel(
            id_estudiante=id_estudiante,
            hash_verificacion=hash_verificacion,
        )
        self.db.add(voto)

        ConteoResultadosRepository(self.db).incrementar(id_candidato)

        self.db.commit()
        self.db.refresh(voto)
        return voto


class ConteoResultadosRepository:
    """Lleva el conteo de votos por candidato."""

    def __init__(self, db: Session):
        self.db = db

    def incrementar(self, id_candidato: int):
        conteo = self.db.query(ConteoResultadosModel).filter(
            ConteoResultadosModel.id_candidato == id_candidato
        ).first()
        if conteo is None:
            conteo = ConteoResultadosModel(id_candidato=id_candidato, total_votos=1)
            self.db.add(conteo)
        else:
            conteo.total_votos += 1
        return conteo

    def obtener_resultados(self):
        return self.db.query(ConteoResultadosModel).options(
            joinedload(ConteoResultadosModel.candidato)
        ).all()