local config = {
    base_directory = "chunk-screenshots",
    zoom_level = 10,
    tile_size = 2048,  -- 4x4 chunks, each chunk is 512x512
    anti_alias = true,
    show_entity_info = false,
    ticks_per_screenshot = 3000
}

local function ensure_directory(path)
    helpers.write_file(path .. "/.chunk-screenshots", "", false)
end

local function get_slippy_map_path(tick, z, x, y)
    return string.format("%s/%d/%d/%d", config.base_directory, tick, z, x),
           string.format("%d.png", y)
end

local function chunk_to_slippy(chunk_x, chunk_y)
    return math.floor(chunk_x / 4), math.floor(chunk_y / 4)
end

local function screenshot_tile(surface, tick, z, x, y)
    local center_x = (x * 128) + 64  -- 4 chunks * 32 tiles per chunk
    local center_y = (y * 128) + 64  -- 4 chunks * 32 tiles per chunk
    local dir, filename = get_slippy_map_path(tick, z, x, y)
    ensure_directory(dir)
    game.take_screenshot{
        surface = surface,
        position = {x = center_x, y = center_y},
        resolution = {config.tile_size, config.tile_size},
        zoom = 1,  -- Adjust to match "slippy" tile scale
        path = dir .. "/" .. filename,
        show_entity_info = config.show_entity_info,
        anti_alias = config.anti_alias,
        quality = 100,
        allow_in_replay = true,
        daytime = 0
    }
end

local function run()
    script.on_nth_tick(config.ticks_per_screenshot, function(event)
        local surface = game.surfaces[1]
        local processed_chunks = {}
        for chunk in surface.get_chunks() do
            local x, y = chunk_to_slippy(chunk.x, chunk.y)
            local key = x .. "," .. y
            if not processed_chunks[key] then
                screenshot_tile(surface, event.tick, config.zoom_level, x, y)
                processed_chunks[key] = true
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