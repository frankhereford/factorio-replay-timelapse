from flask import Flask, send_file, make_response
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import redis
import base64
import logging
import os
import numpy as np

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Connect to Redis
redis_client = redis.Redis(host='10.10.10.1', port=6379)

def generate_debug_tile(label, zoom, x, y):
    # Create a 256x256 transparent image
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a 3px 50% clear border
    border_color = (0, 0, 0, 128)
    draw.rectangle([0, 0, 255, 255], outline=border_color, width=3)

    # Add text to the image
    text = f'Z: {zoom}, X: {x}, Y: {y}'
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    font_size = 20  # Adjust the font size as needed
    font = ImageFont.truetype(font_path, font_size)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_position = (20, 20)

    # Create a layer for the white text
    text_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)

    # Draw the white text multiple times with slight offsets to make it bolder
    offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2), (0, 0)]
    for offset in offsets:
        text_draw.text((text_position[0] + offset[0], text_position[1] + offset[1]), text, fill=(255, 255, 255, 255), font=font)

    # Blur the white text layer with a tighter radius
    blurred_text_layer = text_layer.filter(ImageFilter.GaussianBlur(1))

    # Composite the blurred white text layer under the black text
    img = Image.alpha_composite(img, blurred_text_layer)
    draw = ImageDraw.Draw(img)
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
        logging.info(f'Cache hit 🎉 for key: {cache_key}')
        buffer = io.BytesIO(base64.b64decode(cached_image))
    else:
        logging.info(f'Cache miss ❌ for key: {cache_key}')
        buffer = generate_debug_tile(label, zoom, x, y)
        redis_client.set(cache_key, base64.b64encode(buffer.getvalue()))

    return send_file(buffer, mimetype='image/png')

