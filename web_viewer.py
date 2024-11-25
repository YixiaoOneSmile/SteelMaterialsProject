from flask import Flask, render_template_string, send_file
import os
base_path = "data/clean_html_data"
app = Flask(__name__)

# HTML模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>文件浏览器</title>
    <meta charset="utf-8">
    <style>
        body { 
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .folder {
            margin: 10px 0;
            padding: 10px;
            background-color: #f0f0f0;
            border-radius: 5px;
        }
        .folder-title {
            font-weight: bold;
            margin-bottom: 5px;
        }
        .file-list {
            margin-left: 20px;
        }
        .file-link {
            color: #0066cc;
            text-decoration: none;
        }
        .file-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>文件浏览器</h1>
    {% for folder in folders %}
    <div class="folder">
        <div class="folder-title">{{ folder.name }}</div>
        <div class="file-list">
            {% for file in folder.files %}
            <div>
                <a class="file-link" href="/view/{{ folder.name }}/{{ file }}" target="_blank">{{ file }}</a>
            </div>
            {% endfor %}
        </div>
    </div>
    {% endfor %}
</body>
</html>
'''

@app.route('/')
def index():

    folders = []
    
    # 遍历文件夹
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
            folders.append({
                'name': folder_name,
                'files': files
            })
    
    return render_template_string(HTML_TEMPLATE, folders=folders)

@app.route('/view/<folder>/<file>')
def view_file(folder, file):
    file_path = os.path.join(base_path, folder, file)
    return send_file(file_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 