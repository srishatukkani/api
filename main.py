from fastapi import FastAPI


import datetime
from peewee import *

DATABASE='tweepee1.db'
database=SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database=database

class User(BaseModel):
    username=CharField(unique=True)
    password=CharField()
    email=CharField()
    join_date=DateTimeField(default=datetime.datetime.now)

class Posts(BaseModel):
    text=CharField()
    username = ForeignKeyField(User)
    post_date=DateTimeField(default=datetime.datetime.now)

class Likes(BaseModel):
    post_id=ForeignKeyField(Posts)
    user_id=ForeignKeyField(User)

def create_tables():
    with database:
        database.create_tables([User])
        database.create_tables([Posts])
        database.create_tables([Likes])

if __name__=='__main__':
    create_tables()

#User.create(username='user1',password='pass1',email='email1')
#User.create(username='user2',password='pass2',email='email2')
#User.create(username='user3',password='pass3',email='email3')
#User.create(username='user4',password='pass4',email='email4')
#User.create(username='user5',password='pass5',email='email5')

#Posts.create(text='wesdrftgyhujik',username='user1')
#Posts.create(text='jghfgdfszxcfhujik',username='user1')
#Posts.create(text='edtrftgyhujik',username='user1')

def get_posts(name):
    for post in Posts.select().where(Posts.username_id == name):
        print(post.username_id, ',', post.text,',',post.post_date)

#get_posts('user1')        

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/users")
def all_users():
    users_list=[]
    for user in User.select():
        users_list.append(user.username + ',' + user.password + ',' + user.email)
    return users_list

@app.get("/user/{name}")
def single_user(name: str):
    users_list=[]
    temp=name+'%'
    for ss in User.select().where(User.username ** temp):
        users_list.append(ss.username+','+ss.password+','+ss.email)
    return users_list

@app.get("/posts/{limit}")
def all_posts(limit:str):
    posts_list=[]
    for post in Posts.select().limit(limit):
        posts_list.append(post.username_id+ ','+ post.text+','+str(post.post_date))
    return posts_list

@app.get("/post/{name}")
def single_post(name: str):
    posts_list=[]
    for post in Posts.select().where(Posts.username_id == name):
        posts_list.append(post.username_id+ ','+ post.text)
    return posts_list

@app.get("/like/{user_id}&{post_id}")
def like(user_id: int,post_id:int):
    Likes.create(user_id=user_id,post_id=post_id)

@app.get("/unlike/{user_id}&{post_id}")
def unlike(user_id: int,post_id:int):
    q=Likes.delete().where(Likes.user_id==user_id & Likes.post_id==post_id)
    q.execute()

@app.get("/del_post/{post_id}")
def del_post(post_id:int):
    q=Posts.delete().where(Posts.id==post_id)
    q.execute()