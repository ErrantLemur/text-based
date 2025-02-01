import tomllib  
import random
import rich
from funcs import cls, lfds, randgeneralerror
from valuefile import SPECIFIC_ERRORS
from classes import Location, Item

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

    else:
        print(f'{extracted_values[0]} has no description')
        return current_room,'generalerror'

def action_goto(extracted_values,current_room):
    if current_room.valid_route(extracted_values[0]):
        current_room=location_dict[extracted_values[0]]
        return current_room,'roomchange'
    else:
        return current_room, 'locationerror'
    
    

#INITIALISE PARSER DICTIONARY
COMMAND_SCHEMA=[
    (['look','at','!item'], action_look),
    (['go','to','!location'], action_goto)
]
#COMMAND PARSER

def parse_command(command_list, COMMAND_SCHEMA, current_room):
    outcome=''
    command_found=False
    extracted_values=[]
    for commands, action in COMMAND_SCHEMA:
        if len(command_list) ==len(commands):
            for word,expected in zip(command_list, commands):
                if expected==None:
                    extracted_values.append(word)
                    continue
                if expected[0]=='!':
                    if expected=='!location':
                        if word in location_dict:
                            extracted_values.append(word)
                            print(f'{word} is a location')
                            continue
                        else:
                            outcome='locationerror'
                            extracted_values=[]
                            break
                    elif expected=='!item':
                        if word in item_dict:
                            extracted_values.append(word)
                            print(f'{word} is an item')
                            continue
                        else:
                            outcome='itemerror'
                            extracted_values=[]
                            break

                if isinstance(expected, str):
                    if word != expected:
                        extracted_values=[]
                        break
            else:
                #command is found
                current_room, outcome = action(extracted_values,current_room)
                break
    #no commands are found
    else:
        if outcome=='':
            outcome ='error'

    return current_room, outcome
    

#SET ENTRY POINT
current_room=location_dict['entry']

#debug
def debug():
    pass

#GAMELOOP
cls()


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
        current_room, action = parse_command(command_list, COMMAND_SCHEMA, current_room)
        if action == "roomchange": unmoved=False
        if action in SPECIFIC_ERRORS:
            if callable(SPECIFIC_ERRORS[action]):
                SPECIFIC_ERRORS[action]()
            else:
                print(SPECIFIC_ERRORS[action])




#test