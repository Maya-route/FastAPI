from fastapi import FastAPI , Response , status , HTTPException , Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional , List
from random import randrange
from psycopg2.extras import RealDictCursor
from passlib.context import CryptContext
import time
from sqlalchemy.orm import session
from .import  models 
from .database import engine , get_db 
from .import schemas , utils 
from .routers import post , users , auth , vote
from.config import Settings
from fastapi.middleware.cors import CORSMiddleware




#our API instance
app = FastAPI()

# the below is a really fun topic the middleware so if your api is runnin gon the same domin as your domain then cros is just allowed by default 
# but if you say are trying to reach your API from a different domain like google for exmaple .. you will get a cros error 
#so basically in simple english its about allowing  the API ends to be able to communicate ..see the allow methods you can deside what http metgos are 
# allowed for instance you can only allow to get but no put or post 
# you can put [*] to mean everything 

#so on the below list you can keep adding urls that should be allowed to touch  your API 

#if you are building it for a specific domain you have to make sure that mention those domain 
# here .. its security best practice to narrow them unless you are building a public API 


origins= ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



models.Base.metadata.create_all(bind=engine)

#on the below all we are doing is telling the library i just imported which is passlib to use the bcrypt algorithm for hashing 

pwd_context = CryptContext(schemes=["bcrypt"] , deprecated = "auto")

#The best part about Fast API is that you can automatically generate a documentation for your API .. so when you make a chnage on that API 
#you can automatically generate a documentation for it .. and its a very fast process 
#its called swagger UI , there is also another way of automatic documentation which is called redoc ... it does the excat smae thing but different format 
# use the http://127.0.0.1:8000/docs for swagger UI and http://127.0.0.1:8000/redoc .. for the second option both are amazing 

        
# i will be using pydantic which is a very common module that is independent of FAST API it just 
#simply is a very widely used module that is used to validate Data ... for like schema 

#the most important command for connecting it all .. is 
app.include_router(post.router) 
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
# its like importing all the routes in here 
#so basically whats happening as we run is that it hits the app.include command which is pike saying go and see if 
#there is a match there for the path 

#technically this is called a path operation or like the route operation / path operation  
@app.get("/")
def root():
    return {"message": "Hello World"}
#pretty clean so far but as we keep on working on different path operations   the file is going to get long and unmanageble and not modular enoigh 
#so the standard is to break them out like for example  here i have posts and also users .. we will break them out 
#and use a special way of handling them as we break them out every API frame work has its own way of doing it this is how FAST API does it and thats how we will implement it but the general technical term 
#to it creating routes or simply routers funny huh 
