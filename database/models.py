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
    reward_id = Column(Integer, Sequence('unique_id'), primary_key=False, server_default=text("nextval('unique_id')"))
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now)

    reward = relationship("Reward", back_populates="user")
    tree_order = relationship("TreeOrder", back_populates="user")


class Reward(Base):
    __tablename__ = 'rewards'

    id = Column(Integer, nullable=False, primary_key=True)
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
    tree_id = Column(Integer, nullable=True)
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


#
# class Category(Base):
#     __tablename__ = 'categories'
#
#     id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
#     name = Column(String, nullable=False)
#     name_uz = Column(String, nullable=True)
#     name_en = Column(String, nullable=True)
#     name_tr = Column(String, nullable=True)
#     created_at = Column(DateTime(timezone=True), default=datetime.now)
#     updated_at = Column(DateTime(timezone=True), default=datetime.now)
#
#     product = relationship("Product", back_populates="category")
#
#
# class Product(Base):
#     __tablename__ = 'products'
#
#     id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
#     name = Column(String, nullable=False)
#     name_uz = Column(String, nullable=True)
#     name_en = Column(String, nullable=True)
#     name_tr = Column(String, nullable=True)
#     description = Column(String, nullable=False)
#     description_uz = Column(String, nullable=True)
#     description_en = Column(String, nullable=True)
#     description_tr = Column(String, nullable=True)
#     category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
#     price = Column(DECIMAL, nullable=False)
#     amount = Column(DECIMAL, nullable=False)
#     unit = Column(String, default='kg')
#     image_url = Column(String, nullable=False)
#     created_at = Column(DateTime(timezone=True), default=datetime.now)
#     updated_at = Column(DateTime(timezone=True), default=datetime.now)
#
#     category = relationship("Category", back_populates="product")
#     transaction = relationship("Transaction", back_populates="product")
#
#
# class OrderDetails(Base):
#     __tablename__ = 'order_details'
#
#     id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
#     client_id = Column(Integer, ForeignKey("clients.id"))
#     total = Column(DECIMAL, nullable=False)
#     order_status = Column(String, default='New')
#     payment_id = Column(Integer, ForeignKey("payment_details.id"), nullable=True)
#     created_at = Column(DateTime(timezone=True), default=datetime.now)
#     updated_at = Column(DateTime(timezone=True), default=datetime.now)
#
#     client = relationship("Client", back_populates="order_details")
#     order_items = relationship("OrderItems", back_populates="order_details")
#     payment_details = relationship("PaymentDetails", back_populates="order_details")
#
#
# class OrderItems(Base):
#     __tablename__ = 'order_items'
#
#     id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
#     order_id = Column(Integer, ForeignKey("order_details.id"))
#     product_id = Column(Integer, nullable=False)
#     product_name = Column(String, nullable=False)
#     product_price = Column(DECIMAL, nullable=False)
#     amount = Column(DECIMAL, nullable=False)
#
#     order_details = relationship("OrderDetails", back_populates="order_items")
#
#
# class PaymentDetails(Base):
#     __tablename__ = 'payment_details'
#
#     id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
#     order_id = Column(Integer, nullable=False)
#     amount = Column(DECIMAL, nullable=False)
#     payment_method = Column(String, nullable=False)
#     payment_status = Column(String, default='Not Paid')
#
#     order_details = relationship("OrderDetails", back_populates="payment_details")
#
#
# class Transaction(Base):
#     __tablename__ = 'transactions'
#
#     id = Column(Integer, Sequence('unique_id'), primary_key=True, server_default=text("nextval('unique_id')"))
#     product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
#     product = Column(DECIMAL, nullable=False)
#     price = Column(DECIMAL, nullable=False)
#     payment_method = Column(String, nullable=False)
#     status = Column(String, default='pending')
#     created_at = Column(DateTime(timezone=True), default=datetime.now)
#     updated_at = Column(DateTime(timezone=True), default=datetime.now)
#
#     product = relationship("Product", back_populates="transaction")
