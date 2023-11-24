from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal
from services.tree_order_service.order_model import CreateOrderModel
from database.models import TreeType, TreeOrder, Donation, TreeProgress, Location, User, Reward
from sqlalchemy import desc, text


def create(request: CreateOrderModel, db: Session):
    tree_price = check_if_type_exists_and_return_tree_price(request.type_id, db)
    location_id = create_location(request.location_name, request.latitude, request.longitude, db)
    progress_id = create_progress(db)
    donation_id = create_donation(request.donation_amount, db)
    create_reward(request.user_id, "New Donation", "Thank you for your newly made donation", request.donation_amount * tree_price, db)

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


def exchange_reward(request: CreateOrderModel, db: Session):
    tree_price = check_if_type_exists_and_return_tree_price(request.type_id, db)
    exchange_reward_points = request.donation_amount * tree_price * 50
    check_rewards_points(exchange_reward_points, request.user_id, db)
    update_reward_amount(exchange_reward_points, request.user_id, db)
    location_id = create_location(request.location_name, request.latitude, request.longitude, db)
    progress_id = create_progress(db)
    donation_id = create_donation(request.donation_amount, db, 1)

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


def get_list(offset: int, limit: int, user_id: int, db: Session):
    orders = db.query(
            TreeOrder.id,
            User.id,
            User.name,
            User.phone,
            TreeType.name,
            TreeType.price,
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
        .order_by(desc(TreeOrder.created_at))

    if user_id:
        orders = orders.filter(TreeOrder.user_id == user_id)

    orders = orders.offset(offset).limit(limit).all()

    order_list = [
        {
        "id": order[0],
        "user_id": order[1],
        "user_name": order[2],
        "user_phone": order[3],
        "tree_type": order[4],
        "tree_price": order[5],
        "is_planted": order[6],
        "date_planted": order[7],
        "health_status": order[8],
        "donation_amount": order[9],
        "donation_type": order[10],
        "location_name": order[11],
        "latitude": order[12],
        "longitude": order[13],
        "created_at": order[14],
        "updated_at": order[15],
        }
        for order in orders
    ]

    db.close()
    return order_list


def check_if_type_exists_and_return_tree_price(type_id: int, db: Session):
    tree_type = db.get(TreeType, type_id)
    if not tree_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tree type with id {type_id} not found")
    return tree_type.price


def check_rewards_points(exchange_reward_points: Decimal, user_id: int, db: Session):
    sql = f"SELECT SUM(points) FROM rewards WHERE user_id = '{user_id}'"
    actual_reward_points = db.execute(text(sql)).first()
    if exchange_reward_points > actual_reward_points[0]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You don't have sufficient amount of reward points")


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


def create_donation(amount: Decimal, db: Session, donation_type: int = 0):
    new_donation = Donation(
        amount=amount,
        donation_type=donation_type
    )
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)

    return new_donation.id


def create_reward(user_id: int, name: str, description: str, points: Decimal, db: Session):
    points = points * 10
    new_reward = Reward(
        user_id=user_id,
        name=name,
        description=description,
        points=points
    )
    db.add(new_reward)
    db.commit()
    db.refresh(new_reward)

    return new_reward


def update_reward_amount(points: Decimal, user_id: int, db: Session):
    new_reward = Reward(
        user_id=user_id,
        name="Exchange",
        description="Thank you for exchanging rewards for new donations",
        points=-points
    )
    db.add(new_reward)
    db.commit()
    db.refresh(new_reward)
