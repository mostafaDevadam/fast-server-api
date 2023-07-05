#
class Person: 
    def __init__(self, name): 
        self.name = name
        
#
def get_person_name(one_person):
    return one_person 

name = "adam"
result = get_person_name(name)
print( result )  