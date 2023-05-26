from sqlalchemy import Column, String, DateTime, ForeignKey, DECIMAL, Integer, text, Sequence, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('unique_id', start=10000000, increment=1), primary_key=True, server_default=text("nextval('unique_id')"))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now)
    role = Column(String, nullable=False, default='User')

    reward = relationship("Reward", back_populates="user")
    tree_order = relationship("TreeOrder", back_populates="user")


class Reward(Base):
    __tablename__ = 'rewards'

    id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    points = Column(Integer, nullable=False)

    user = relationship("User", back_populates="reward")


class TreeType(Base):
    __tablename__ = 'tree_types'

    id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    planting_cost = Column(DECIMAL, nullable=False)
    price = Column(DECIMAL, nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now)

    tree_order = relationship("TreeOrder", back_populates="tree_type")


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
    name = Column(String, nullable=False)
    longitude = Column(DECIMAL, nullable=False)
    latitude = Column(DECIMAL, nullable=False)

    tree_order = relationship("TreeOrder", back_populates="location")


class TreeProgress(Base):
    __tablename__ = 'tree_progress'

    id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
    is_planted = Column(Boolean, nullable=False, default=False)
    date_planted = Column(DateTime, nullable=True)
    health_status = Column(Integer, nullable=True)

    tree_order = relationship("TreeOrder", back_populates="progress")


class Donation(Base):
    __tablename__ = 'donations'

    id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
    amount = Column(DECIMAL, nullable=False)
    donation_type = Column(Integer, nullable=False, default=0)

    tree_order = relationship("TreeOrder", back_populates="donation")


class TreeOrder(Base):
    __tablename__ = 'tree_orders'

    id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
    type_id = Column(Integer, ForeignKey("tree_types.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"))
    progress_id = Column(Integer, ForeignKey("tree_progress.id", ondelete="CASCADE"))
    donation_id = Column(Integer, ForeignKey("donations.id", ondelete="CASCADE"))
    status = Column(String, default='Pending')
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now)

    tree_type = relationship("TreeType", back_populates="tree_order")
    user = relationship("User", back_populates="tree_order")
    location = relationship("Location", back_populates="tree_order")
    progress = relationship("TreeProgress", back_populates="tree_order")
    donation = relationship("Donation", back_populates="tree_order")


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
    author = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    subject = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)


class Advertiser(Base):
    __tablename__ = 'advertisers'

    id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
    name = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    website = Column(String, nullable=True)

    advertisement = relationship("Advertisement", back_populates="advertiser")


class Advertisement(Base):
    __tablename__ = 'advertisements'

    id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
    advertiser_id = Column(Integer, ForeignKey("advertisers.id", ondelete="CASCADE"))
    description = Column(String, nullable=True)
    image = Column(String, nullable=False)

    advertiser = relationship("Advertiser", back_populates="advertisement")
