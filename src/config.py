import os
import pathlib

from dotenv import load_dotenv


def load():
    if os.path.exists(
        os.path.join(pathlib.Path(__file__).parent.parent, "docker", "python", ".env")
    ):
        load_dotenv(
            dotenv_path=os.path.join(
                pathlib.Path(__file__).parent.parent, "docker", "python", ".env"
            )
        )
    else:
        load_dotenv()
