"""
MIDPEM Internal API.

:author: Max Milazzo
"""


import time
import shlex
import subprocess
import multiprocessing
import discord


RESERVED_FILENAMES = ["bot.py", "man.py"]
# list of files than cannot be replaced using "sendfile" command


processes = []
# global variable to hold current active processes managed by program


cleanup = None
# stop command signal cleanup function (run before processes are killed)


end = None
# stop command singla end function (run after processes are killed)


def stop() -> str:
    """
    Stop connected bot processes.
    
    :return: command response message
    """
    
    global processes
    
    try:
        if len(processes) == 0:
            return "%s: [i] device already halted"
            # do not run shutdown procedures on already halted device
    
        if cleanup is not None:
            cleanup()
            # pre-termination clean-up
    
        for process in processes:
            process.terminate()
            # terminate active reported processes
        
        if end is not None:        
            end()
            # end post-termination function
            
        processes = []
        
        return "%s: [*] SHUTDOWN COMPLETE"
        
    except Exception as e:
        return "%s: [!] shutdown failure\n" + str(e)


def start(func: callable, only_halted: bool = False) -> str:
    """
    Stop connected bot.
    
    :param func: connected bot "main" entry point
    :param only_halted: if flag is true, only start halted devices
    :return: command response message
    """
    
    global processes
    global cleanup
    global end
    
    try:
        if only_halted and len(processes) != 0:
            return "%s: [i] device already running"
            # do not restart running device when "only_halted" flag is present
    
        res_msg = "%s: [*] STARTUP COMPLETE"
        
        if len(processes) != 0:
            stop()
            # stop process so bot restarts
            
            res_msg = "%s: [*] RESTART COMPLETE"

        processes, cleanup, end = func()
        # start connected bot and collect reported active processes
        
        return res_msg
        
    except Exception as e:
        return "%s: [!] startup failure\n" + str(e)

        
async def receive_file(ctx) -> str:
    """
    Receive file sent from remote controller.
    
    :param ctx: command context
    :type ctx: Discord context object
    
    :return: command response message
    """
    
    try:
        filenames = []
        files = ctx.message.attachments
        # get command attachments

        for file in files:
            filename = file.filename
            # extract filename
    
            if not filename in RESERVED_FILENAMES:
                await file.save(filename)
                filenames.append(filename)
                # save files and contruct list of names
        
        if len(filenames) == 0:
            return "%s: [i] no files saved"
            # return special message if all file saves were failed
            # (caused by files with reserved names being sent)
            
        return f"%s: [*] {', '.join(filenames)} saved"
        # format base response message and returns
        
    except Exception as e:
        return "%s: [!] file send failure\n" + str(e)
    
    
def return_file(filenames: tuple) -> tuple:
    """
    Fetch files from local system to return to remote controller.
    
    :param filenames: filenames to fetch
    :return: command response message, fetched files
    """
    
    try:
        files = []
        
        for filename in filenames:
            files.append(discord.File(filename))
            # fetch all files
        
        if len(files) == 0:
            return "%s: [i] no files retrieved", None
            # handle no matching files case
            
        elif len(files) == 1:
            return "%s: [*] file retrieved", files
            # handle one matching file case
            
        return "%s: [*] files retrieved", files
        # handle many matching files case
        
    except Exception as e:
        return "%s: [!] file fetch failure\n" + str(e), None
    

def get_status() -> str:
    """
    Get connected bot execution status.
    
    :return: command response message
    """
    
    try:
        if len(processes) == 0:
            return "%s: [i] STATUS -- HALTED"
        else:
            return "%s: [i] STATUS -- RUNNING"
            
    except Exception as e:
        return "%s: [!] status query failure\n" + str(e)
    
    
def shell(cmd: tuple) -> str:
    """
    Execute local shell command.
    
    :param cmd: command to run (passed as tuple containing command/arg info)
    :return: command response message
    """
    
    try:
        parsed_cmd = " ".join(cmd)
        # parse command tuple
        
        result = subprocess.run(
            shlex.split(parsed_cmd), shell=True, capture_output=True, text=True
        )
        # run command and store result
        
        return f"%s: [i] SHELL EXECUTION RESULTS --\n{str(result)}"
        
    except Exception as e:
        return "%s: [!] shell execution failure\n" + str(e)
        
        
def shell_p(cmd: tuple) -> str:
    """
    Execute local shell command in process.
    
    :param cmd: command to run (passed as tuple containing command/arg info)
    :return: command response message
    """
    
    try:
        parsed_cmd = " ".join(cmd)
        # parse command tuple
        
        subprocess.Popen(shlex.split(parsed_cmd), shell=True)
        # run command in new process
        
        return "%s: [i] SHELL PROCESS EXECUTED"
        
    except Exception as e:
        return "%s: [!] shell process execution failure\n" + str(e)
