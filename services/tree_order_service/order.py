from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import text
from decimal import Decimal
from services.tree_order_service.order_model import CreateOrderModel
from database.models import TreeType, TreeOrder, Donation, TreeProgress, Location, User
from sqlalchemy import desc

def create(request: CreateOrderModel, db: Session):
    check_if_type_exists(request.type_id, db)
    location_id = create_location(request.location_name, request.latitude, request.longitude, db)
    progress_id = create_progress(db)
    donation_id = create_donation(request.donation_amount, db)

    new_order = TreeOrder(
        type_id=request.type_id,
        user_id=request.user_id,
        location_id=location_id,
        progress_id=progress_id,
        donation_id=donation_id
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


def get_by_id(order_id: int, db: Session):
    order = db.query(
            TreeOrder.id,
            User.id,
            User.name,
            User.phone,
            TreeType.name,
            TreeProgress.is_planted,
            TreeProgress.date_planted,
            TreeProgress.health_status,
            Donation.amount,
            Donation.donation_type,
            Location.name,
            Location.latitude,
            Location.longitude,
            TreeOrder.created_at,
            TreeOrder.updated_at)\
        .join(TreeType, TreeOrder.type_id == TreeType.id)\
        .join(User, TreeOrder.user_id == User.id)\
        .join(TreeProgress, TreeOrder.progress_id == TreeProgress.id)\
        .join(Donation, TreeOrder.donation_id == Donation.id)\
        .join(Location, TreeOrder.location_id == Location.id)\
        .filter(TreeOrder.id == order_id)\
        .first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order with id {order_id} not found")

    order_list = {
        "id": order[0],
        "user_id": order[1],
        "user_name": order[2],
        "user_phone": order[3],
        "tree_type": order[4],
        "is_planted": order[5],
        "date_planted": order[6],
        "health_status": order[7],
        "donation_amount": order[8],
        "donation_type": order[9],
        "location_name": order[10],
        "latitude": order[11],
        "longitude": order[12],
        "created_at": order[13],
        "updated_at": order[14],
    }

    db.close()
    return order_list

def get_list(offset: int, limit: int, db: Session):
    orders = db.query(
            TreeOrder.id,
            User.id,
            User.name,
            User.phone,
            TreeType.name,
            TreeProgress.is_planted,
            TreeProgress.date_planted,
            TreeProgress.health_status,
            Donation.amount,
            Donation.donation_type,
            Location.name,
            Location.latitude,
            Location.longitude,
            TreeOrder.created_at,
            TreeOrder.updated_at)\
        .join(TreeType, TreeOrder.type_id == TreeType.id)\
        .join(User, TreeOrder.user_id == User.id)\
        .join(TreeProgress, TreeOrder.progress_id == TreeProgress.id)\
        .join(Donation, TreeOrder.donation_id == Donation.id)\
        .join(Location, TreeOrder.location_id == Location.id)\
        .order_by(desc(TreeOrder.created_at)).offset(offset).limit(limit).all()

    order_list = [
        {
        "id": order[0],
        "user_id": order[1],
        "user_name": order[2],
        "user_phone": order[3],
        "tree_type": order[4],
        "is_planted": order[5],
        "date_planted": order[6],
        "health_status": order[7],
        "donation_amount": order[8],
        "donation_type": order[9],
        "location_name": order[10],
        "latitude": order[11],
        "longitude": order[12],
        "created_at": order[13],
        "updated_at": order[14],
        }
        for order in orders
    ]

    db.close()
    return order_list


def check_if_type_exists(type_id: int, db: Session):
    tree_type = db.get(TreeType, type_id)
    if not tree_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tree type with id {id} not found")


def create_location(name: str, latitude: Decimal, longitude: Decimal, db: Session):
    new_location = Location(
        name=name,
        latitude=latitude,
        longitude=longitude
    )
    db.add(new_location)
    db.commit()
    db.refresh(new_location)

    return new_location.id


def create_progress(db: Session):
    new_progress = TreeProgress()
    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)

    return new_progress.id


def create_donation(amount: Decimal, db: Session):
    new_donation = Donation(
        amount=amount
    )
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)

    return new_donation.id
