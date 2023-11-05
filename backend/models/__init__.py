from __future__ import annotations

from ocpp.v16.enums import ChargePointStatus, ChargePointErrorCode
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Enum,
    JSON,
    ARRAY,
    Integer,
    Sequence,
    Numeric,
    UniqueConstraint,
    PrimaryKeyConstraint,
    Date
)
from sqlalchemy.orm import relationship

from core.database import Model, Base
from core.fields import TransactionStatus


class SpotPrice(Model):
    __tablename__ = "spot_prices"

    date = Column(Date, nullable=False, unique=True)
    hourly_prices = Column(ARRAY(Numeric(scale=2)))


class Person(Model):
    __abstract__ = True

    email = Column(String(48), nullable=False, unique=True)
    first_name = Column(String(24), nullable=False, unique=False)
    last_name = Column(String(24), nullable=False, unique=False)
    address = Column(String(48), nullable=False, unique=False)

    def __repr__(self) -> str:
        return f"Driver: {self.id}, {self.email}"


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
    operators = relationship("Operator",
                             back_populates="garage",
                             lazy="joined")
    drivers = relationship("Driver",
                           back_populates="garage",
                           lazy="joined")
    government_rebates = relationship("GovernmentRebate",
                                      back_populates="garage",
                                      lazy="joined")


class GovernmentRebate(Model):
    __tablename__ = "government_rebates"

    value = Column(Numeric, nullable=False)
    period = Column(Date, nullable=False)

    garage_id = Column(String, ForeignKey("garages.id"), nullable=True)
    garage = relationship("Garage", back_populates="government_rebates", lazy="joined")


class Operator(Person):
    __tablename__ = "operators"

    password = Column(String(124), nullable=False, unique=False)

    garage_id = Column(String, ForeignKey("garages.id"), nullable=True)
    garage = relationship("Garage", back_populates="operators", lazy="joined")

    @property
    def is_superuser(self):
        return not bool(self.garage_id)


class Driver(Person):
    __tablename__ = "drivers"

    billing_requisites = Column(JSON, default=dict())
    connectors = relationship("Connector",
                              back_populates="driver",
                              lazy="joined")

    garage_id = Column(String, ForeignKey("garages.id"), nullable=False)
    garage = relationship("Garage", back_populates="drivers", lazy="joined")


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

    driver_id = Column(String, ForeignKey("drivers.id"), nullable=True)
    driver = relationship("Driver", back_populates="connectors", lazy="joined")

    @property
    def is_taken(self):
        return bool(self.driver_id)


class Transaction(Model):
    __tablename__ = "transactions"
    transaction_id_seq = Sequence("transaction_id_seq")

    garage = Column(String, nullable=False)
    driver = Column(String, nullable=False)
    meter_start = Column(Integer, nullable=False)
    meter_stop = Column(Integer, nullable=True)
    charge_point = Column(String, nullable=False)
    connector = Column(Integer, nullable=False)
    transaction_id = Column(Integer, transaction_id_seq, server_default=transaction_id_seq.next_value())
    status = Column(Enum(TransactionStatus), default=TransactionStatus.in_progress)

    @property
    def total_consumed_kw(self):
        # Assuming we receive meters as watts.
        return (self.meter_stop - self.meter_start) / 1000

    @property
    def total_session_minutes(self):
        return (self.updated_at - self.created_at).total_seconds() / 60

    @property
    def consumption_per_minute(self):
        return self.total_consumed_kw / self.total_session_minutes

    def __repr__(self):
        return f"Transaction (id={self.id}, " \
               f"garage_id={self.garage}, " \
               f"charge_point={self.charge_point}, " \
               f"transaction_id={self.transaction_id}, " \
               f"status={self.status}, " \
               f"meter_start={self.meter_start}, " \
               f"meter_stop={self.meter_stop})"
