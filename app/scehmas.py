from pydantic import BaseModel
from typing import Optional

# ===========================================================
# Pydantic Model - Request Validation Schema
# ===========================================================
class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    created_at: Optional[str] = None

