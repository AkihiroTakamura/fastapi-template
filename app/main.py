from fastapi import FastAPI, Depends, Header, HTTPException, status

from app.routers import items, users

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


app = FastAPI(
    title="FastAPI Application Template",
    description="None",
    version="0.1.0",
    openapi_tags=tags_metadata,
)


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Token header invalid",
        )


app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
)

app.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
)
