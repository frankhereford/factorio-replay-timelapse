local config = {
    base_directory = "chunk-screenshots",
    zoom_level = 10,
    tile_size = 32,
    anti_alias = true,
    show_entity_info = true,
    -- ticks_per_screenshot = 60*60*10
    ticks_per_screenshot = 5*60*60,
}


-- local function ensure_directory(path)
--     helpers.write_file(path .. "/.chunk-screenshots", "", false)
-- end

local function get_slippy_map_path(tick, z, x, y, offset)
    offset = offset or 128
    local offset_x = x + offset
    local offset_y = y + offset
    return string.format("%d/%d", tick, offset_x),
           string.format("%d.png", offset_y)
end

local function chunk_to_slippy(chunk_x, chunk_y)
    return chunk_x, chunk_y
end

local function screenshot_tile(surface, surface_index, tick, z, x, y)
    local center_x = (x * 32) + 16  -- 1 chunk * 32 tiles per chunk
    local center_y = (y * 32) + 16  -- 1 chunk * 32 tiles per chunk
    local dir, filename = get_slippy_map_path(tick, z, x, y, 0)
    -- ensure_directory(dir)
    local path = surface_index .. "/" .. dir .. "/" .. filename
    -- log("Using path: " .. path)
    game.take_screenshot{
        surface = surface,
        position = {x = center_x, y = center_y},
        resolution = {config.tile_size * 32, config.tile_size * 32},
        zoom = 1,  -- Adjust to match "slippy" tile scale
        path = path,
        show_entity_info = config.show_entity_info,
        anti_alias = config.anti_alias,
        quality = 80,
        allow_in_replay = true,
        daytime = 0
    }
end

local function process_chunks_or_entities(bounds, surface, surface_index, event, config)
    for x = bounds.min_x, bounds.max_x do
        for y = bounds.min_y, bounds.max_y do
            log("Iterating chunk at: " .. x .. ", " .. y)
            local slippy_x, slippy_y = chunk_to_slippy(x, y)
            screenshot_tile(surface, surface_index, event.tick, config.zoom_level, slippy_x, slippy_y)
        end
    end
end

local function run()
    script.on_nth_tick(60 * 30, function(event)
        -- if event.tick <= 3537000 then
        --     return
        -- end
    
        local tick = event.tick
        local ticks_per_screenshot = config.ticks_per_screenshot
    
        -- Determine the position within the "family" of screenshots
        local position_in_family = tick % ticks_per_screenshot
    
        -- if position_in_family == 0 or position_in_family == 15 or position_in_family == 30 or position_in_family == 45 then
        if true then
            for surface_index, surface in pairs(game.surfaces) do
                local entities = {
                    min_x = math.huge,
                    min_y = math.huge,
                    max_x = -math.huge,
                    max_y = -math.huge
                }
    
                player = game.get_player(1)
                local entities_list = surface.find_entities_filtered({force = player.force})
                for _, entity in pairs(entities_list) do
                    local selection_box = entity.selection_box
                    log("Entity: " .. entity.name)
                    -- log("Selection box: " .. serpent.line(selection_box))
    
                    -- Update bounding box
                    entities.min_x = math.min(entities.min_x, selection_box.left_top.x)
                    entities.min_y = math.min(entities.min_y, selection_box.left_top.y)
                    entities.max_x = math.max(entities.max_x, selection_box.right_bottom.x)
                    entities.max_y = math.max(entities.max_y, selection_box.right_bottom.y)
                end
    
                -- Divide each number by 32 and round up to the next integer
                entities.min_x = math.ceil(entities.min_x / 32)
                entities.min_y = math.ceil(entities.min_y / 32)
                entities.max_x = math.ceil(entities.max_x / 32)
                entities.max_y = math.ceil(entities.max_y / 32)
    
                -- Ensure the bounding box includes top_left (-3, -3) and bottom_right (3, 3)
                entities.min_x = math.min(entities.min_x, -3)
                entities.min_y = math.min(entities.min_y, -3)
                entities.max_x = math.max(entities.max_x, 3)
                entities.max_y = math.max(entities.max_y, 3)
    
                -- Pad the bounds by 2 in every direction
                entities.min_x = entities.min_x - 2
                entities.min_y = entities.min_y - 2
                entities.max_x = entities.max_x + 2
                entities.max_y = entities.max_y + 2
    
                log("Entities Bounding box: " .. serpent.line(entities))
    
                local chunks = {
                    min_x = math.huge,
                    min_y = math.huge,
                    max_x = -math.huge,
                    max_y = -math.huge
                }
    
                for chunk in surface.get_chunks() do
                    -- log("Processing chunk at: " .. chunk.x .. ", " .. chunk.y)
    
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
    
                -- process_chunks_or_entities(chunks, surface, event, config)
                process_chunks_or_entities(entities, surface, surface_index, event, config)
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