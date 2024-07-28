from fastapi import FastAPI, Request, Response, HTTPException, Form
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    name: str
    age: int

    def __hash__(self):
        return hash(self.name) + hash(self.age)


users = set()


@app.get("/add")
def add(a: int, b: int) -> int:
    return a + b


@app.post("/users")
def add_user(name: str, age: int) -> User:
    user = User(name=name, age=age)
    if user in users:
        raise HTTPException(status_code=500, detail="User already exists in DB")
    users.add(user)
    return user


@app.get("/users")
def get_users() -> set[User]:
    return users


@app.put("/users/{name}")
def update_user(user: User) -> User:
    user = User(name=user.name, age=user.age)
    if user not in users:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = [l_user for l_user in users if user == l_user]
    updated_user[0].name = user.name
    updated_user[0].age = user.age
    return updated_user[0]


@app.delete("/users")
def delete_user(user: User):
    user = User(name=user.name, age=user.age)
    users.remove(user)


@app.get("/users-ui")
def get_users_ui(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.post("/users-ui")
def get_users_ui(request: Request, name: str = Form(...), age: int = Form(...)):
    add_user(name, age)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})
