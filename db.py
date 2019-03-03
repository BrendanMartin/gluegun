import os
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

from app.models import Base, Submission
from config import config
from reddit_api import get_new_submissions

Config = config.get(os.environ.get('FLASK_CONFIG'))
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

def create_db():
    Base.metadata.create_all(engine)

def destroy_db():
    Base.metadata.drop_all(engine)

@contextmanager
def get_session():
    session = sessionmaker(bind=engine)()
    try:
        yield session
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        return
    finally:
        session.close()


def update_submissions():

    check_ids = ', '.join(f"('{i}')" for i in ['awul69', 'awkc5o', '23km1'])
    stmt = text("""
        select t.id 
        from (
          values """ + check_ids + """
        ) as t(id)
        left join submission s on s.reddit_id = t.id
        where s.id is null;
    """)
    with engine.connect() as conn:
        result = conn.execute(stmt).fetchall()
        print([r[0] for r in result])


if __name__ == '__main__':
    update_submissions()
    # destroy_db()
    # create_db()
    #
    # submissions = list(get_new_submissions('diwhy'))
    # with get_session() as sess:
    #     for s in submissions:
    #         sub = Submission()
    #         sub.from_praw_object(s)
    #         sess.add(sub)

