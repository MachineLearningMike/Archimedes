from fastapi import FastAPI

from utils.helper import download
from utils.models import Data

description = """
API description
"""

app = FastAPI(
    title="Project Name",
    description=description,
    version="0.0.1",
    contact={
        "name": "Author",
        "url": "https://example.com",
        "email": "admin@example.com",
    },
)


@app.get("/")
def handle(id: int, name: str):
    return f"GET: {id} - {name}"



    print(df)
    return "success"
