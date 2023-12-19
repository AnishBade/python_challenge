from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

# Specify the URL of the website you want to serve locally
website_url = "http://www.bbc.com"

# Specify the local directory to store the website content
local_directory = "bbc_content"

@app.route('/')
def index():
    # Fetch the content of the website
    response = requests.get(website_url)
    content = response.text

    # Save the content to a local file
    # save_path = os.path.join(local_directory, "index.html")
    save_path = "index.html"
    # os.makedirs(save_path, exist_ok=True)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Render the fetched content
    return render_template('index.html', content=content)

if __name__ == '__main__':
    app.run(debug=True)
