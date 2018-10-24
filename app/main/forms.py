from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL


class FindRedditVideoForm(FlaskForm):
    reddit_url = StringField('Reddit submission URL', validators=[URL()])