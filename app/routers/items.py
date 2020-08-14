from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "Item Bar"}]


@router.get("/{item_id}")
async def read_item(item_id: int):
    return {"name": "Fake Specific Item", "item_id": item_id}


@router.put(
    "/{item_id}", responses={403: {"description": "Operation forbidden"}}
)
async def update_item(item_id: int):
    if item_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update the item: 1",
        )
    return {"item_id": item_id, "name": "The Fighters"}
