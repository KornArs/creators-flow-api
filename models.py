from pydantic import BaseModel, Field 
from typing import Optional, List 
from datetime import datetime 
 
class User(BaseModel): 
    id: int 
    telegram_id: int 
    username: Optional[str] = None 
    full_name: Optional[str] = None 
    role: Optional[str] = None 
    registration_date: Optional[datetime] = None 
    last_activity: Optional[datetime] = None 
 
class Order(BaseModel): 
    id: int 
    brand_id: int 
    product_description: str 
    video_count: int 
    audience: Optional[str] = None 
    style_preferences: Optional[str] = None 
    deadline: int 
    brief: Optional[str] = None 
    status: str 
    created_at: datetime 
    updated_at: Optional[datetime] = None 
 
class OrderSummary(BaseModel): 
    id: int 
    product_description: str 
    video_count: int 
    status: str 
    deadline: int 
    created_at: datetime 
 
class Video(BaseModel): 
    id: int 
    order_id: int 
    creator_id: int 
    file_id: Optional[str] = None 
    content_type: Optional[str] = None 
    public_url: Optional[str] = None 
    preview_url: Optional[str] = None 
    status: Optional[str] = None 
    comment: Optional[str] = None 
    uploaded_at: datetime 
    updated_at: Optional[datetime] = None 
