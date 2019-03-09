import os
from contextlib import contextmanager

from sqlalchemy import create_engine, text, update
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


def update_submissions(subreddit):
    """
    Pulls new submissions from Reddit API and stores them in Postgres
    :return:
    """
    submissions = list(get_new_submissions(subreddit))

    check_ids = ', '.join(f"('{sub.id}')" for sub in submissions)
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

        if not result:  # No new submissions from subreddit
            return False

        safe_ids = [r[0] for r in result]

    with get_session() as sess:
        for submission in submissions:
            if submission.id in safe_ids:
                sub = Submission()
                sub.from_praw_object(submission)
                sess.add(sub)


def retrieve_videos(offset=0, filter_ids=None):
    with get_session() as sess:
        q = sess.query(Submission.reddit_video_url,
                       Submission.reddit_id,
                       Submission.reddit_video_duration,
                       Submission.reddit_video_height,
                       Submission.reddit_video_width) \
            .filter(Submission.no_object == None) \
            .order_by(Submission.created_utc)
        if filter_ids:
            ids = filter_ids if isinstance(filter_ids, list) else [filter_ids]
            q = q.filter(Submission.reddit_id.notin_(ids))
        if offset > 0:
            q = q.offset(offset)
        videos = q.limit(5).all()
        if videos:
            return [v._asdict() for v in videos]

        return False


def store_frame_selections(reddit_id, selections):
    with get_session() as sess:
        submission = sess.query(Submission).filter_by(reddit_id=reddit_id).first()
        submission.object_time_locations = selections
        sess.add(submission)


def store_object_not_in_video(reddit_id):
    with get_session() as sess:
        sess.execute(update(Submission).where(Submission.reddit_id == reddit_id).values(no_object=True))


def compute_statistics():
    stmt = text("""select * from 
(select count(*) as "total_count" from submission ) as total_count, 
(select count(*) as "videos_labeled_count" from submission  where array_length(object_time_locations, 1) > 0) as videos_labeled_count,
(select count(*) as "no_object_count" from submission where no_object = true) as no_object_count,
(select sum(array_length(object_time_locations, 1)) as "labeled_frames_count" from submission) as labeled_frames_count,
(select count(*) as "needs_labeling_count" from submission where object_time_locations is null and no_object is null) as needs_labeling_count
""")

    labels = dict(
        total_count="Videos in database",
        videos_labeled_count="Videos with frames labeled",
        no_object_count="Videos with no object",
        labeled_frames_count="Frames labeled",
        needs_labeling_count="Videos that need labeling"
    )

    with get_session() as sess:
        result = sess.execute(stmt).fetchall()[0]
        result = dict(result)
        fmt_result = dict()
        for k, v in result.items():
            fmt_result[labels[k]] = v
        return fmt_result


if __name__ == '__main__':
    # destroy_db()
    # create_db()
    # update_submissions()
    r = compute_statistics()
    print(r)
    #
    # submissions = list(get_new_submissions('diwhy'))
    # with get_session() as sess:
    #     for s in submissions:
    #         sub = Submission()
    #         sub.from_praw_object(s)
    #         sess.add(sub)
