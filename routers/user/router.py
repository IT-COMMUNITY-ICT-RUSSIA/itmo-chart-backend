from fastapi import APIRouter, Depends

user_router = APIRouter(
    prefix="user",
    tags=["user"],
)


@user_router.post("/login")
def login():
    """
    log the user in provided the username
    and password and return a JWT token
    """
    pass


@user_router.get("/me")
def get_user_data():
    """return data for the requested user"""
    pass


@user_router.get("/users")
def get_all_users():
    """get all known users"""
    pass


@user_router.get("/achievements")
def get_user_achievements():
    """return achievement data for the requested user"""
    pass
