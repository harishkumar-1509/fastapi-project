from fastapi import APIRouter

router = APIRouter()

@router.get('/get-user')
async def get_user():
    return {"user":"User returned"}