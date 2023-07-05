import graphene
#from fastapi import FastAPI
from starlette.graphql import GraphQLApp
import mongo

#
class Person(graphene.ObjectType):
    name = graphene.String()
    age = graphene.Int()
    city = graphene.String()


#
class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="from iQL"))
    user = graphene.Int(username=graphene.Int(default_value=33, description= "the user field"))
    person = graphene.Field(Person)

    def resolve_hello(self, info, name):
        return "Hello " + name
    
    def resolve_user(self, info, username): 
        return {username}

#
class CreatePerson(graphene.Mutation): 
    class Arguments: 
        name = graphene.String()
        age = graphene.Int()
        city = graphene.String()
    #
    ok = graphene.Boolean()
    person = graphene.Field(lambda: Person)
    #
    def mutate(root, info, name, age, city):
        #
        print("mutate: ", info)
        #
        person = Person(name=name, age=age, city=city)
        #
        print("person: ", person.name, person.age, person.city)
        # insert into Mongodb
        res = mongo.collection.insert_one({"name":person.name,"age":person.age, "city": person.city})
        print("res: ", res.inserted_id, res['docs'])
        #
        ok = True 
        return CreatePerson(person=person, ok=ok)
            
    
# Mutation
class MyMutations(graphene.ObjectType): 
    create_person = CreatePerson.Field()


    
    
    

#app = FastAPI()
#app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))