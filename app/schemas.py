from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr

class ProjectCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    title: str
    description: Optional[str] = None

class CourseCreate(BaseModel):
    code: str
    name: str

class CourseUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None

class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    name: str

# Optional: enrollments endpoints
class EnrollmentIn(BaseModel):
    course_id: int
