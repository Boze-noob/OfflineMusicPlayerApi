from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {'example' : 'Hello World', 'data': 0}