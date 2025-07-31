from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from ..import database , schemas , oath2 , models
from sqlalchemy.orm import session

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/",status_code=status.HTTP_201_CREATED)

def vote(vote: schemas.Vote ,db:session = Depends(database.get_db) , current_user : int = Depends(oath2.get_current_user)):
    #creating the logic 
    vote_query= db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id==current_user.user_id)
    found_vote = vote_query.first()
    post= db.query(models.Vlans).filter(models.Vlans.vlan_id== vote.post_id).first()
     #chekking that the vote doesnt exist 
    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {vote.post_id} Doest exist")
    if (vote.dir == 1 ):
       
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail = f"user {current_user.user_id} has already voted for {vote.post_id}")
        new_vote= models.Vote(post_id = vote.post_id , user_id = current_user.user_id )
        db.add(new_vote)
        db.commit()
        return{"message": "successfully  added vote"}
    else:
        
        if not found_vote: # if there is post 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = "Vote does not exist")
        vote_query.delete(synchronize_session = False)
        db.commit()
        return {"message": "successfully  deleted vote"}
        