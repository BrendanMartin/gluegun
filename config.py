import os

DOTENV_LOC = os.path.join(os.path.dirname(__file__), '.env')
SUBMISSION_DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'extractor', 'submissions')



class Config():
    pass