def generate_still_tile(tick, zoom, x, y):
    label = 'stills'
    cache_key = f'{label}:{tick}:{zoom}:{x}:{y}'
    cached_image = redis_client.get(cache_key)

    base_zoom = 6

    if cached_image:
        logging.info(f'Cache hit 🎉 for key: {cache_key}')
        buffer = io.BytesIO(base64.b64decode(cached_image))
        return buffer
    else:
        logging.info(f'Cache miss ❌ for key: {cache_key}')
        if zoom > (base_zoom + 2):
            logging.debug(f'Zoom level: {zoom} is greater than base_zoom + 2, recursively generating image')
            # Calculate the coordinates for the tile at the previous zoom level
            prev_zoom = zoom - 1
            tile_x = x // 2
            tile_y = y // 2
            logging.debug(f'Previous zoom level: {prev_zoom}, Tile coordinates: ({tile_x}, {tile_y})')
            
            try:
                tile_buffer = generate_still_tile(tick, prev_zoom, tile_x, tile_y)
                tile_image = Image.open(tile_buffer)
            except Exception as e:
                logging.error(f'Error opening tile image: {e}')
                # Create a black image if the file is missing
                tile_image = Image.new('RGB', (256, 256), color='black')
            
            # Calculate the box to crop the image for the current zoom level
            left = (x % 2) * 128
            upper = (y % 2) * 128
            right = left + 128
            lower = upper + 128
            img = tile_image.crop((left, upper, right, lower))
            
            # Resize the cropped image to 256x256
            img = img.resize((256, 256))
            
            # Save the image to a bytes buffer
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            return buf

        elif zoom < base_zoom:
            logging.debug(f'Zoom level: {zoom}, Coordinates: ({x}, {y})')
            # Calculate the coordinates for the four tiles at the next zoom level
            next_zoom = zoom + 1
            tiles = []
            for dx in range(2):
                for dy in range(2):
                    tile_x = x * 2 + dx
                    tile_y = y * 2 + dy
                    logging.debug(f'Next zoom level: {next_zoom}, Tile coordinates: ({tile_x}, {tile_y})')
                    try:
                        tile_buffer = generate_still_tile(tick, next_zoom, tile_x, tile_y)
                        tile_image = Image.open(tile_buffer)
                    except Exception as e:
                        logging.error(f'Error opening tile image: {e}')
                        # Create a transparent image if the file is missing
                        tile_image = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
                    tiles.append(tile_image)
        
            # Create a new blank image to stitch the four tiles together
            stitched_image = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
            stitched_image.paste(tiles[0], (0, 0))
            stitched_image.paste(tiles[2], (256, 0))
            stitched_image.paste(tiles[1], (0, 256))
            stitched_image.paste(tiles[3], (256, 256))
        
            logging.debug('Stitched image created, resizing to 256x256')
            # Resize the stitched image to 256x256
            img = stitched_image.resize((256, 256))
            logging.debug('Image resized to 256x256')

            # Store the image in cache
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
            redis_client.set(cache_key, encoded_image)
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
            source_dir = f'/app/static/nauvis/{tick}'
            if zoom == base_zoom:
                source_image_path = os.path.join(source_dir, f'{transformed_x}/{transformed_y}.png')
            elif zoom == (base_zoom + 1):
                source_image_path = os.path.join(source_dir, f'{transformed_x // 2}/{transformed_y // 2}.png')
            elif zoom == (base_zoom + 2):
                source_image_path = os.path.join(source_dir, f'{transformed_x // 4}/{transformed_y // 4}.png')

            # print(f"source_image_path: {source_image_path}")
            
            # Debugging: Check if the file exists
            if not os.path.exists(source_image_path):
                # logging.error(f'File not found: {source_image_path}')
                # Create a transparent image if the file is missing
                source_image = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
            else:
                try:
                    # Open the source image
                    source_image = Image.open(source_image_path)
                except Exception as e:
                    logging.error(f'Error opening source image: {e}')
                    # Create a transparent image if the file cannot be opened
                    source_image = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
            
            if zoom == (base_zoom + 2):
                # Calculate the box to crop the image for zoom level 8
                left = (transformed_x % 4) * 256
                upper = (transformed_y % 4) * 256
                right = left + 256
                lower = upper + 256
                img = source_image.crop((left, upper, right, lower))
            elif zoom == (base_zoom + 1):
                # Calculate the box to crop the image for zoom level 7
                left = (transformed_x % 2) * 512
                upper = (transformed_y % 2) * 512
                right = left + 512
                lower = upper + 512
                source_image = source_image.crop((left, upper, right, lower))
                img = source_image.resize((256, 256))
            elif zoom == base_zoom:
                # Resize the image to 256x256 for zoom level 6
                img = source_image.resize((256, 256))
            else:
                raise ValueError(f'Unsupported zoom level: {zoom}')

    # Create a grid of dark and light grey boxes
    grid_image = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(grid_image)
    box_size = 128
    for i in range(0, 256, box_size):
        for j in range(0, 256, box_size):
            color = (169, 169, 169) if (i // box_size + j // box_size) % 2 == 0 else (211, 211, 211)
            draw.rectangle([i, j, i + box_size, j + box_size], fill=color)
    
    # Composite the generated image onto the grid
    grid_image.paste(img, (0, 0), img)
    
    # Save the image to a bytes buffer
    buffer = io.BytesIO()
    grid_image.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Store the image in cache
    encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    redis_client.set(cache_key, encoded_image)
    
    return buffer
    
@app.route('/stills/<int:tick>/<int:zoom>/<int:x>/<int:y>.png')
def still_tile(tick, zoom, x, y):
    label = 'stills'
    cache_key = f'{label}:{tick}:{zoom}:{x}:{y}'
    cached_image = redis_client.get(cache_key)

    if cached_image:
        logging.info(f'Cache hit 🎉 for key: {cache_key}')
        buffer = io.BytesIO(base64.b64decode(cached_image))
    else:
        logging.info(f'Cache miss ❌ for key: {cache_key}')
        buffer = generate_still_tile(tick, zoom, x, y)
        redis_client.set(cache_key, base64.b64encode(buffer.getvalue()))

    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)