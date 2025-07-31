from ..import schemas , models , utils
from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import session
from ..database import get_db # the double dots are to mean 2 directories up , like [ fast api then app ] so thats 2 directories 


router = APIRouter(prefix="/users" , tags=['Users']) # from my path operation since everyone started with /users i moved them here inside as prefix .. its like it starts from here and removed it from the actual path operations this is how paths are managed in production because  path operations get complex 

@router.post("/", status_code=status.HTTP_201_CREATED , response_model=schemas.User_Response)

def create_user (user : schemas.Create_user ,db :session = Depends(get_db)):
    
    
    
    #before it is stored lets hash the password 
    #on the first line i am hashing the password ... 
    #on the second line i am assigning the hashed password o the user.pass to be added to the db 
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user= models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user   
@router.get("/{id}", response_model=schemas.User_Response)
    
def get_user (id = int ,db :session = Depends(get_db) ):
    user = db.query(models.Users).filter(models.Users.user_id == id).first()
    
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= " the user under {id} does not exist")
    
    return user