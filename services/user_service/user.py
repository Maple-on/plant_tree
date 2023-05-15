from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from services.user_service.user_model import CreateUserModel, UpdateUserModel, RewardModel
from database.models import User, Reward
from datetime import datetime
from database.hashing import Hash
from services.auth_service.auth import log_in_while_creation


def create(request: CreateUserModel, db: Session):
    check_if_user_exists(request.email, db)
    new_user = User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
        phone=request.phone,
        role=request.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = log_in_while_creation(request.email, request.password, db)
    return {'user': new_user, 'token': token}


def get_list(db: Session):
    user = db.query(User).all()

    return user


def get_by_id(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()
    rewards = db.query(Reward).filter(Reward.user_id == id).all()
    reward_list = []
    all_sum = 0
    for reward in rewards:
        model = RewardModel(
            id=reward.id,
            name=reward.name,
            description=reward.description,
            points=reward.points
        )
        all_sum += reward.points
        reward_list.append(model)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")


    return {'user': user, 'rewards': reward_list, 'reward_sum': all_sum}


def update(id: int, request: UpdateUserModel, db: Session):
    user = db.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    setattr(user, "updated_at", datetime.now())
    db.commit()
    db.refresh(user)

    return user


def delete(id: int, db: Session):
    user = db.query(User).filter(User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    user.delete(synchronize_session=False)
    db.commit()

    return status.HTTP_204_NO_CONTENT


def check_if_user_exists(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with email {email} already exists")
