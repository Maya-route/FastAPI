# WATCH OUT YOU DON’T HAVE TO PUT ANY PASSWORD RELATED OR SENSITIVE 
# STUFF ON YOUR ACTUAL CODE .. NOW HOW THATD DOENIS USING PYDENTIC MODEL


from pydantic_settings import BaseSettings


class Settings (BaseSettings):
    
    database_port:str
    database_hostname: str
    database_username: str
    database_name:str
    database_password: str 
    SECRET_KEY : str 
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int 

    class Config:
        env_file = ".env"
settings = Settings()


#see all DB connectivity related .. all jwt related env variables [ these are variables that can also change based on the env you are working on ]
#Now we can use the settings.path or all the others as we need .. but see we dont have to expose these variables 
#on our code directly .. they are stored on a machine somewhere ... and with the path too 
# so professionally we can put all our environment  variables here .. like connectivity settings .. passwords like for the JWT database connectivity 


#SO IN PRODUCTION .. YOU WILL BE SETTING ALL THESE ON THE MACHINE ITSELF 
#IN A DEV ENVIRONMENT .. YOU CAN CREATE A .ENV FILE AND ASSIGN VALUES TO ALL THESE IN THERE and use that 