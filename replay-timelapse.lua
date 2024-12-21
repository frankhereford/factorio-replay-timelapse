local resolution = {x = 1920, y = 1080}
local framerate = 60
local speedup = 300
local output_dir = "replay-timelapse"
local screenshot_filename_pattern = output_dir .. "/%08d-base.png"
local research_progress_filename = output_dir .. "/research-progress.csv"
local events_filename = output_dir .. "/events.csv"
local tile_size_px = 32
local nth_tick = 60 * speedup / framerate

-- User config: set to true if you want to use a static bounding box,
-- or false if you want the script to determine it automatically from uncovered chunks.
local use_configured_bbox = true

-- If use_configured_bbox is true, this box will be used:
local configured_bbox = {
  l = -300,  -- left boundary (tiles)
  r = 300,   -- right boundary (tiles)
  t = -300,  -- top boundary (tiles)
  b = 300,   -- bottom boundary (tiles)
}

function frame_to_timestamp(frame)
  local s = math.floor(frame / framerate)
  local m = math.floor(s / 60)
  local h = math.floor(m / 60)
  local f = frame % framerate
  return string.format("%02d:%02d:%02d:%02d", h, m % 60, s % 60, f)
end

function init_research_csv()
  helpers.write_file(events_filename, "tick,frame,timestamp,event\n", false)
  helpers.write_file(
    research_progress_filename,
    "state,tick,frame,timestamp,research_name,research_progress\n",
    false
  )
end

-- Find bounding box of all generated chunks
function uncovered_bbox()
  local surface = game.surfaces[1]
  local l, r, t, b = math.huge, -math.huge, math.huge, -math.huge
  for chunk in surface.get_chunks() do
    if surface.is_chunk_generated(chunk) then
      local area = chunk.area
      if area.left_top.x < l then l = area.left_top.x end
      if area.left_top.y < t then t = area.left_top.y end
      if area.right_bottom.x > r then r = area.right_bottom.x end
      if area.right_bottom.y > b then b = area.right_bottom.y end
    end
  end

  if l == math.huge then
    return {l=-32, r=32, t=-32, b=32}
  end
  return {l=l, r=r, t=t, b=b}
end

function compute_camera(bbox)
  local center = {
    x = (bbox.l + bbox.r) / 2,
    y = (bbox.t + bbox.b) / 2
  }
  local w_px = (bbox.r - bbox.l) * tile_size_px
  local h_px = (bbox.b - bbox.t) * tile_size_px
  local desired_zoom = math.min(resolution.x / w_px, resolution.y / h_px)

  return {
    position = center,
    zoom = desired_zoom,
  }
end

local current_camera = nil
local frame_num = 0

function watch(tick)
  game.take_screenshot{
    surface = game.surfaces[1],
    position = current_camera.position,
    resolution = {resolution.x, resolution.y},
    zoom = current_camera.zoom,
    path = string.format(screenshot_filename_pattern, frame_num),
    show_entity_info = true,
    daytime = 0,
    allow_in_replay = true,
    anti_alias = true,
    force_render = true,
  }

  local force = game.players[1].force
  if force.current_research then
    helpers.write_file(
      research_progress_filename,
      string.format(
        "current,%s,%s,%s,%s,%s\n",
        tick, frame_num, frame_to_timestamp(frame_num),
        force.current_research.name, force.research_progress
      ),
      true
    )
  else
    helpers.write_file(
      research_progress_filename,
      string.format("none,%s,%s,%s,,\n", tick, frame_num, frame_to_timestamp(frame_num)),
      true
    )
  end

  frame_num = frame_num + 1
end

function watch_base(event)
  if event.tick == 0 then
    init_research_csv()
  end
  watch(event.tick)
end

function run()
  local bbox
  if use_configured_bbox then
    bbox = configured_bbox
  else
    bbox = uncovered_bbox()
  end

  current_camera = compute_camera(bbox)

  script.on_event(defines.events.on_player_joined_game, function(e)
    game.surfaces[1].show_clouds = false
  end)

  script.on_nth_tick(nth_tick, watch_base)

  script.on_event(defines.events.on_research_finished, function(e)
    helpers.write_file(
      events_filename,
      string.format(
        "%s,%s,%s,research-finished,%s\n",
        e.tick, frame_num, frame_to_timestamp(frame_num), e.research.name
      ),
      true
    )
  end)
end

return {
  run = run,
}
