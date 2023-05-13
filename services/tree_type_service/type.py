from sqlalchemy import desc
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from services.tree_type_service.type_model import CreateTypeModel, UpdateTypeModel, TypeModel
from database.models import TreeType
from services.tree_type_service.bucket import delete_image_from_s3, send_image_to_s3, update_image_from_s3
from datetime import datetime


def create(request: CreateTypeModel, file: UploadFile, db: Session):
    uploaded_file_url = send_image_to_s3(file)

    new_type = TreeType(
        name=request.name,
        description=request.description,
        planting_cost=request.planting_cost,
        price=request.price,
        image_url=uploaded_file_url
    )
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    db.close()

    return new_type


def get_list(offset: int, limit: int, db: Session):
    types = db.query(TreeType).order_by(desc(TreeType.created_at)).offset(offset).limit(limit).all()
    type_list = []

    for tree_type in types:
        each_category = TypeModel(
            id=tree_type.id,
            name=tree_type.name,
            description=tree_type.description,
            planting_cost=tree_type.planting_cost,
            price=tree_type.price,
            image_url=tree_type.image_url,
            created_at=tree_type.created_at,
            updated_at=tree_type.updated_at
        )
        type_list.append(each_category)

    db.close()
    return type_list


def get_by_id(id: int, db: Session):
    tree_type = db.query(TreeType).filter(TreeType.id == id).first()
    if not tree_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tree type with id {id} not found")

    specific_type = TypeModel(
            id=tree_type.id,
            name=tree_type.name,
            description=tree_type.description,
            planting_cost=tree_type.planting_cost,
            price=tree_type.price,
            image_url=tree_type.image_url,
            created_at=tree_type.created_at,
            updated_at=tree_type.updated_at
    )

    return specific_type


def update(id: int, request: UpdateTypeModel, db: Session):
    tree_type = db.get(TreeType, id)
    if not tree_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tree type with id {id} not found")
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "image_url" and value is not None:
            value = update_image_from_s3(request.image_url, str(tree_type.image_url))
        if value is not None:
            setattr(tree_type, key, value)
    setattr(tree_type, "updated_at", datetime.now())
    db.commit()
    db.refresh(tree_type)
    db.close()

    return tree_type


def delete(id: int, db: Session):
    tree_type = db.query(TreeType).filter(TreeType.id == id)

    if not tree_type.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tree type with id {id} not found")

    file_url = str(tree_type.first().image_url)

    delete_image_from_s3(file_url)
    tree_type.delete(synchronize_session=False)
    db.commit()
    db.close()

    return status.HTTP_204_NO_CONTENT
