from pydantic import BaseModel, Field

class LibroCreate(BaseModel):
    titulo: str = Field(..., min_length=1)
    autor: str = Field(..., min_length=1)
    isbn: str = Field(..., min_length=5)
    stock: int = Field(..., ge=0)

class LibroUpdate(BaseModel):
    titulo: str
    autor: str
    isbn: str
    stock: int

class LibroResponse(BaseModel):
    id: int
    titulo: str
    autor: str
    isbn: str
    stock: int

    class Config:
        from_attributes = True

        