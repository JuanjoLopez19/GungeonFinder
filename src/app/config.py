import os
import pathlib

from dotenv import load_dotenv


def load():
    if os.path.exists(os.path.join(pathlib.Path(__file__), ".env")):
        load_dotenv(dotenv_path=os.path.join(pathlib.Path(__file__), ".env"))
    else:
        load_dotenv()
