import asyncio
from rustplus import convert_xy_to_grid
from asyncio import sleep

detected_events = []
event_type_names = {
    1: "Player",
    2: "Explosion",
    3: "Vending Machine",
    4: "Chinook",
    5: "Cargo Ship",
    6: "Crate",
    7: "Generic Radius",
    8: "Patrol Helicopter",
}
async def check_and_send_events(socket):
        while True:
            events = await socket.get_current_events()
            for event in list(detected_events):  # Convert set to list to remove items
                if event not in events:
                    await socket.send_team_message(f"Event: {event_name} is no longer on the map.")
                    detected_events.remove(event)
            for event in events:
                event_type = event.type
                if event_type in event_type_names:
                    event_name = event_type_names[event_type]
                    map_size = await socket.get_info()
                    grid = "NULL"
                    if not grid == "NoneType":
                        grid = convert_xy_to_grid((event.x, event.y), map_size.size)
                    
                    if event not in detected_events:
                        detected_events.append(event)
                        await socket.send_team_message(f"New event: {event_name} at Grid {grid}")
                        print(f"New event found; Status 0")
            await asyncio.sleep(8)


async def check_member_status(socket):
    await socket.send_team_message("Check_member_status initialized")
    
    player_info = {}

    while True:
        team_info = await socket.get_team_info()

        for member in team_info.members:
            map_size = await socket.get_info()
            grid = convert_xy_to_grid(coords=(member.x, member.y), map_size=map_size.size)
            grids = "".join(map(str, grid))
            
            # Use memory address as a unique identifier
            member_id = id(member)

            if member_id not in player_info:
                # If the player is not in the local dictionary, add them
                player_info[member_id] = {'is_alive': member.is_alive, 'grid': grids, 'death_notified': False}

            if member.is_alive != player_info[member_id]['is_alive']:
                # If the player's status has changed, update the local copy
                player_info[member_id]['is_alive'] = member.is_alive

                if not member.is_alive and not player_info[member_id]['death_notified']:
                    # Send death message only once for each death
                    player_info[member_id]['death_notified'] = True
                    print(f"{member.name} died at {grids}; Status 0")
                    await socket.send_team_message(f'{member.name} died at {grids}')
                elif member.is_alive:
                    # Reset death notification flag when the player is alive again
                    player_info[member_id]['death_notified'] = False

        await asyncio.sleep(5)