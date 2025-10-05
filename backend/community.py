from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os
from datetime import datetime

router = APIRouter()

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), "community.db")

# ===== Create table if not exists =====
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS community_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT NOT NULL,
            user_name TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ===== Pydantic models =====
class PostMessage(BaseModel):
    disease: str
    user_name: str
    message: str

class CommunityPost(BaseModel):
    id: int
    disease: str
    user_name: str
    message: str
    timestamp: str

# ===== API endpoints =====

@router.post("/post", response_model=CommunityPost)
def create_post(post: PostMessage):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO community_posts (disease, user_name, message)
        VALUES (?, ?, ?)
    """, (post.disease, post.user_name, post.message))
    conn.commit()
    post_id = cursor.lastrowid
    cursor.execute("SELECT * FROM community_posts WHERE id = ?", (post_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return CommunityPost(id=row[0], disease=row[1], user_name=row[2], message=row[3], timestamp=row[4])
    raise HTTPException(status_code=500, detail="Post creation failed")

@router.get("/posts", response_model=List[CommunityPost])
def list_posts(disease: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if disease:
        cursor.execute("SELECT * FROM community_posts WHERE disease = ? ORDER BY timestamp DESC", (disease,))
    else:
        cursor.execute("SELECT * FROM community_posts ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return [CommunityPost(id=row[0], disease=row[1], user_name=row[2], message=row[3], timestamp=row[4]) for row in rows]
