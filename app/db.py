from sqlmodel import SQLModel, create_engine, Session, select
from .models import Post
from dotenv import load_dotenv
from os import getenv


load_dotenv()
db_url = getenv("DB_URL")

engine = create_engine(db_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def generate_posts():
    with Session(engine) as session:
        statement = select(Post)
        results = session.exec(statement)
        posts = results.all()

        if len(posts) == 0:
            post_1 = Post(title="Title 1", content="Content 1")
            post_2 = Post(title="Title 2", content="Content 2")
            post_3 = Post(title="Title 3", content="Content 3")
            session.add(post_1)
            session.add(post_2)
            session.add(post_3)
            session.commit()
            print("Initialized the database with initial posts.")
        else:
            print("The database already has posts. Skipping data generation.")
