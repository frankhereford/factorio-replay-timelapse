from flask import Flask, send_file, make_response
from PIL import Image, ImageDraw, ImageFont
import io
import redis
import base64
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379)

def generate_tile(label, zoom, x, y):
    # Create a 256x256 transparent image
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a 3px 50% clear border
    border_color = (0, 0, 0, 128)
    draw.rectangle([0, 0, 255, 255], outline=border_color, width=3)

    # Add text to the image
    text = f'{label}: Zoom: {zoom}, X: {x}, Y: {y}'
    font = ImageFont.load_default()
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_position = ((256 - text_width) // 2, (256 - text_height) // 2)
    draw.text(text_position, text, fill=(0, 0, 0, 255), font=font)

    # Save the image to a bytes buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

@app.before_request
def clear_cache():
    # The following line will remove this handler, making it
    # only run on the first request
    app.before_request_funcs[None].remove(clear_cache)
    redis_client.flushall()
    
    logging.debug('Cache cleared 🗑️')

@app.route('/debug/<int:zoom>/<int:x>/<int:y>.png')
def debug_tile(zoom, x, y):
    label = 'debug'
    cache_key = f'{label}:{zoom}:{x}:{y}'
    cached_image = redis_client.get(cache_key)

    if cached_image:
        logging.debug(f'Cache hit 🎉 for key: {cache_key}')
        buffer = io.BytesIO(base64.b64decode(cached_image))
    else:
        logging.debug(f'Cache miss ❌ for key: {cache_key}')
        buffer = generate_tile(label, zoom, x, y)
        redis_client.set(cache_key, base64.b64encode(buffer.getvalue()))

    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)