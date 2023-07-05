from fastapi import APIRouter

# define router
router = APIRouter(
    prefix="/order",
    tags=["order"]
)


# add routes
@router.get("/")
def start(): 
    return {"msg" : "start order Router!"}
