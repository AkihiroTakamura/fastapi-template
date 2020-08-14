from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.depends import (
    get_db,
    get_current_active_user,
)
from app import models, schemas, service

router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
def read_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    if service.user.is_superuser(current_user):
        items = service.item.get_list(db, skip=skip, limit=limit)
    else:
        items = service.item.get_list_by_owner(
            db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return items


@router.get("/{item_id}", response_model=schemas.Item)
def read_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """
    Get Item by ID.
    """
    item = service.item.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    if not service.user.is_superuser(current_user) and (
        item.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return item


@router.post("/", response_model=schemas.Item)
def create_item(
    *,
    db: Session = Depends(get_db),
    item_in: schemas.ItemCreate,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = service.item.create_with_owner(
        db, obj_in=item_in, owner_id=current_user.id
    )
    return item


@router.put("/{item_id}", response_model=schemas.Item)
def update_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    item_in: schemas.ItemUpdate,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    item = service.item.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    if not service.user.is_superuser(current_user) and (
        item.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    item = service.item.update(db, db_obj=item, obj_in=item_in)
    return item


@router.delete("/{item_id}", response_model=schemas.Item)
def delete_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = service.item.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    if not service.user.is_superuser(current_user) and (
        item.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    item = service.item.remove(db, id=item_id)
    return item
