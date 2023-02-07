from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.getcwd(), '.env'))
from src.app import create_app

application = create_app(__name__)

if __name__ == '__main__':
    application.run()