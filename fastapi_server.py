from fastapi import FastAPI

app = FastAPI()

counter = 0

@app.get("/")
def read_root():
    return {"counter": counter}

@app.post("/increment")
def increment_counter():
    global counter
    counter += 1
    return {"counter": counter}
