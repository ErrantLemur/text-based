import tomllib  
import random
COMMAND_FAILURES=[
    "That's ridiculous...",
    "What? Why?",
    "Error, brain not found",
    "Over my dead body",
    "That's it, you're cut off"
]

#CLASSES
class Location:
    def __init__(self, title,attributes):
        self.title=title
        self.desc = attributes.get("desc", False)
        if attributes.get('contains',False):
            self.contains=[item.strip() for item in attributes['contains'].split(',')]
        else: self.contains=False

    def describe(self):
        description="You are in " + self.desc +".\nYou see:\n"+ "\n".join(self.contains)+'\n'
        print(description)


class Item:
    def __init__(self, title, attributes):
        self.title=title
        '''
        #let's not use this because we have to test  hasattr every time 
         for key, value in attributes.items():
            setattr(self,key,value)
            '''
        self.desc = attributes.get("desc", False)
        self.container_size = attributes.get("desc", 0)
        #self.desc = attributes.get("desc", False)
        #self.desc = attributes.get("desc", False)
        #self.desc = attributes.get("desc", False)
        

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



#COMMAND FUNCTIONS

def action_look(extracted_values):
    print(f'you did it, you {extracted_values}!')



#INITIALISE PARSER DICTIONARY
command_schema=[
    (['look','at',None], action_look)

]

#COMMAND PARSER

def parse_command(command_list, command_schema):
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
                action(extracted_values)
                break
    #no commands are found
    else: print(COMMAND_FAILURES[random.randint(0,len(COMMAND_FAILURES)-1)])
    
    

#SET ENTRY POINT
current_room=location_dict['entry']

#MAIN LOOP
playing=True
while playing:
    current_room.describe()
    user_input=input('Take an action: ')
    command_list=user_input.split(' ')
    print(command_list)
    parse_command(command_list, command_schema)



