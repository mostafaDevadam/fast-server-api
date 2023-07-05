from fastapi import APIRouter

router = APIRouter(
    prefix="/customer",
    tags=["customer_"]
)




@router.get("/")
async def start():
    return {"msg":"start customer router!"}