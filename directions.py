import requests
from lxml import html
from bs4 import BeautifulSoup

steps = ["Preheat oven to 350 degrees F (175 degrees C.) In a large bowl, combine flour sugar, salt and baking powder. Cut in shortening until mixture resembles coarse crumbs. Mix egg yolk and water together and mix into flour until it forms a ball. Roll out to fit the bottom of a 10x15 inch pan. Watch Now",
    "In a large bowl, combine apples, lemon juice, 2 tablespoons flour, sugar and cinnamon. Pour filling into pie crust and dot with 2 tablespoons butter. Watch Now",
    "In a medium bowl, combine 1 cup flour, 1 teaspoon cinnamon, 2/3 cup brown sugar and 2/3 cup butter. Cut in the butter until crumbly, then sprinkle over apples. Watch Now",
    "Bake in the preheated oven for 60 minutes, or until topping is golden brown. Watch Now"]

class direction:
    def __init__(self, step, ingredient, method, tool, time):
        self.step = step
        self.ingredient = ingredient
        self.method = method
        self.tool = tool
        self.time = time
    def print_dir(self):
        print("step: ", self.step)
        if self.ingredient:
            print("Ingredients involved: ", self.ingredient)
        if self.method:
            print("methods used: ", self.method)
        if self.tool:
            print("tools used: ", self.tool)
        if self.time:
            print("time included in step: ", self.time)
        print('\n\n')



def extract_directional_info(steps):

    tools = ["pot", "pan", "oven", "oven rack", "broiler", "skillet", "saute pan", "bowl", "plate",
            "tongs", "fork", "whisk", "microwave"]

    times = ["minutes", "hour", "seconds"]

    methods = ["saute", "broil", "boil", "poach", "cook", "whisk", "bake", "stir", "mix", "preheat",
            "set", "heat", "add", "remove", "place", "grate", "shake", "stir", "crush", "squeeze",
            "beat", "toss", "top", "sprinkle", "chop", "dice", "mince", "cut", "drain", "coat",
            "serve", "combine", "marinate", "transfer", "layer", "microwave", "spoon"]


    step_info = {}
    direc_lst = []
    for step in steps:
        tools_needed = []
        methods_used = []
        times_included = []
        step = step.lower().replace(",", "")
        step = step.lower().replace(".", "")
        step = step.lower().replace(";", "")
        for tool in tools:
            if tool in step.lower() and tool not in tools_needed:
                tools_needed.append(tool)
        for method in methods:
            if method in step.lower() and method not in methods_used:
                methods_used.append(method)
        for time in times:
            if time in step.lower() and time not in times_included:
                index_num = step.split().index(time) - 1
                times_included.append(step.split()[index_num] + " " + time)
        direc_lst.append(direction(step.replace("Watch Now", ""), [], methods_used, tools_needed, times_included))
    for i in direc_lst:
        i.print_dir()

    #print("tools needed are ", tools_needed)
    #print("methods used are ", methods_used)

    # parsing for  ingredients, tools, methods, and times

extract_directional_info(steps)
