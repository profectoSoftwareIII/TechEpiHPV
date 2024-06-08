from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UsuarioModel(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    cedula = Column(String)
    edad = Column(Integer)
    telefono = Column(String)
    email = Column(String)
    # foraneo para otras tablas
    medico = relationship("MedicoModel", back_populates="usuario")
    tipo = Column(String(20), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "usuario",  # tipo usuario
        "polymorphic_on": tipo,  # tipo de subclase
    }


class PacienteModel(UsuarioModel):
    __tablename__ = "paciente"
    id = Column(Integer, ForeignKey("usuario.id"), primary_key=True)
    tipo_hpv = Column(String)
    doctor_id = Column(Integer, ForeignKey("medico.id"))
    consulta = relationship("ConsultaModel", back_populates="paciente")
    recordatorio = relationship("RecordatorioModel", back_populates="paciente")
    medico = relationship("MedicoModel", back_populates="paciente")
    __mapper_args__ = {"polymorphic_identity": "paciente"}


class MedicoModel(Base):
    __tablename__ = "medico"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    tarjeta_profesional = Column(String)
    especialidad = Column(String)
    # foraneo para otras tablas
    recordatorio = relationship("RecordatorioModel", back_populates="medico")
    consulta = relationship("ConsultaModel", back_populates="medico")
    # Recibo de foraneo de otras tablas
    paciente = relationship(
        "PacienteModel",
        back_populates="medico",
        foreign_keys="[PacienteModel.doctor_id]",
    )
    usuario = relationship("UsuarioModel", back_populates="medico")


class RecordatorioModel(Base):
    __tablename__ = "recordatorio"
    id = Column(Integer, primary_key=True)
    medico_id = Column(Integer, ForeignKey("medico.id"))
    paciente_id = Column(Integer, ForeignKey("paciente.id"))
    tipo_recordatorio = Column(String)
    descripcion = Column(String)
    fecha = Column(DateTime)
    # foraneo para otras tablas
    # Recibo de foraneo de otras tablas
    medico = relationship("MedicoModel", back_populates="recordatorio")
    paciente = relationship("PacienteModel", back_populates="recordatorio")


class ConsultaModel(Base):
    __tablename__ = "consulta"
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("paciente.id"))
    medico_id = Column(Integer, ForeignKey("medico.id"))
    tratamiento_id = Column(Integer, ForeignKey("tratamiento.id"))
    nombre_diagnostico = Column(String)
    descripcion = Column(String)
    fecha = Column(DateTime)
    # Relaciones
    medico = relationship("MedicoModel", back_populates="consulta")
    paciente = relationship("PacienteModel", back_populates="consulta")
    tratamiento = relationship("TratamientoModel", back_populates="consulta")


class TratamientoModel(Base):
    __tablename__ = "tratamiento"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    # Relaciones
    consulta = relationship("ConsultaModel", back_populates="tratamiento")
