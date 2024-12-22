from flask import Flask, send_file, make_response
from PIL import Image, ImageDraw, ImageFont
import io
import redis
import base64
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379)

def generate_debug_tile(label, zoom, x, y):
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
        buffer = generate_debug_tile(label, zoom, x, y)
        redis_client.set(cache_key, base64.b64encode(buffer.getvalue()))

    return send_file(buffer, mimetype='image/png')

def generate_still_tile(tick, zoom, x, y):
    if zoom < 6:
        logging.debug(f'Zoom level: {zoom}, Coordinates: ({x}, {y})')
        # Calculate the coordinates for the four tiles at the next zoom level
        next_zoom = zoom + 1
        tiles = []
        for dx in range(2):
            for dy in range(2):
                tile_x = x * 2 + dx
                tile_y = y * 2 + dy
                logging.debug(f'Next zoom level: {next_zoom}, Tile coordinates: ({tile_x}, {tile_y})')
                tile_buffer = generate_still_tile(tick, next_zoom, tile_x, tile_y)
                tile_image = Image.open(tile_buffer)
                tiles.append(tile_image)
    
        # Create a new blank image to stitch the four tiles together
        stitched_image = Image.new('RGB', (512, 512))
        stitched_image.paste(tiles[0], (0, 0))
        stitched_image.paste(tiles[2], (256, 0))
        stitched_image.paste(tiles[1], (0, 256))
        stitched_image.paste(tiles[3], (256, 256))
    
        logging.debug('Stitched image created, resizing to 256x256')
        # Resize the stitched image to 256x256
        img = stitched_image.resize((256, 256))
        logging.debug('Image resized to 256x256')
    else:
        # Calculate the grid size and center coordinate
        grid_size = 2 ** zoom
        center_x = grid_size // 2
        center_y = grid_size // 2
        logging.debug(f'Grid size: {grid_size}x{grid_size}, Center coordinate: ({center_x}, {center_y})')

        # Transform the incoming coordinates
        transformed_x = x - center_x
        transformed_y = y - center_y
        logging.debug(f'Transformed coordinates: ({transformed_x}, {transformed_y})')

        # Determine the source image path
        source_dir = f'/app/static/{tick}'
        if zoom == 6:
            source_image_path = os.path.join(source_dir, f'{transformed_x}/{transformed_y}.png')
        elif zoom == 7:
            source_image_path = os.path.join(source_dir, f'{transformed_x // 2}/{transformed_y // 2}.png')
        elif zoom == 8:
            source_image_path = os.path.join(source_dir, f'{transformed_x // 4}/{transformed_y // 4}.png')

        # Debugging: Check if the file exists
        if not os.path.exists(source_image_path):
            logging.error(f'File not found: {source_image_path}')
            raise FileNotFoundError(f'File not found: {source_image_path}')

        # Open the source image
        source_image = Image.open(source_image_path)

        if zoom == 8:
            # Calculate the box to crop the image for zoom level 8
            left = (transformed_x % 4) * 256
            upper = (transformed_y % 4) * 256
            right = left + 256
            lower = upper + 256
            img = source_image.crop((left, upper, right, lower))
        elif zoom == 7:
            # Calculate the box to crop the image for zoom level 7
            left = (transformed_x % 2) * 512
            upper = (transformed_y % 2) * 512
            right = left + 512
            lower = upper + 512
            source_image = source_image.crop((left, upper, right, lower))
            img = source_image.resize((256, 256))
        elif zoom == 6:
            # Resize the image to 256x256 for zoom level 6
            img = source_image.resize((256, 256))
        else:
            raise ValueError(f'Unsupported zoom level: {zoom}')

    # Save the image to a bytes buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

@app.route('/stills/<int:tick>/<int:zoom>/<int:x>/<int:y>.png')
def still_tile(tick, zoom, x, y):
    label = 'stills'
    cache_key = f'{label}:{tick}:{zoom}:{x}:{y}'
    cached_image = redis_client.get(cache_key)

    if cached_image:
        logging.debug(f'Cache hit 🎉 for key: {cache_key}')
        buffer = io.BytesIO(base64.b64decode(cached_image))
    else:
        logging.debug(f'Cache miss ❌ for key: {cache_key}')
        buffer = generate_still_tile(tick, zoom, x, y)
        redis_client.set(cache_key, base64.b64encode(buffer.getvalue()))

    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)