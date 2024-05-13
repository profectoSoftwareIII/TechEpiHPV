from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UsuarioModel(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    cedula = Column(String)
    edad = Column(String)
    email = Column(String)
    password = Column(String)
    telefono = Column(String)

    # foraneo para otras tablas
    paciente = relationship("pacienteModel", back_populates="usuario")
    medico = relationship("medicoModel", back_populates="usuario")
    poblacionGeneral = relationship("poblacionGeneralModel", back_populates="usuario")

    # Recibo de foraneo de otras tablas


class PacienteModel(Base):
    __tablename__ = "paciente"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))

    # foraneo para otras tablas

    # Recibo de foraneo de otras tablas
    usuario = relationship("UsuarioModel", back_populates="paciente")


class MedicoModel(Base):
    __tablename__ = "medico"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    tarjeta_profesional = Column(String)
    especialidad = Column(String)

    # foraneo para otras tablas
    recordatorio = relationship("RecordatorioModel", back_populates="medico")

    # Recibo de foraneo de otras tablas
    usuario = relationship("UsuarioModel", back_populates="medico")


class PoblacionGeneralModel(Base):
    __tablename__ = "poblacionGeneral"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))

    # foraneo para otras tablas

    # Recibo de foraneo de otras tablas
    usuario = relationship("UsuarioModel", back_populates="poblacionGeneral")


class RecordatorioModel(Base):
    __tablename__ = "recordatorio"
    id = Column(Integer, primary_key=True)
    medico_id = Column(Integer, ForeignKey("medico.id"))
    tipo_recordatorio = Column(String)
    descripcion = Column(String)
    fecha = Column(DateTime)

    # foraneo para otras tablas

    # Recibo de foraneo de otras tablas
    medico = relationship("medicoModel", back_populates="recordatorio")


class HistorialDiagnosticoModel(Base):
    __tablename__ = "historialDiagnostico"
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("paciente.id"))
    medico_id = Column(Integer, ForeignKey("medico.id"))

    # foraneo para otras tablas

    # Recibo de foraneo de otras tablas
    medico = relationship("MedicoModel", back_populates="historialDiagnostico")
    paciente = relationship("PacienteModel", back_populates="historialDiagnostico")