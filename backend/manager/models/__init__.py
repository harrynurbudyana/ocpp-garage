from __future__ import annotations

from ocpp.v16.enums import ChargePointStatus
from sqlalchemy import Column, String, ForeignKey, Enum, JSON, Integer, Sequence
from sqlalchemy.orm import relationship

from core.database import Model


class Person(Model):
    __abstract__ = True

    email = Column(String(48), nullable=False, unique=True)
    first_name = Column(String(24), nullable=True, unique=False)
    last_name = Column(String(24), nullable=True, unique=False)
    address = Column(String(48), nullable=True, unique=False)


class Operator(Person):
    __tablename__ = "operators"

    password = Column(String(124), nullable=False, unique=False)


class Driver(Person):
    __tablename__ = "drivers"

    billing_requisites = Column(JSON, default=dict())
    charge_points = relationship("ChargePoint",
                                 back_populates="driver",
                                 lazy="joined")

    def __repr__(self) -> str:
        return f"Driver: {self.id}, {self.login}"


class ChargePoint(Model):
    __tablename__ = "charge_points"

    description = Column(String(124), nullable=True)
    status = Column(Enum(ChargePointStatus), default=ChargePointStatus.unavailable, index=True)
    manufacturer = Column(String, nullable=False)
    serial_number = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=True)
    model = Column(String, nullable=False)
    connectors = Column(JSON, default=dict())

    driver_id = Column(String, ForeignKey("drivers.id"), nullable=True)
    driver = relationship("Driver", back_populates="charge_points", lazy="joined")

    def __repr__(self):
        return f"ChargePoint (id={self.id}, status={self.status}, location={self.location})"


class Transaction(Model):
    __tablename__ = "transactions"
    transaction_id_seq = Sequence("transaction_id_seq")

    driver = Column(String, nullable=False)
    meter_start = Column(Integer, nullable=False)
    meter_stop = Column(Integer, nullable=True)
    charge_point = Column(String, nullable=False)
    transaction_id = Column(Integer, transaction_id_seq, server_default=transaction_id_seq.next_value())
