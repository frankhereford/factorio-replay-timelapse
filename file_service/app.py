import os
from flask import Flask, request, send_file, render_template_string
from werkzeug.utils import safe_join
from PIL import Image
from io import BytesIO
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)




@app.route('/images/', defaults={'subpath': ''})
@app.route('/images/<path:subpath>')
def serve_path(subpath):
    base_dir = os.environ.get('SERVICE_DIRECTORY', '.')
    full_path = safe_join(base_dir, subpath)

    if os.path.isdir(full_path):
            
        items_raw = os.listdir(full_path)
        logging.debug(f"Raw directory listing for {full_path}: {items_raw}")
    
        items = sorted(os.listdir(full_path), key=lambda x: (not os.path.isdir(os.path.join(full_path, x)), int(x) if x.lstrip('-').isdigit() else x))
        logging.debug(f"Directory listing for {full_path}: {items}")
        
        links = []
        for item in items:
            item_path = os.path.join(subpath, item)
            if os.path.isdir(os.path.join(full_path, item)):
                links.append(f'<li><a href="/images/{item_path}">{item}/</a></li>')
            else:
                # Only show PNG images
                if item.lower().endswith('.png'):
                    links.append(
                        f'<li><a href="/images/{item_path}">'
                        f'<img src="/images/thumb/{item_path}" alt="{item}" style="height:50px;"> '
                        f'{item}</a></li>'
                    )
        template = f'''
        <h1>Index of /images/{subpath}</h1>
        <ul>
            {''.join(links)}
        </ul>
        '''
        return render_template_string(template)
    else:
        return send_file(full_path)

@app.route('/images/thumb/<path:subpath>')
def thumbnail(subpath):
    base_dir = os.environ.get('SERVICE_DIRECTORY', '.')
    logging.debug(f"base_dir: {base_dir}")
    logging.debug(f"subpath: {subpath}")
    full_path = safe_join(base_dir, subpath)
    logging.debug(f"Thumbnail request for: {full_path}")

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


if __name__ == "__main__":
    app.run(debug=True)