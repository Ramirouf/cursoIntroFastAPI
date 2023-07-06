from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "My app with FastAPI"
app.version = "0.0.1"
movies = [
    {"id": 1, "title": "Avatar", "year": 2009, "category": "Action"},
    {"id": 2, "title": "Interstellar", "year": 2014, "category": "Sci-fi"},
]


# "tags" is used to group endpoints in the documentation
@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>Hello world!</h1>")


@app.get("/movies", tags=["movies"])
def get_movies():
    return movies


@app.get("/movies/{id}", tags=["movies"])
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    return []


# Query params have key value
@app.get("/movies/", tags=["movies"])
# Last slash used to declare that a query param will be received
# Filter movies by category
def get_movies_by_category(category: str, year: int):
    # FastAPI detects that category and year are query params
    for item in movies:
        if item["category"] == category and item["year"] == year:
            return item
    return []


@app.post("/movies", tags=["movies"])
def create_movie(
    id: int = Body(), title: str = Body(), year: int = Body(), category: str = Body()
):
    movies.append({"id": id, "title": title, "year": year, "category": category})
    return movies


@app.put("/movies/{id}", tags=["movies"])
def update_movie(
    id: int, title: str = Body(), year: int = Body(), category: str = Body()
):
    for item in movies:
        if item["id"] == id:
            item["title"] = title
            item["year"] = year
            item["category"] = category
            return movies


@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return movies
