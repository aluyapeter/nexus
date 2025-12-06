from fastapi import APIRouter, Depends
from .. import schemas, models
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Returns the currently logged-in user.
    The dependency 'get_current_user' automatically validates the Cookie.
    """
    return current_user