import uvicorn
from sqlalchemy import Column, Integer, String, create_engine, Float, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import os
import shutil
import uuid
from pathlib import Path
from datetime import datetime
from validators import DocumentValidator
from wa_score import WAscore
from ig_score import IGscore

# DB config
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model
class Clubs(Base):
    __tablename__ = "clubs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tags = Column(String, index=True)
    community = Column(Float, index=True)
    social = Column(Float, index=True)
    events = Column(Float, index=True)
    collab = Column(Float, index=True)
    votes = Column(Float, index=True)
    overall = Column(Float, index=True)

Base.metadata.create_all(bind=engine)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()

# Initialize Document Validator
doc_validator = DocumentValidator(max_size=25 * 1024 * 1024)

# Import Whatsapp Chat
@app.post("/upload/wa")
async def upload_whatsapp_export(item_id: int, file: UploadFile = File(...)):
    validation = await doc_validator.validate_file(file)

    if not validation["valid"]:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "File validation failed",
                "errors": validation["errors"]
            }
        )

    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )
    
    score = WAscore(file_path)
    db = SessionLocal()
    db_item = db.query(Clubs).filter(Clubs.id == item_id).first()
    db_item.community = score
    db.commit()

    return {
        "success": True,
        "score" : score,
    }


# Scrape Instagram Page
@app.post("/scrape/ig")
async def scrape_instagram_id(item_id: int, username:str):
    score = IGscore(username)
    db = SessionLocal()
    db_item = db.query(Clubs).filter(Clubs.id == item_id).first()
    db_item.social = score
    db.commit()

    return {
        "success": True,
        "score": score,
    }


# Club ranking and clubbing
@app.get("/ranked")
async def club_ranking():
    db = SessionLocal()
    item = db.query(Clubs).order_by(desc(Clubs.overall))
    return item.all()

@app.get("/bins")
async def club_binning():
    db = SessionLocal()
    item = db.query(Clubs).order_by(Clubs.tags)
    return item.all()


# CRUD on the clubs table
@app.post("/clubs/")
async def create_item(name: str, tags: str, community: float, social:float, events:float, votes:float, collab:float, overall:float):
    db = SessionLocal()
    db_item = Clubs(name=name, tags=tags, community=community, social=social, events=events, votes=votes, collab=collab, overall=overall)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/clubs/{item_id}")
async def read_item(item_id: int):
    db = SessionLocal()
    item = db.query(Clubs).filter(Clubs.id == item_id).first()
    return item


@app.put("/clubs/{item_id}")
async def update_item(item_id: int, name: str, tags: str, community: float, social:float, events:float, votes:float, collab:float, overall:float):
    db = SessionLocal()
    db_item = db.query(Clubs).filter(Clubs.id == item_id).first()
    db_item.name = name
    db_item.tags = tags
    db_item.community = community
    db_item.social = social
    db_item.events = events
    db_item.votes = votes
    db_item.collab = collab
    db_item.overall = overall
    db.commit()
    return db_item


@app.delete("/clubs/{item_id}")
async def delete_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(Clubs).filter(Clubs.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return {"message": "Club deleted successfully"}


@app.get("/")
async def root():
    return {"message": "FastAPI is running"}
