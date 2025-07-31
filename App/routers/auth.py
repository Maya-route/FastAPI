from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter  
from sqlalchemy.orm import session
from .. import database , models , utils, schemas , oath2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=["Authentication"])

# creating this for user authentication .. remember in utils we have a path operation for creating users , but how do we verify users 
#its more modular again to put it in a different file ... not that there will be a problem if i use the utils but again for better management 
 
 
 #creating the login path remember everything we are creating something we use the post operation .. we are not getting something from the server we are sending 
 
 
@router.post("/login" , response_model=schemas.Token)

def login (user_credential: OAuth2PasswordRequestForm = Depends() , db :session = Depends(database.get_db)):
    # so for the below reason we create a dependency and save it under the variable user_credential 
    # so the another  best thing about fat api is the module OAuth2PasswordRequestForm that imported 
    # so instead of us defining the what payload data we put in for the token .. it pretty much prepares a form for the user 
    # one thing to always remember  is that it always uses the username : the password : these 2 as a form of dict it does not  care if the user name is an email a number a ame or what ever  
    #btw depends() is imported from fastapi .. its a built in method for it 
    #and btw for that reason i mean the structure of the form instead of the user credential . email (which in my case i have email and password , i will instead use username .. because thats how the module  works )
    #so now when using post man for testing you can no longer use a raw jason  it wont work so instead of raw data use the form data part 
    user = db.query(models.Users).filter(models.Users.email == user_credential.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail= " Incorrect credentials")
    
    if not utils.verify(user_credential.password , user.password):
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN , detail= " Incorrect credentials")
    
    #if correct then this is where we create token 
    access_token = oath2.create_jwt_token(data = {"user_id" : user.user_id}) #here its like we decided to create the token out of user_id for the payload part .. remeber everything else comes from the header and secrete .. refer to the slide on one note .. the JWT library handles the secrete and the header part 
    # this is like controlling  the payload part 
    
    return {"access_token": access_token,  "token_type": "bearer" } 
    #then return the token 
    # so basically up until this point user tries to login if sucessful we created a token ... 
    #for the token its best to create a schema because remember the token is coming from the clint end and never stored in DB and really chemas should be for both path 
    #but especially when the client is sending it ... so creating a schema for the access token .. cause see here we expect access token and the bearer the bearer is just something that will be used for the front end 
    
    
    # from everything we have done so far we are done with authentication but if you really go to any of the operations in our pots 
    #i can simply just do it without being asked to be authenticated so thats the next part technically we call it protecting the end points 
    #this is where we make use of that dependency tha we have been working on under oath2 ..lets goo 
    
    