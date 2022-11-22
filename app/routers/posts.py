from .. import models,schemas,auth2
from typing import List,Optional
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi    import FastAPI , status , HTTPException,Depends,APIRouter
router=APIRouter()

my_posts = [{"title":"title of post 1","content":"content of post1","id":1},{"title":"my favourite foods","content":"I like pizza","id":2}]       

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p  

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"]== id:
          return i

@router.get("/posts",response_model=List[schemas.Postout])
#def get_posts():
def get_posts(db: Session = Depends(get_db),current_user: int=Depends(auth2.get_current_user),Limit : int =10,skip:int=0,search: Optional[str]=""):
    
    posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    #cur.execute("""SELECT * FROM posts; """)
    #post= cur.fetchall()
    results= db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
    print(results)
    return results
    #return {"data":my_posts}     

@router.get("/1")
async def root():
       return {"Hello Akshat Pal"}

#@app.post("/createposts")
#def create_posts(payload: dict = Body(...)):
    #print(payload)
    #return {"new_post": f"title {payload['title']} content: {payload['content']}"}

@router.post("/posts",status_code = status.HTTP_201_CREATED,response_model=schemas.Post)
#def create_posts(post: Post):
def create_posts(post:schemas.responsepost,db: Session = Depends(get_db), current_user: int=Depends(auth2.get_current_user)):

    #post_dict=post.dict()
    #post_dict["id"]=randrange(1,100000)
    #my_posts.append(post_dict)
     #return {"data":post_dict}
    #cur.execute("""INSERT INTO posts (title,content,publish) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.publish))
    #new_post=cur.fetchone()
    #conn.commit()
    print(current_user.id)
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/latest") #we have to keep this above the lastone becoz code is compiled from top to bottom so                            
def get_latestpost():     #to iradicate the ignorance we have to keep it above the last one to make it owrk for us
    post=my_posts[len(my_posts)-1]
    return {"detail":post}

@router.get("/posts/{id}",response_model=schemas.Postout)   #latest is string so we have to keep that first
#def get_post(id: int,response: Response):
def get_post(id: int,db: Session = Depends(get_db),current_user: int=Depends(auth2.get_current_user)):
    #cur.execute(""" SELECT * from posts WHERE id = %s""",str(id))
    #post=cur.fetchone()
    #return{"data":test_post}
    #post = find_post(int(id))
    post=db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id}  was not found')
        #response.status_code=  status.HTTP_404_NOT_FOUND
        #return {'message':f'post with id: {id}  was not found'}
    return post

@router.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)
#def delete_post(id: int):
def delete_post(id: int,db: Session = Depends(get_db),current_user: int=Depends(auth2.get_current_user)):    
    #delete post
    #find the index in the array that has required ID
    #my_post.pop(index)
    #cur.execute("""DELETE FROM posts WHERE id = %s returning * """,str(id))
    #del_post=cur.fetchone()
    #conn.commit()
    del_post= db.query(models.Post).filter(models.Post.id==id)
    post=del_post.first()
    #index=find_index_post(id)
    #if index==None:
    if post==None:
        raise  HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    if post.owner_id!=current_user.id: 
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    del_post.delete(synchronize_session=False)#my_posts.pop(index)
    db.commit()
    #return {"deleted post": del_post}
    return {"message":"the post was sucessfully deleted"}

@router.put("/posts/{id}")
#def update_post(id: int, post:Post):
def update_post(id: int,updated_post:schemas.Post,db: Session = Depends(get_db) ,current_user: int=Depends(auth2.get_current_user)):
    #index=find_index_post(id)
    #if index==None:
        #raise  HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    #post_dict=post.dict()
    #post_dict["id"]=id
    #my_posts[index]=post_dict
    #return {"data": post_dict}
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id:{id} does not exist')
    if schemas.Post.owner_id!=current_user.id: 
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return{"data":post_query.first()}

@router.get("/sqlalchemy")
def test_posts( db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"data":posts}  