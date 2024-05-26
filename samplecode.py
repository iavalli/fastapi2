# для библиотек с вызовом через await:

@app.get('/')
async def read_results():
    results = await some_library()
    return results

# для библиотек с вызовом без await:

@app.get('/')
def results():
    results = some_library()
    return results

@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers

# other path operation decorators:
@app.post() # для всех операций с GraphQL
@app.put()
@app.delete()
@app.options()
@app.head()
@app.patch()
@app.trace()

# path operation functions - функции операции пути
async def anyname():

return # любые типы данных, модели Pydantic, 
# будут преобразованы автоматически в json

"""
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
"""
    
# проверка типа параметра пути
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# сначала операции для фиксированных путей, потом - с параметрами
@app.get("/users/admin")
async def read_user_admin():
    return {"user_id": "admin"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


####

from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# Значение "lenet" также можно получить с помощью ModelName.lenet.value


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


##

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

##

# необязательные Query - параметры:
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# path and query parameters in any order
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# required parameter - needy - no default value

@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

# needy - required, skip - in with dafault value 0, limit - non-obligatory int

@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

