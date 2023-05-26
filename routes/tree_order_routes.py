from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from services.tree_order_service.order_model import CreateOrderModel
from services.tree_order_service.order import create, get_by_id, get_list
from database import database
from database.oauth2 import get_current_user
from services.user_service.user_model import UserModel

router = APIRouter(
    prefix="/orders",
    tags=['Tree orders']
)

get_db = database.get_db


@router.get('/', status_code=status.HTTP_200_OK)
def Get_list(user_id: int, offset: int = 0, limit: int = 10, session: Session = Depends(get_db)):
    return get_list(offset, limit, user_id, session)


@router.get('/{id}', status_code=status.HTTP_200_OK)
def Get_by_id(id: int, session: Session = Depends(get_db)):
    return get_by_id(id, session)


@router.post('/', status_code=status.HTTP_201_CREATED)
def Create(request: CreateOrderModel = Depends(), session: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return create(request, session)


# @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
# def Update(id: int, request: UpdateOrderModel, session: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
#     return update(id, request, session)
#
#
# @router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def Delete(id: int, session: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
#     return delete(id, session)
