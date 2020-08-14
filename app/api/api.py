from fastapi import APIRouter

from app.api.routes import users, items

router = APIRouter()
router.include_router(users.router, tags=["users"], prefix="/users")
router.include_router(items.router, tags=["items"], prefix="/items")


tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users."
        "The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]
