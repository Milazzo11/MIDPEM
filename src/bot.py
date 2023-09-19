"""
Test MIDPEM connected bot.

:author: Max Milazzo
"""


import time
import multiprocessing


def test_func(x: int) -> None:
    """
    Test function run in a process.
    
    :param x: test parameter
    """
    
    while True:
        print(f"Hello from process {x}")
        time.sleep(1)
    

def cleanup() -> None:
    """
    Program exit cleanup.
    """
    
    print("Clean-up")
    
    
def end() -> None:
    """
    Program exit.
    """
    
    print("Exit")


def main() -> tuple:
    """
    Connected bot start signal entry point.
    
    :return: list of initiated processess, clean-up function,
        post-termination function
    """

    processes = []

    for x in range(10):
        p = multiprocessing.Process(target=test_func, args=(x,))
        p.start()
        # start processes
        
        processes.append(p)
        # add processes to tracking list
        
    return processes, cleanup, end