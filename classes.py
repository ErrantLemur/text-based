from funcs import lfds

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
        self.description = attributes.get("description", False)
        self.container_size = attributes.get("container_size", 0)

    def describe(self):
        return self.description
    
#class gamestate