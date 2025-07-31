from ..import models, schemas , oath2
from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter  
from sqlalchemy.orm import session
from sqlalchemy import func
from ..database import get_db # we left engine  on the main file 
from typing import Optional , List

router = APIRouter(prefix= "/posts" , tags=['Posts'])




#the first path operation that matches is going to be the one that runs ... once it finds a match it stops 
#so its pretty much like how ACLS work 
#order always matters

# i changed it to list because for the rest it worked because its just one value but this is is a list of everything and pydantic model by itself 
# doesnt do the list so i imported list from typing model and changed  the response to list 


@router.get("/", response_model= list[schemas.Post_out]) 

#@router.get("/")
def get_posts(db :session = Depends(get_db), current_user : int = Depends(oath2.get_current_user) 
              ,limit : int = 4 , skip : int = 0 , search: Optional[str] = ""): # this is like what we call creating a dependency 
    #if you only wanna get the posts made only by the loged in user (the current user ) you can edit the filter code to the below
    #posts = db.query(models.Vlans).filter(models.Vlans.owner_id == current_user.user_id).all()
    posts = db.query(models.Vlans).filter(models.Vlans.name.contains(search)).limit(limit).offset(skip).all()
    
    
    #in reality usually we work with data bases with combined info .. like you may not want to filter over just one table ..we may want to merge info from multiple tables and look through that 
    #and for that the we use the powerful method called joins ... basically we are joining info from different tables based on what we need 
    #the tech term is join .. we can work with pgadmin but you know in prod or even test .. thats hard to do version control 
    #so sqlalchamy i mean you can do sql too but ... i will focus on the sql alchamey skill . so the other majior idea besides , tables , relationhips , foreign and compoiste key ... is joints 
    
    #by the way dont stress about the ommand here we are trying to join tables based on requiremet and the end goal is to have a joint table so i can count the nunver of vots a post or in my case a vlan got 
    #come  back and watch the tutur in case anything is ambigious 
    
    result = db.query(models.Vlans , func.count(models.Vlans.vlan_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Vlans.vlan_id , 
                                         isouter= True).group_by(models.Vlans.vlan_id).filter(models.Vlans.name.contains(search)).limit(limit).offset(skip).all()
    
    
    return result
    #the limit inside here is the query parameter .. its like limiting what you get ..
    # the 10 in the method is a default incase you dont provide 
    #{{URL}}/posts?limit=2 this is how you will be testing it on post man the url you give it key value  pair 
    #use %20 in your search bar if you are searching for more than 1 word for example besches%20vlans will give you all entires with those 2 words in them , because we cant use a spave on the url we use %20
    return posts
#working with post method 
#best practice is name the path operation in a way following best practices 

@router.post("/" , status_code=status.HTTP_201_CREATED, response_model=schemas.Post_Response)
def cerate_post(post : schemas.Post_create , db :session = Depends(get_db) , current_user : int = Depends(oath2.get_current_user)):
    #so the last dependency i added is the part where we are protecting the end point ..the jwt token does most of the job and essentially we can also use the current_user variable
    # in our logic as it represents  the current valid authenticated user 
    # you gotta be logged and authenticated to be able to create posts
    # so for all the path operations you want the user to be logged in in order to perform  add user_id : int = Depends(oath2.get_current_user) 
    #as a dependency inside  the method 
    post = models.Vlans(owner_id = current_user.user_id ,**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post) # this is like to return the newly added post 
    
    # the payload here technically is what we call the pydantic model .. like we created it 
    #cursor.execute("""INSERT INTO vlan_management (name , vlan_id) VALUES (%s,%s) RETURNING * """ , (post.name , post.vlan_id))
    #new_post= cursor.fetchone()
    #conn.commit()
    return  post

#mind you this will allow our client  to be posting what ever they want to the server .. or sending what ever they want to the server 
#this is not what we want we want to validate it .. and in technical terms thats what we call prepare the SCHEMA .. its like 
#prepare the laws of it ... like what exactly  is allowed for you to send .
#again be very careful with 
@router.get("/{id}" , response_model=schemas.Post_out)
def get_post(id:int , db :session = Depends(get_db)): # this is a built in way for Fat API to check that the id given is infact integer and if not it throws error 
    #cursor.execute("""SELECT * FROM vlan_management WHERE vlan_id = %s """, (id,))
    #post = cursor.fetchone()
    #post = db.query(models.Vlans).filter(models.Vlans.vlan_id== id).first()
    
    post = db.query(models.Vlans , func.count(models.Vlans.vlan_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Vlans.vlan_id , 
                                         isouter= True).group_by(models.Vlans.vlan_id).filter(models.Vlans.vlan_id== id).first()
    if not post:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND , detail= f'The value with ID = {id} is not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {f'post with {id} was not found'}   
        #The above 3 lines of code is how you would handle like ids that doesn't exist with substance for showing what teh errer is for the clinet end 
        #but there is a way to efficiently handle this with fast api built in module called HTTP exceptions .. normally we call them 
        #exception handling
        
    #if you only wanna get it for the current logged in user add the below piece of code , commented  commented 
        
    #if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail = "Not allowed to perform action ")
       
     
    return post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)



# no body should be able to delete a post other people created we should only delete our own posts so we gotta set up that logic too 

def delete_post (id:int ,db :session = Depends(get_db) , current_user : int = Depends(oath2.get_current_user)) :
    post = db.query(models.Vlans).filter(models.Vlans.vlan_id== id).first()
    #cursor.execute("""DELETE FROM vlan_management WHERE vlan_id = %s returning *""", (id,))
    #Deleted_post= cursor.fetchone()
    #conn.commit()
    if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= f'post with {id} does not exist')
    
    # no body should be able to delete a post other people created we should only delete our own 
    # post the below logic is for that .
    #i will use the same logic for update too .. should only be able to update your own post 
    
    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail = "Not allowed to perform action ")
    
    # we can keep using this logic anywhere we want to see things performed by the current logged  in user only 
    #for instance for get by id .. like it only returns if you are trying to get something that you yourself have created 
    #post.delete(synchronize_session=False)
    
    
    db.delete(post)
    db.commit()
    
@router.put("/{id}")

def update_post(id:int , updated_post : schemas.Post_create ,db :session = Depends(get_db) , current_user : int = Depends(oath2.get_current_user)):
    
    post_query = db.query(models.Vlans).filter(models.Vlans.vlan_id== id)
    post= post_query.first()
    #cursor.execute("""UPDATE vlan_management SET name = %s WHERE  vlan_id = %s returning*""" ,( post.name, id))
    #updated_post=cursor.fetchone()
    #conn.commit()
    if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= f'post with {id} does not exist')
    
    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail = "Not allowed to perform action ")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    
# This is where i will create a registration for uses .. since we are cerating something we are using the post method 
