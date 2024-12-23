local config = {
    base_directory = "chunk-screenshots",
    zoom_level = 10,
    tile_size = 32,
    anti_alias = true,
    show_entity_info = true,
    ticks_per_screenshot = 15000
}

local function ensure_directory(path)
    helpers.write_file(path .. "/.chunk-screenshots", "", false)
end

local function get_slippy_map_path(tick, z, x, y, offset)
    offset = offset or 128
    local offset_x = x + offset
    local offset_y = y + offset
    return string.format("%s/%d/%d", config.base_directory, tick, offset_x),
           string.format("%d.png", offset_y)
end

local function chunk_to_slippy(chunk_x, chunk_y)
    return chunk_x, chunk_y
end

local function screenshot_tile(surface, tick, z, x, y)
    local center_x = (x * 32) + 16  -- 1 chunk * 32 tiles per chunk
    local center_y = (y * 32) + 16  -- 1 chunk * 32 tiles per chunk
    local dir, filename = get_slippy_map_path(tick, z, x, y, 0)
    ensure_directory(dir)
    game.take_screenshot{
        surface = surface,
        position = {x = center_x, y = center_y},
        resolution = {config.tile_size * 32, config.tile_size * 32},
        zoom = 1,  -- Adjust to match "slippy" tile scale
        path = dir .. "/" .. filename,
        show_entity_info = config.show_entity_info,
        anti_alias = config.anti_alias,
        quality = 80,
        allow_in_replay = true,
        daytime = 0
    }
end

            -- local x, y = chunk_to_slippy(chunk.x, chunk.y)
            -- local key = x .. "," .. y
            -- if not processed_chunks[key] then
            --     log("Processing chunk at: " .. chunk.x .. ", " .. chunk.y)
            --     -- screenshot_tile(surface, event.tick, config.zoom_level, x, y)
            --     processed_chunks[key] = true
            -- end

-- ...existing code...

local function run()
    script.on_nth_tick(config.ticks_per_screenshot, function(event)
        local surface = game.surfaces[1]
        local chunks = {
            min_x = math.huge,
            min_y = math.huge,
            max_x = -math.huge,
            max_y = -math.huge
        }
        
        for chunk in surface.get_chunks() do
            log("Processing chunk at: " .. chunk.x .. ", " .. chunk.y)
            
            if chunk.x < chunks.min_x then
                chunks.min_x = chunk.x
            end
            if chunk.y < chunks.min_y then
                chunks.min_y = chunk.y
            end
            if chunk.x > chunks.max_x then
                chunks.max_x = chunk.x
            end
            if chunk.y > chunks.max_y then
                chunks.max_y = chunk.y
            end
        end
        
        log("Chunks boundaries: min_x=" .. chunks.min_x .. ", min_y=" .. chunks.min_y .. ", max_x=" .. chunks.max_x .. ", max_y=" .. chunks.max_y)

        for x = chunks.min_x, chunks.max_x do
            for y = chunks.min_y, chunks.max_y do
                log("Iterating chunk at: " .. x .. ", " .. y)
                -- Add your processing code here
                -- For example, you can call screenshot_tile function
                local slippy_x, slippy_y = chunk_to_slippy(x, y)
                screenshot_tile(surface, event.tick, config.zoom_level, slippy_x, slippy_y)
            end
        end
    end)

    script.on_event(defines.events.on_player_joined_game, function(_)
        game.surfaces[1].show_clouds = false
    end)
end

return {
    run = run,
    config = config
}