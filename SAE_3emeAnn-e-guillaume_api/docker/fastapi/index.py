from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    """La route par def"""
    return {"Hello": "World"}