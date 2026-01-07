from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("", response_model=schemas.CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(payload: schemas.CourseCreate, db: Session = Depends(get_db)):
    course = models.Course(code=payload.code, name=payload.name)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.get("", response_model=list[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).order_by(models.Course.id.asc()).all()

@router.get("/{course_id}", response_model=schemas.CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: int, payload: schemas.CourseUpdate, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if payload.code is not None:
        course.code = payload.code
    if payload.name is not None:
        course.name = payload.name

    db.commit()
    db.refresh(course)
    return course

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return None


# OPTIONAL: enroll a user in a course (many-to-many)
@router.post("/enroll/{user_id}", status_code=200)
def enroll_user(user_id: int, payload: schemas.EnrollmentIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    course = db.query(models.Course).filter(models.Course.id == payload.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course in user.courses:
        return {"message": "Already enrolled"}

    user.courses.append(course)
    db.commit()
    return {"message": "Enrolled successfully"}
