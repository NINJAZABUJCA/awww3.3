from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import List


app = FastAPI()


SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Tag(Base):
    __tablename__ = "stronaglownaobrazoowa_tag"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Image(Base):
    __tablename__ = "stronaglownaobrazoowa_image"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)
    data_publikacji = Column(DateTime, default=datetime.now)

class TagImage(Base):
    __tablename__ = "stronaglownaobrazoowa_image_tags"
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer)
    tag_id = Column(Integer)

    @app.get("/tags", response_model=None)
    def get_images(db: Session = Depends(get_db)):
        query = db.query(Tag.name, func.count(TagImage.image_id)). \
            join(TagImage, Tag.id == TagImage.tag_id). \
            group_by(Tag.id)

        tag_image_counts = query.all()

        result = [{"tag_name": name, "image_count": count} for name, count in tag_image_counts]

        return result

    @app.get("/images", response_model=None)
    def list_images_with_tags(db: Session = Depends(get_db)):
        images = db.query(Image).all()

        images_with_tags = []
        for image in images:
            tags = db.query(Tag.name).join(TagImage, Tag.id == TagImage.tag_id).filter(
                TagImage.image_id == image.id).all()
            tag_names = [tag[0] for tag in tags]

            image_data = {
                "id": image.id,
                "image": image.image,
                "data_publikacji": image.data_publikacji,
                "tags": tag_names
            }
            images_with_tags.append(image_data)

        return images_with_tags


    @app.get("/images/{tag}", response_model=None)
    def list_images_by_tag(tag: str, db: Session = Depends(get_db)):
        db_tag = db.query(Tag).filter(Tag.name == tag).first()

        images = db.query(Image). \
            join(TagImage, Image.id == TagImage.image_id). \
            filter(TagImage.tag_id == db_tag.id).all()

        images_data = []
        for image in images:
            image_data = {
                "id": image.id,
                "image": image.image,
                "data_publikacji": image.data_publikacji,
            }
            images_data.append(image_data)
        return images_data

    @app.post("/images/del")
    def delete_images(image_ids: List[int], db: Session = Depends(get_db), response_model=None):
        # Sprawdzamy, czy przekazano jakieś identyfikatory obrazków

        # Kasujemy obrazy o podanych identyfikatorach
        deleted_count = db.query(Image).filter(Image.id.in_(image_ids)).delete(synchronize_session=False)
        db.commit()

        return None