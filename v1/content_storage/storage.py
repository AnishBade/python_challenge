import os

folder = None

def store_pages(root_url):
    global folder
    folder = f'{root_url.replace("://", "")}'  
    os.makedirs(folder, exist_ok=True)
    
    pages = get_pages()
    for url, content in pages.items():
        file_path = url.replace(root_url, "")        
        with open(f'{folder}/{file_path}', 'wb') as f:
            f.write(content)
            
def get_page(path):
    filepath = f'{folder}/{path}'
    if os.path.exists(filepath):  
        with open(filepath, 'rb') as f:
            return f.read()

    return None