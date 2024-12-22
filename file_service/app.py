import os
from flask import Flask, request, send_file, render_template_string
from werkzeug.utils import safe_join
from PIL import Image
from io import BytesIO
import logging

logging.basicConfig(level=logging.DEBUG)

available_file_data = 6

app = Flask(__name__)

@app.route('/', defaults={'subpath': ''})
@app.route('/<path:subpath>')
def serve_path(subpath):
    base_dir = os.environ.get('SERVICE_DIRECTORY', '.')
    full_path = safe_join(base_dir, subpath)
    # Extract zoom level from the URL
    zoom_level = extract_zoom_level(subpath)
    logging.debug(f"Zoom level: {zoom_level}")

    if zoom_level != available_file_data:
        parts = subpath.split('/')
        if len(parts) > 1:
            parts[0] = str(available_file_data)
            new_subpath = '/'.join(parts)
            full_path = safe_join(base_dir, new_subpath)
            logging.debug(f"Overloaded full path: {full_path}")

    if os.path.isdir(full_path):
        items_raw = os.listdir(full_path)
        logging.debug(f"Raw directory listing for {full_path}: {items_raw}")
    
        items = sorted(os.listdir(full_path), key=lambda x: (not os.path.isdir(os.path.join(full_path, x)), int(x) if x.lstrip('-').isdigit() else x))
        logging.debug(f"Directory listing for {full_path}: {items}")
        
        links = []
        for item in items:
            item_path = os.path.join(subpath, item)
            if os.path.isdir(os.path.join(full_path, item)):
                links.append(f'<li><a href="/{item_path}">{item}/</a></li>')
            else:
                # Only show PNG images
                if item.lower().endswith('.png'):
                    links.append(
                        f'<li><a href="/{item_path}">'
                        f'<img src="/thumb/{item_path}" alt="{item}" style="height:50px;"> '
                        f'{item}</a></li>'
                    )
        template = f'''
        <h1>Index of /{subpath}</h1>
        <ul>
            {''.join(links)}
        </ul>
        '''
        return render_template_string(template)
    else:
        return send_file(full_path)

@app.route('/thumb/<path:subpath>')
def thumbnail(subpath):
    base_dir = os.environ.get('SERVICE_DIRECTORY', '.')
    logging.debug(f"base_dir: {base_dir}")
    logging.debug(f"subpath: {subpath}")
    full_path = safe_join(base_dir, subpath)
    logging.debug(f"Thumbnail request for: {full_path}")
    zoom_level = extract_zoom_level(subpath)
    logging.debug(f"Zoom level: {zoom_level}")

    if zoom_level != available_file_data:
        parts = subpath.split('/')
        if len(parts) > 1:
            parts[0] = str(available_file_data)
            new_subpath = '/'.join(parts)
            full_path = safe_join(base_dir, new_subpath)
            logging.debug(f"Overloaded full path: {full_path}")

    try:
        with Image.open(full_path) as img:
            img.thumbnail((100, 100))
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            buf = BytesIO()
            img.save(buf, format='JPEG')
            buf.seek(0)
            return send_file(buf, mimetype='image/jpeg')
    except Exception as e:
        logging.error(f"Error creating thumbnail for {full_path}: {e}")
        return "Thumbnail Error", 404

def extract_zoom_level(subpath):
    parts = subpath.split('/')
    if len(parts) > 1 and parts[0].isdigit():
        return int(parts[0])
    return None

if __name__ == "__main__":
    app.run(debug=True)