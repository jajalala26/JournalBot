# pip install spherov2
# pip install bleak
import time

# importing spherov2 functionalities
from spherov2 import scanner

# Prints out all of the Sphero's nearby to search for the
def find_sphero() -> None:
    # Scan for available Sphero devices
    toys = scanner.find_toys()
    
    # OPTIONAL: Print out all of the nearby Sphero's information to find yours,
    #           copy the first field called "address"
    for item in toys:
        print(f"{item.name}: {item.address}")

# Select the desired Sphero
def select_sphero(addy: str):
    toys = scanner.find_toys()
    toy = None
    for item in toys:
        if item.address == addy:
            toy = item
    return toy

