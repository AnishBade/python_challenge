import typer 
from crawler import crawl, base_url  
from storage import store_pages
from webserver import serve

app = typer.Typer()

@app.command()
def crawl(url: str):
    base_url = url
    crawl(url)
    store_pages(base_url)

@app.command()   
def serve():
    serve()

if __name__ == "__main__": 
    app()