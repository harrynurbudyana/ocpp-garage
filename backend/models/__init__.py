from __future__ import annotations

from ocpp.v16.enums import ChargePointStatus, ChargePointErrorCode
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Enum,
    Integer,
    Sequence,
    Numeric,
    UniqueConstraint,
    Boolean, PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship

from core.database import Model, Base
from core.fields import TransactionStatus, Role


class User(Model):
    __tablename__ = "users"

    password = Column(String(124), nullable=True, unique=False)
    email = Column(String(48), nullable=False, unique=True)
    first_name = Column(String(24), nullable=False, unique=False)
    last_name = Column(String(24), nullable=True, unique=False)
    address = Column(String(48), nullable=True, unique=False)
    role = Column(Enum(Role), nullable=True)
    is_superuser = Column(Boolean, default=False)

    garage_id = Column(String, ForeignKey("garages.id"), nullable=True)
    garage = relationship("Garage", back_populates="users", lazy="joined")

    @property
    def id_tag(self):
        return self.id

    @property
    def is_admin(self) -> bool:
        return Role(self.role) is Role.admin if not self.is_superuser else False

    @property
    def is_operator(self) -> bool:
        return Role(self.role) is Role.operator if not self.is_superuser else False

    def __repr__(self) -> str:
        return f"User: {self.id}, {self.email}, {self.role}"


class GridProvider(Model):
    __tablename__ = "grid_providers"

    postnummer = Column(String, nullable=False, unique=True, index=True)
    region = Column(String, nullable=False)
    name = Column(String, nullable=False, index=True)
    daily_rate = Column(Numeric(precision=2, scale=2))
    nightly_rate = Column(Numeric(precision=2, scale=2))

    garages = relationship("Garage",
                           back_populates="grid_provider",
                           lazy="joined")


class Garage(Model):
    __tablename__ = "garages"

    name = Column(String, nullable=False, unique=True)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    daily_rate = Column(Numeric(precision=2, scale=2))
    nightly_rate = Column(Numeric(precision=2, scale=2))

    grid_provider_id = Column(String, ForeignKey("grid_providers.id"), nullable=False)
    grid_provider = relationship("GridProvider", back_populates="garages", lazy="joined")

    charge_points = relationship("ChargePoint",
                                 back_populates="garage",
                                 lazy="joined")
    users = relationship("User",
                         back_populates="garage",
                         lazy="joined")


class ChargePoint(Model):
    __tablename__ = "charge_points"

    description = Column(String(124), nullable=True)
    status = Column(Enum(ChargePointStatus), default=ChargePointStatus.unavailable, index=True)
    vendor = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    location = Column(String, nullable=True)
    model = Column(String, nullable=True)
    connectors = relationship("Connector",
                              back_populates="charge_point",
                              passive_deletes=True,
                              lazy="joined")

    garage_id = Column(String, ForeignKey("garages.id"), nullable=False)
    garage = relationship("Garage", back_populates="charge_points", lazy="joined")

    def __repr__(self):
        return f"ChargePoint (id={self.id}, status={self.status}, location={self.location})"


class Connector(Base):
    __tablename__ = "connectors"

    __table_args__ = (
        UniqueConstraint("id", "charge_point_id"),
        PrimaryKeyConstraint("id", "charge_point_id")
    )

    id = Column(Integer, nullable=False)
    status = Column(Enum(ChargePointStatus), default=ChargePointStatus.unavailable)
    error_code = Column(Enum(ChargePointErrorCode), default=ChargePointErrorCode.no_error)

    charge_point_id = Column(String, ForeignKey("charge_points.id", ondelete='CASCADE'), nullable=False)
    charge_point = relationship("ChargePoint", back_populates="connectors", lazy="joined")


class Transaction(Model):
    __tablename__ = "transactions"

    id = Column(Integer, Sequence('transaction_id_seq'), primary_key=True)
    garage = Column(String, nullable=False)
    meter_start = Column(Integer, nullable=False)
    meter_stop = Column(Integer, nullable=True)
    charge_point = Column(String, nullable=False)
    connector = Column(Integer, nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.in_progress)

    def __repr__(self):
        return f"Transaction (id={self.id}, " \
               f"garage_id={self.garage}, " \
               f"charge_point={self.charge_point}, " \
               f"transaction_id={self.id}, " \
               f"status={self.status}, " \
               f"meter_start={self.meter_start}, " \
               f"meter_stop={self.meter_stop})"
