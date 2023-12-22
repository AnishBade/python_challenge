# Database connection parameters
DATABASE_URL = "postgresql://username:password@localhost/mydatabase"

async def create_db_connection():
    return await asyncpg.connect(DATABASE_URL)

@app.post("/process-url/", description="Stores a given URL in the database.")
async def process_url(url_input: UrlInput):
    conn = await create_db_connection()
    try:
        await conn.execute('''
            INSERT INTO urls(url) VALUES($1)
        ''', url_input.url)
        return {"message": "URL stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()