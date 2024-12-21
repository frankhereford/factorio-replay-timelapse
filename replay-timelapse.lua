-- Configuration
local config = {
    base_directory = "chunk-screenshots",  -- Base output directory
    chunk_size = 32,                      -- Factorio chunk size in tiles
    tile_size = 256,                      -- Desired pixel size for each tile
    anti_alias = true,                    -- Use anti-aliasing for screenshots
    show_entity_info = false              -- Hide entity info for cleaner maps
}

-- Calculate zoom based on desired tile size
local zoom = config.tile_size / (config.chunk_size * 32) -- 32 is Factorio's pixels per tile

local function ensure_directory(path)
    helpers.write_file(path .. "/.chunk-screenshots", "", false)
end

local function get_chunk_filename(tick, chunk_x, chunk_y)
    local dir = string.format("%s/%d", config.base_directory, tick)
    local filename = string.format("%d/%d.png", chunk_x, chunk_y)
    return dir, filename
end

local function screenshot_chunk(surface, chunk_x, chunk_y, tick)
    -- Calculate center position of chunk in tiles
    local center_x = (chunk_x * config.chunk_size) + (config.chunk_size / 2)
    local center_y = (chunk_y * config.chunk_size) + (config.chunk_size / 2)
    
    -- Create directory path for this tick if it doesn't exist
    local dir, filename = get_chunk_filename(tick, chunk_x, chunk_y)
    ensure_directory(dir)
    
    -- Take the screenshot
    game.take_screenshot{
        surface = surface,
        position = {x = center_x, y = center_y},
        resolution = {config.tile_size, config.tile_size},
        zoom = zoom,
        path = dir .. "/" .. filename,
        show_entity_info = config.show_entity_info,
        anti_alias = config.anti_alias,
        quality = 100,
        allow_in_replay = true,
        daytime = 0  -- Consistent lighting
    }
end

local function run()
    -- Initialize event handlers
    script.on_nth_tick(300, function(event)  -- Screenshot every second
        local surface = game.surfaces[1]  -- Get primary surface
        
        -- Screenshot each chunk
        for chunk in surface.get_chunks() do
            screenshot_chunk(surface, chunk.x, chunk.y, event.tick)
        end
    end)
    
    -- Disable clouds for cleaner screenshots
    script.on_event(defines.events.on_player_joined_game, function(event)
        game.surfaces[1].show_clouds = false
    end)
end

return {
    run = run,
    config = config  -- Expose config for modification
}