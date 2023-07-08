from fastapi import FastAPI, Body, Path, Query, status, Response
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

app = FastAPI()
app.title = "My app with FastAPI"
app.version = "0.0.1"


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=20)
    year: int = Field(le=datetime.date.today().year)
    category: str = Field(min_length=5, max_length=20)

    # The following replaces the use of "default" as a parameter in each Field()
    class Config:
        schema_extra = {
            "example": {
                "id": 0,
                "title": "Unknown title",
                "year": 2023,
                "category": "Unknown category",
            }
        }


movies = [
    {"id": 1, "title": "Avatar", "year": 2009, "category": "Action"},
    {"id": 2, "title": "Interstellar", "year": 2014, "category": "Sci-fi"},
]


# "tags" is used to group endpoints in the documentation
@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>Hello world!</h1>")


# response_model is used to define and document the schema (structure) of the response
@app.get(
    "/movies",
    tags=["movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
)
def get_movies() -> List[Movie]:
    return movies
    # Both do the same, because FastAPI by default sends an JSONResponse with the content of the return
    # The following is a redundant way
    # return JSONResponse(content=movies)


@app.get(
    "/movies/{id}",
    tags=["movies"],
    response_model=Movie,
    status_code=status.HTTP_200_OK,
)
# Path is used to validate the path parameter
def get_movie(response: Response, id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return item
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=[])
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return []


# Query params have key value
@app.get("/movies/", tags=["movies"], response_model=List[Movie])
# Last slash used to declare that a query param will be received
# Filter movies by category
# ↓↓↓ Query is used because a query param is received !!! ↓↓↓
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=15)
) -> List[Movie]:
    # ↑↑↑ FastAPI detects that category and year are query params ↑↑↑
    return [item for item in movies if item["category"] == category]
    # for item in movies:
    #     if item["category"] == category and item["year"] == year:
    #         return item
    # return []


@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return {"message": "The movie was registered"}


@app.put("/movies/{id}", tags=["movies"], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["year"] = movie.year
            item["category"] = movie.category
            return {"message": "The movie was updated"}


@app.delete("/movies/{id}", tags=["movies"], response_model=dict)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return {"message": "The movie was deleted"}
