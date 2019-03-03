from datetime import datetime
from sqlalchemy import Integer, Column, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Submission(Base):
    __tablename__ = 'submission'
    id = Column(Integer, primary_key=True)
    reddit_id = Column(Text, unique=True)
    author = Column(Text)
    created_utc = Column(DateTime)
    num_comments = Column(Integer)
    permalink = Column(Text)
    score = Column(Integer)
    title = Column(Text)
    reddit_video_url = Column(Text)
    reddit_video_duration = Column(Integer)
    reddit_video_height = Column(Integer)
    reddit_video_width = Column(Integer)
    
    def from_praw_object(self, praw_object):
        self.reddit_id = praw_object.id
        self.author = str(praw_object.author)
        self.created_utc = datetime.utcfromtimestamp(praw_object.created_utc)
        self.num_comments = praw_object.num_comments
        self.permalink = praw_object.permalink
        self.score = praw_object.score
        self.title = praw_object.title
        self.reddit_video_url = praw_object.media['reddit_video']['fallback_url']
        self.reddit_video_duration = praw_object.media['reddit_video']['duration']
        self.reddit_video_height = praw_object.media['reddit_video']['height']
        self.reddit_video_width = praw_object.media['reddit_video']['width']

    @property
    def d(self):
        return self.__dict__
    
    def from_kwargs(self, **kwargs):
        self.__dict__.update(kwargs)