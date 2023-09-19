"""
Multi-Instance Distributed Process Execution Manager.

:author: Max Milazzo
"""


import sys
import shlex
import discord
from bot import main
from man_api import api
from man_api.transmit import transmit
from discord import SyncWebhook
from discord.ext import commands


TOKEN = "MTE1MTI2NDIyMzI4NDk1MzIwMA.GfdZQ3.6UFavcd1Hl9pFxO4wTJlCAf6xMq2Kw89kwCvF8"
# Discord bot interface token


CMD_PREFIX = "$"
# command prefix


with open("id.txt") as f:
    COMPUTER_ID = f.read()
    # get computer identification


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=CMD_PREFIX, intents=intents)
client.remove_command("help")
# create and set up bot


@client.command(name="start", aliases=["st"])
async def _start(ctx, device_id: str) -> None:
    """
    Device-specific start/restart bot process(es) command signal.
    
    :param ctx: command context
    :type ctx: Discord context object
    :param device_id: command execution device identifier
    """
    
    if device_id.lower() == COMPUTER_ID.lower():
        await transmit(
            ctx, f"{COMPUTER_ID}: [i] STARTUP SIGNAL RECEIVED\n" +
                 "[local commands unavailable until complete]"
        )
        # transmit startup receipt confirmation
        # (since startup process/confirmation may take some time depending on
        # the user bot implementation)
        
        res = api.start(main)
        await transmit(ctx, res % COMPUTER_ID, no_cmd=True)


@client.command(name="startall", aliases=["sta"])
async def _start_all(ctx, halted: str = None) -> None:
    """
    Universal start/restart bot process(es) command signal.
    
    :param ctx: command context
    :type ctx: Discord context object
    :param halted: start only halted device if set to "halted"
    """
    
    await transmit(
        ctx, f"{COMPUTER_ID}: [i] STARTUP SIGNAL RECEIVED\n" +
             "[local commands unavailable until complete]"
    )
    # transmit startup receipt confirmation
    # (since startup process/confirmation may take some time depending on
    # the user bot implementation)
    
    only_halted = False
    
    if halted is not None and halted == "halted":
        only_halted = True
        # set "only_halted" flag
    
    res = api.start(main, only_halted=only_halted)
    await transmit(ctx, res % COMPUTER_ID, no_cmd=True)
 
    
@client.command(name="stop", aliases=["sp"])
async def _stop(ctx, device_id: str) -> None:
    """
    Device-specific stop bot process(es) command signal.
    
    :param ctx: command context
    :type ctx: Discord context object
    :param device_id: command execution device identifier
    """
    
    if device_id.lower() == COMPUTER_ID.lower():
        await transmit(
            ctx, f"{COMPUTER_ID}: [i] SHUTDOWN SIGNAL RECEIVED\n" +
                 "[local commands unavailable until complete]"
        )
        # transmit shutdown receipt confirmation
        # (since shutdown/cleanup process may take some time depending on the
        # user bot implementation)
        
        res = api.stop()
        await transmit(ctx, res % COMPUTER_ID, no_cmd=True)


@client.command(name="stopall", aliases=["spa"])
async def _stop_all(ctx) -> None:
    """
    Universal stop bot process(es) command signal.
    
    :param ctx: command context
    :type ctx: Discord context object
    """
    
    await transmit(
        ctx, f"{COMPUTER_ID}: [i] SHUTDOWN SIGNAL RECEIVED\n" +
             "[local commands unavailable until complete]"
    )
    # transmit shutdown receipt confirmation
    # (since shutdown/cleanup process may take some time depending on the
    # user bot implementation)
    
    res = api.stop()
    await transmit(ctx, res % COMPUTER_ID, no_cmd=True)


@client.command(name="sendfiles", aliases=["sendfile", "sf"])
async def _send_files(ctx, device_id: str) -> None:
    """
    Device-specific controller->local file send command signal.
    
    :param ctx: command context
    :type ctx: Discord context object
    :param device_id: command execution device identifier    
    """
    
    if device_id.lower() == COMPUTER_ID.lower():
        res = await api.receive_file(ctx)
        await transmit(ctx, res % COMPUTER_ID)


@client.command(name="sendfilesall", aliases=["sendfileall", "sfa"])
async def _send_files_all(ctx) -> None:
    """
    Universal controller->local file send command signal.
    
    :param ctx: command context
    :type ctx: Discord context object
    """
    
    res = await api.receive_file(ctx)
    await transmit(ctx, res % COMPUTER_ID)


