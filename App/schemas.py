from pydantic import BaseModel , EmailStr , Field
from datetime import datetime
from typing import Optional,Annotated
from pydantic.types import conint
class User_Response (BaseModel):
    email: EmailStr
    user_id : int 
    created_at : datetime
    class config():
        orm_mode = True
class Post_base(BaseModel):
    #the right side is called field .. the title  , content ... extra 
    name :str
    vlan_id : int
    

class Post_create(Post_base):
    pass
#basically here we used the concept of inheritance to keep a clean modular code .. see i dont have to define 
#the field for every class .. instead i have the main one base model and that class can be inherited by others 
#where i can override or only use the field that i want or even add a filed specific to that class. this makes it a good code 

class Post_Response (Post_base):
    created_at : datetime
    owner_id : int
    owner : User_Response # so this is the whole pydentic model (the class for user response to be resturnd to it ) if it doesnt make sense go to the models and see the relation 1 line code 
    
    
    class config():
        orm_mode = True
class Post_out(BaseModel):
    
    Vlans: Post_Response
    votes: int 
    
    class config():
        orm_mode = True
        
class Create_user (BaseModel):
    email: EmailStr
    password : str
    
    
class User_Login (BaseModel):
    email : EmailStr
    password : str 
        

class Token (BaseModel):
    access_token : str
    token_type : str
    
class Token_Data(BaseModel):
    # remember  this is what we chose to actualy use in the jwt token in my case i chose the user_id .. 
    # so basically here i am trying to make sure the user id is within ... it should be ,, this is safety gain 
    
    # for now i will leave it empty 

    user_id : Optional[int] = None
    
class Vote (BaseModel):
    post_id : int
    #dir : conint(le=1) 
    dir: Annotated[int, Field(le=1, ge=0)]# this is basically saying less than or equals to one the idea here is that a like is 1 and if you say wanna take that back like accedentally liking a pots unliking it so like (1 or 0 kind of thing )