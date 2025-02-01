import os, random

#REGULAR FUNCTIONS
def cls(): #clears the screen
    os.system('cls' if os.name == 'nt' else 'clear')

def lfds(mydict, key): #return list for dictionary of delimited strings based on key
    if mydict.get(key, False):
        return [item.strip() for item in mydict[key].split(',')]
    else: return False

def randgeneralerror():
    print(random.choice([
    "That's ridiculous...",
    "What? Why?",
    "Error, brain not found",
    "Over my dead body",
    "That's it, you're cut off"]))






