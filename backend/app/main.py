from fastapi import FastAPI

# Create an instance of the FastAPI class
# This 'app' object will be the main point of interaction to create all your API.
app = FastAPI()

# Define a "path operation decorator"
# @app.get("/") means this function will handle GET requests to the root path ("/")
@app.get("/")
async def read_root():
    # This function will be called when a client sends a GET request to "/"
    # 'async def' means it's an asynchronous function, good for I/O bound tasks.
    # FastAPI handles running async functions correctly.
    return {"message": "Hello World from ContentWeaver AI Backend!"}

# You can add more endpoints here
@app.get("/ping")
async def ping_pong():
    return {"ping": "pong!"}