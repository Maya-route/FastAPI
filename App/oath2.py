from jose import JWTError , jwt
from datetime import datetime, timedelta
from . import schemas , database , models
from fastapi import Depends ,status , HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session
from .config import settings

oath2_scheme = OAuth2PasswordBearer(tokenUrl="login") 

#jwt = jason web token btw 
#this is the page that deals with tokens 

# this module needs 3 things 
#1 SECRETE KEy 
#2 we define the algorithm 
#3 we need an expiration time for the token otherwise user is logged in forever 


#to test weather the token expiration works you can reduce the time from 30 to a 
# minute and test just like how we do it in ttl change for DNS 

SECRET_KEY = settings.SECRET_KEY#"09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = settings.ALGORITHM#"HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES#30

#when you see bearer is just is a type of tooken to tell the client end what type of token to send .. its one of the types 
#the algo HS256 you see is a hashing algo .. the one you know about cryptographic algo 

def create_jwt_token (data: dict):
    
    to_encode = data.copy() #copying the data and saving it to a variable 
    expire = datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)# like it expires from now to the access token time and we use the method time delta to get that time 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY , algorithm=ALGORITHM)# the built in jwt encode method actually produces the token for us with those 3 essentials i mentioned 
    return encoded_jwt

#function to verify the  token ... up to this point the token comes from the client   remember this JWT thing is a stateless because the token comes from the client end 

# now once we have the token on the below method we take that token in and decode it and verify if its valid 
def verify_access_token (token : str , credential_exception):
    
    try:
        
        payload = jwt.decode(token , SECRET_KEY , algorithms=ALGORITHM)
        #from this payload get the user id so after decoding get the user id because remember we used it to decode as our payload 
        id : str = payload.get("user_id") # you are trying to retrieve  the user id and save it under a variable 
        #another point here is that the x.y like for instance the payload.user_id for instance  is only for objects so basically like classes and methods imported ,  not dictionaries 
        #to get a value from a dictionary we use either ["key"] or the .get() method  
        
        if id is None: #no id is present 
            raise credential_exception # this is what ever is given within the method itself 
        token_data = schemas.Token_Data(user_id=id)
        
    except JWTError as e:
        print(e)
        raise credential_exception
   
    
    #the method below is to simply extract the id from all these incase we just want to refer to this method and get the id to use it for what ever 
    
    return token_data

#the whole idea of the below method is to grab that already authenticated user so we can perform some logic with it in our codes as we want 
def get_current_user (token:str =  Depends(oath2_scheme) , db: session = Depends(database.get_db)):# again creating a dependency here again this came from a builtin module  form past api look at the imports 

#remember we are trying to get the current user 
#this is also where i define the credentials exception 

    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail = "could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token , credential_exception)
    
    user = db.query(models.Users).filter(models.Users.user_id == token.user_id).first()
    
    return user

#so this connected to db and filters the authenticated user id 

#so essentially what we will do is use this as a dependency for instance any user that wants to use the post method needs to be authenticated  
#so this can be used inside the post method like we did for dp session dependency we can use this method to basically validate that the user is authenticated
#so basically any time the user tries to use any path or like resources that requires them to be logged in we except them to have a valid toekn and 
#we created  this method  to verify that i know it sounds a little  complicated   but just be aware of it  

#so here in the methods using like data token .. it can be anything ... i logic of assignment and comparison like decode encode comes from the jwt library 
#i just have to focus on the logic 