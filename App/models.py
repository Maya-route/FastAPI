from .database import Base
from sqlalchemy import Column , Integer , String , Boolean ,ForeignKey
from sqlalchemy.sql.expression import null , text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class Vlans (Base):
    
    __tablename__ = "vlans"
    
    vlan_id = Column(Integer , primary_key = True , nullable= False )
    name = Column(String , nullable=False )
    description = Column(String , server_default= "In_Use", nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default= text('now()'), nullable=False)
    owner_id = Column( Integer , ForeignKey("users.user_id" , ondelete="CASCADE"),nullable = False)
    #so mind you the owner_id is  where i created the foreign  key .. i am creating a relation ship 
    # between the bales , essentially  what this will do is create a column for the foregn key so like the use_id from the users table .. 
    # will have a column  in vlans table too .. in simple words  thats what  happens 
    
    #the below is a powerful way of creating a relationship it has nothing to do with foregn key and stuff .. what 
    #this does in english is that get the user information for the task we are performing 
    #example  say you want to get a post with id = 40 as an exple this relation will also show you who creted it 
    #like it gives extra info 
    
    owner = relationship("Users") # inside is the whole class btw . 
    #after this we go to our schema and add a filed to get the info ,sqlalchamy figures out the relationhip its built in dont worry 
    
    
    
class Users (Base):
    __tablename__ = "users"
    #these are technically called constraints , it just means conditions to be fullfil 
    #user_id = Column(Integer, primary_key= True )
    email = Column(String , nullable= False , unique = True )
    password = Column(String, nullable = False)
    user_id = Column(Integer, primary_key= True )
    created_at = Column(TIMESTAMP(timezone=True), server_default= text('now()'), nullable=False)
    
    
    
    #by the way when ever you edit something  , make a change on sqlalchamy if the table already exists  
    #it does not  do anything unless in a dev env you can delate tables and run the code again that will..
    #create a new table with all the changes you made ... thats something you cant do in prod env 
    #for that we have DB migration tools ,, which we will cover later 
    
class Vote (Base):
    __tablename__ = "votes"
    
    post_id = Column(Integer , ForeignKey(Vlans.vlan_id , ondelete="CASCADE"), primary_key = True , nullable = False )
    user_id = Column(Integer , ForeignKey(Users.user_id , ondelete="CASCADE"), primary_key = True , nullable = False )
    

# so basically here we created a composite key ... this is for like in a solual media where we hit like or like vote for a post 

