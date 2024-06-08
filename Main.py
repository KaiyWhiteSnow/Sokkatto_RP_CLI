# Library
from rustplus import RustSocket, Command, CommandOptions
import asyncio
import random

# Functions
import events
import jokes


ip = ""
port = ""
steamID = 1
playerToken = 1

async def main():
    options = CommandOptions(prefix="!")
    socket = RustSocket(ip, port, steamID, playerToken, command_options=options)
    await socket.connect()
    await socket.send_team_message(f"Sokkatto: Connected to {ip}:{port}. Good luck and have fun.")

    @socket.command
    async def pop(command: Command):
        info = await socket.get_info()
        await socket.send_team_message(f"There are {info.players}/{info.max_players} players")
        print(f"User {command.sender_name} issued !pop; Status code 0")
        return info
    
    @socket.command
    async def time(command: Command):
        info = await socket.get_time()
        await socket.send_team_message(f"It is {info.time}")
        print(f"User {command.sender_name} issued !time; Status code 0")

    
    @socket.command
    async def dadjoke(command: Command):
        await socket.send_team_message(random.choice(jokes.dad_jokes))
        print(f"User {command.sender_name} issued !dadjoke; Status code 0")
        
    
    
    @socket.command
    async def quote(command: Command):
        await socket.send_team_message(random.choice(jokes.quotes))
        print(f"User {command.sender_name} issued !dadjoke; Status code 0")
    
    
    @socket.command
    async def kiss(command: Command):
        await socket.send_team_message(f"*kisses {command.sender_name} on the forehead*")
        print(f"User {command.sender_name} issued !kiss; Status code 0")
    

    asyncio.create_task(events.check_and_send_events(socket)
    
    
    await socket.hang()

if __name__ == "__main__":
    asyncio.run(main())
