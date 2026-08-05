from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db
import models, schemas
from datetime import date, datetime, timedelta
from auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"message":"QueryDB is now Online!"}

@app.post("/users/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized! User does not Exist!")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Unauthorized! Incorrect Password!")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type":"bearer"}

@app.post("/users/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists!")
    password_hashed = hash_password(user.password)
    db_user = models.User(email = user.email, hashed_password = password_hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/queries", response_model = schemas.QueryResponse)
def create_query(query: schemas.QueryCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    db_query = models.Query(
        query_name = query.query_name,
        query_sql = query.query_sql,
        report_type = query.report_type,
        created_by = current_user_id
    )

    if query.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(query.tag_ids)).all()
        db_query.tags = tags

    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query

@app.get("/queries", response_model = list[schemas.QueryResponse])
def get_queries(search: str=None, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    queries = db.query(models.Query).filter(models.Query.created_by == current_user_id)
    if search:
        queries = queries.filter(
            (models.Query.query_name.contains(search)) | (models.Query.query_sql.contains(search))
        )
    queries = queries.all()
    return queries

@app.get("/queries/{query_id}", response_model = schemas.QueryResponse)
def get_query_by_id(query_id: int, db:Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    filtered_query = db.query(models.Query).filter(models.Query.id == query_id).first()
    if filtered_query is None:
        raise HTTPException(status_code = 404, detail= "Query Not Found!")
    if filtered_query.created_by != current_user_id:
        raise HTTPException(status_code = 403, detail= "Not Authorized to access this Query")
    return filtered_query

@app.delete("/queries/{query_id}")
def delete_query_by_id(query_id: int, db:Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    filtered_query = db.query(models.Query).filter(models.Query.id == query_id).first()
    if filtered_query is None:
        raise HTTPException(status_code=404, detail="Query to be deleted is not found")
    if filtered_query.created_by != current_user_id:
        raise HTTPException(status_code=403, detail="Not Authorized to access this Query!")
    db.delete(filtered_query)
    db.commit()
    return {"message": f"Query '{filtered_query.query_name}' deleted successfully!"}

@app.put("/queries/{query_id}", response_model=schemas.QueryResponse)
def update_query(query_id: int, query_update: schemas.QueryUpdate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    filtered_query = db.query(models.Query).filter(models.Query.id == query_id).first()
    if filtered_query is None:
        raise HTTPException(status_code=404, detail="Query to update not found!")
    if filtered_query.created_by != current_user_id:
        raise HTTPException(status_code=403, detail="Not Authorized to update this Query")

    if query_update.query_name is not None:
        filtered_query.query_name = query_update.query_name
    if query_update.query_sql is not None:
        filtered_query.query_sql = query_update.query_sql
    if query_update.report_type is not None:
        filtered_query.report_type = query_update.report_type

    if query_update.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(query_update.tag_ids)).all()
        filtered_query.tags = tags

    db.commit()
    db.refresh(filtered_query)
    return filtered_query

@app.post("/tags", response_model=schemas.TagResponse)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    existing_tag = db.query(models.Tag).filter(
        models.Tag.name == tag.name,
        models.Tag.created_by == current_user_id
    ).first() # Do the existing_tag check first
    
    if existing_tag:
        raise HTTPException(status_code=400, detail="Tag already exists!")
    
    db_tag = models.Tag(name=tag.name, created_by=current_user_id) # And then create the new tag
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@app.get("/tags", response_model = list[schemas.TagResponse])
def get_tags(search: str=None, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    tags = db.query(models.Tag).filter(models.Tag.created_by == current_user_id)
    if search:
        tags = tags.filter(
            (models.Tag.name.contains(search)) 
        )
    tags = tags.all()
    return tags

@app.delete("/tags/{tag_id}")
def delete_tag_by_id(tag_id: int, db:Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    filtered_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if filtered_tag is None:
        raise HTTPException(status_code=404, detail="Tag to be deleted is not found")
    if filtered_tag.created_by != current_user_id:
        raise HTTPException(status_code=403, detail="Unauthorized user")
    db.delete(filtered_tag)
    db.commit()
    return {"message":f"Tag '{filtered_tag.name}' deleted successfully!"}