@client.command(name="getfiles", aliases=["getfile", "gf"])
async def _get_files(ctx, device_id: str, *filenames) -> None:
    """
    Device-specific local->controller file transmit command signal.
    
    :param ctx: command context
    :type ctx: Discord context object
    :param device_id: command execution device identifier
    :param filenames: filenames to fetch
    :type filenames: *str
    """
    
    if device_id.lower() == COMPUTER_ID.lower():
        res, files = api.return_file(filenames)
        await transmit(ctx, res % COMPUTER_ID, files)
        
        
@client.command(name="getfilesall", aliases=["getfileall", "gfa"])
async def _get_files_all(ctx, *filenames) -> None:
    """
    Universal local->controller file transmit command signal.
    
    :param ctx: command context
    :type ctx: Discord context object
    :param filenames: filenames to fetch
    :type filenames: *str
    """

    res, files = api.return_file(filenames)
    await transmit(ctx, res % COMPUTER_ID, files)
    
    
@client.command(name="status", aliases=["ss"])
async def _status(ctx, device_id: str = None) -> None:
    """
    Device-specific AND Universal execution status query signal.
    
    :param ctx: command context
    :type ctx: Discord context object
    :param device_id: command execution device identifier
    """
    
    if device_id is None or device_id.lower() == COMPUTER_ID.lower():
        res = api.get_status()
        await transmit(ctx, res % COMPUTER_ID)


@client.command(name="statusall", aliases=["ssa"])
async def _status_all(ctx) -> None:
    """
    Universal execution status query signal (alternate syntax).
    
    :param ctx: command context
    :type ctx: Discord context object
    """

    res = api.get_status()
    await transmit(ctx, res % COMPUTER_ID)
    

@client.command(name="shell", aliases=["sl"])
async def _shell(ctx, device_id: str, *cmd) -> None:
    """
    Device-specific shell command execution command signal.
    
    :param ctx: command context
    :type ctx: Discord context object
    :param device_id: command execution device identifier
    :param cmd: command to run (passed as tuple containing command/arg info)
    :type cmd: *str
    """
    
    if device_id.lower() == COMPUTER_ID.lower():
        res = api.shell(cmd)
        await transmit(ctx, res % COMPUTER_ID)


@client.command(name="shellall", aliases=["sla"])
async def _shell_all(ctx, *cmd) -> None:
    """
    Universal shell command execution command signal.
    
    :param ctx: command context
    :type ctx: Discord context object
    :param cmd: command to run (passed as tuple containing command/arg info)
    :type cmd: *str
    """
    
    res = api.shell(cmd)
    await transmit(ctx, res % COMPUTER_ID)
    
    
@client.command(name="shutdown")
async def _shutdown(ctx, device_id: str) -> None:
    """
    Device-specific MIDPEM manager shutdown signal.
    
    :param ctx: command context
    :type ctx: Discord context object
    :param device_id: command execution device identifier
    """
    
    if device_id.lower() == COMPUTER_ID.lower():
        await transmit(ctx, f"{COMPUTER_ID}: MIDPEM SHUTTING DOWN")
        sys.exit(0)


@client.command(name="shutdownall")
async def _shutdown_all(ctx) -> None:
    """
    Universal MIDPEM manager shutdown signal.
    
    :param ctx: command context
    :type ctx: Discord context object
    """
    
    await transmit(ctx, f"{COMPUTER_ID}: MIDPEM SHUTTING DOWN")
    sys.exit(0)


@client.event
async def on_message(message) -> None:
    """
    Directly handle messages to allow other bots and webhooks to interface with
    MIDPEM and send their own commands.
    
    :param message: server message
    :type message: Discord message object
    """

    if message.author == client.user:
        return
        # exit on current bot message read

    if message.author.bot:
    # allow webhook and bot commands to be processed
    
        command_text = shlex.split(message.content)
        command = client.get_command(command_text[0].replace(CMD_PREFIX, ""))
        ctx = await client.get_context(message)
        # process input command and get context
        
        if len(command_text) == 1:
            await command(ctx)
            # process 0 argument command
            
        else:
            await command(ctx, *command_text[1:])
            # process 1+ argument command

    else:
        await client.process_commands(message)
        # process user commands normally
        # (this allows error detection and messaging to stay on)


@client.event
async def on_command_error(ctx, error) -> None:
    """
    Command error handler.
    
    :param ctx: command context
    :type ctx: Discord context object
    :param error: error
    :type error: Discord error object
    """
    
    await ctx.reply(COMPUTER_ID + ": " + str(error))


@client.event
async def on_ready():
    """
    Display console message on startup.
    """
    
    print("MIDPEM: [listener active]\n")

    
if __name__ == "__main__":
    client.run(TOKEN, log_handler=None)