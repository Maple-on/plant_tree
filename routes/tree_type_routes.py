from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import UploadFile, File

from services.tree_type_service.type import CreateTypeModel, UpdateTypeModel
from services.tree_type_service.type import create, get_list, get_by_id, delete, update
from database import database
from database.oauth2 import get_current_user
from services.user_service.user_model import UserModel

router = APIRouter(
    prefix="/types",
    tags=['Tree types']
)

get_db = database.get_db


@router.get('/', status_code=status.HTTP_200_OK)
def Get_list(offset: int = 0, limit: int = 10,  session: Session = Depends(get_db)):
    return get_list(offset, limit, session)


@router.get('/{id}', status_code=status.HTTP_200_OK)
def Get_by_id(id: int, session: Session = Depends(get_db)):
    return get_by_id(id, session)


@router.post('/', status_code=status.HTTP_201_CREATED)
def Create(request: CreateTypeModel = Depends(), picture: UploadFile = File(...),
                   session: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return create(request, picture, session)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def Update(id: int, request: UpdateTypeModel, session: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return update(id, request, session)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def Delete(id: int, session: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return delete(id, session)
