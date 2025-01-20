import tomllib  
import random
import os
import rich

COMMAND_FAILURES=[
    "That's ridiculous...",
    "What? Why?",
    "Error, brain not found",
    "Over my dead body",
    "That's it, you're cut off"
]

#REGULAR FUNCTIONS
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def lfds(mydict, key): #return list for dictionary of strings bassed on key
    if mydict.get(key, False):
        return [item.strip() for item in mydict[key].split(',')]
    else: return False


#CLASSES
class Location:
    def __init__(self, title,attributes):
        self.title=title
        self.desc = attributes.get("desc", False)
        self.contains=lfds(attributes,'contains')
        self.routes=lfds(attributes,'routes')

    def describe(self):
        printtext="You are in " + self.desc +"\nYou see:\n-"+ "\n-".join( self.contains)+'\n'
        print(printtext)

    def valid_route(self,route):
        return route in self.routes
    
    def show_routes(self):
        description="You can see the following routes:\n-" + "\n-".join(self.routes)+'\n'
        print(description)


class Item:
    def __init__(self, title, attributes):
        self.title=title
        '''
        #let's not use this because we have to test  hasattr every time 
         for key, value in attributes.items():
            setattr(self,key,value)
            '''
        self.description = attributes.get("description", False)
        self.container_size = attributes.get("desc", 0)
        #self.desc = attributes.get("desc", False)
        #self.desc = attributes.get("desc", False)
        #self.desc = attributes.get("desc", False)

    def describe(self):
        return self.description
        

#LOAD ITEM AND LOCATION TOMLS INTO DICTIONARIES      

with open('items.toml', 'rb') as file:
    item_data=tomllib.load(file)

with open('locations.toml', 'rb') as file:
    room_data=tomllib.load(file)

#INITIALISE CLASSES PER ITEM AND LOCATION

item_dict = {}
for key, value in item_data.items():
    item_dict[key]=Item(key,value)

location_dict = {}
for key, value in room_data.items():
    location_dict[key]=Location(key,value)



#COMMAND/ACTION FUNCTIONS

def action_look(extracted_values, current_room):
    if hasattr(item_dict[extracted_values[0]], "describe"):
        print(item_dict[extracted_values[0]].describe())
        return current_room,'success'

def action_goto(extracted_values,current_room):
    if current_room.valid_route(extracted_values[0]):
        current_room=location_dict[extracted_values[0]]
        return current_room,'roomchange'
    else:
        return current_room, 'roomerror'


#INITIALISE PARSER DICTIONARY
command_schema=[
    (['look','at',None], action_look),
    (['go','to',None], action_goto)

]

#COMMAND PARSER

def parse_command(command_list, command_schema, current_room):
    command_found=False
    extracted_values=[]
    for commands, action in command_schema:
        if len(command_list) ==len(commands):
            for word,expected in zip(command_list, commands):
                if expected==None:
                    extracted_values.append(word)
                    continue
                if isinstance(expected, str):
                    if word != expected:
                        extracted_values=[]
                        break
            else:
                #command is found
                return action(extracted_values,current_room)
                break
    #no commands are found
    else:
        print(COMMAND_FAILURES[random.randint(0,len(COMMAND_FAILURES)-1)])
        return current_room, "error"
    

#SET ENTRY POINT
current_room=location_dict['entry']

#errortext
error_text={'roomerror': 'No such location exists'}

#debug
def debug():
    pass

#GAMELOOP
cls()

debug_mode=False
if debug_mode:
    debug()
#main
print('welcome to game')
playing=True
unmoved=True
action=""
while playing:
    unmoved=True
    current_room.describe()
    current_room.show_routes()
    while unmoved:
        user_input=input('Take an action: ')
        cls()
        command_list=user_input.split(' ')
        current_room, action = parse_command(command_list, command_schema, current_room)
        if action == "roomchange": unmoved=False
        if action in error_text: print(error_text[action])




