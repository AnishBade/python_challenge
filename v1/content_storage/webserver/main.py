from fastapi import FastAPI
from content_storage import storage
import uvicorn

app = FastAPI()

@app.get("/")
async def get_index():
   return storage.get_page("index.html")
   
@app.get("/{path}")
async def get_page(path):
   return storage.get_page(path)

if __name__ == "__main__":    
    uvicorn.run(app)