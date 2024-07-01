from fastapi import FastAPI

app = FastAPI()

@app.get("/hello/{name}")
async def hello(name:str):
    return f"Hello {name}"