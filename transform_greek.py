# transform from recipe to greek

from parse import wrapper, remove_punc_lower, food, direction, make_recipe_obj
import string
from collections import deque
from get_key_ingredient import get_key, get_key_food

def lookup(ing, lst):
    name_lst = ing.name.lower().translate(str.maketrans('', '', string.punctuation)).split()
    for word in name_lst:
        if word in lst:
            return ing.name
        else:
            if word[-1] == 's' and word[:-1] in lst:
                return ing.name
    return False


def transform_soup_greek(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
    meat = ['chicken','turkey','fish','sausage','beef','pork','venison','bacon','ham']
    vegetable = ['asparagus','cucumber','celery','cabbage','spinach','lettuce','turnip','carrot','garlic','onion','parsnip','kale','brussels','tomato','okra','broccoli','radish','collard','artichoke','cauliflower','ginger','watercress','pumpkin','arugula','tomatillo','pepper','turnip','chard','horseradish','radish','fennel','pea','zucchini','rutabaga','eggplant','mushroom','squash']

    meat_lst = []
    veggie_lst = []
    meat_obj_lst = []
    veggie_obj_lst = []

    new_food_lst = []
    new_food_name_lst = []
    new_direc_obj_lst = []

    for ing in food_obj_lst:
        meat_present = lookup(ing,meat)
        veggie_present = lookup(ing,vegetable)
        if meat_present:
            meat_lst.append(meat_present)
            meat_obj_lst.append(ing)
        if veggie_present:
            veggie_lst.append(veggie_present)
            veggie_obj_lst.append(ing)

    # makes 8 servings
    new_food_lst.append(food("tomatoes", 29,"ounces","","diced"))
    new_food_name_lst.append("tomatoes")

    new_food_lst.append(food("great Northern beans", 28,"ounces","","undrained"))
    new_food_name_lst.append("great Northern beans")

    new_food_lst.append(food("spinach", 14,"ounces","","chopped drained"))
    new_food_name_lst.append("spinach")
    new_food_lst.append(food("chicken broth", 29,"ounces","",""))
    new_food_name_lst.append("chicken broth")

    new_food_lst.append(food("tomato sauce", 8,"ounces","",""))
    new_food_name_lst.append("tomato sauce")

    new_food_lst.append(food("water", 3,"cups","",""))
    new_food_name_lst.append("water")

    new_food_lst.append(food("garlic", 1,"tablespoon","","minced"))
    new_food_name_lst.append("garlic")

    new_food_lst.append(food("bacon", 8,"slices","crisp","cooked crumbled"))
    new_food_name_lst.append("bacon")

    new_food_lst.append(food("parsley", 1,"tablespoon","dried",""))
    new_food_name_lst.append("parsley")

    new_food_lst.append(food("garlic powder", 1,"teaspoon","",""))
    new_food_name_lst.append("garlic powder")

    new_food_lst.append(food("salt",1.5,"teaspoons","",""))
    new_food_name_lst.append("salt")

    new_food_lst.append(food("black pepper", 0.5,"teaspoon","","ground"))
    new_food_name_lst.append("black pepper")

    new_food_lst.append(food("basil", 0.5,"teaspoon","dried",""))
    new_food_name_lst.append("basil")

    new_food_lst.append(food("seashell pasta", 0.5,"pound","",""))
    new_food_name_lst.append("seashell pasta")

    meat_str = ""
    step1 = ""
    ing_lst = []
    items_added = []
    countt = 0

    if meat_obj_lst:
        new_food_lst.append(food("vegetable oil", 1,"tablespoon","",""))
        new_food_name_lst.append("vegetable oil")
        ing_lst.append("vegetable oil")
        items_added.append("vegetable oil")
    for ing in meat_obj_lst:
        if countt == len(meat_obj_lst) - 1:
            meat_str = meat_str + "and " + ing.name + " "
        else:
            if len(meat_obj_lst) == 2:
                meat_str = meat_str + ing.name + " "
                countt += 1
            else:
                meat_str = meat_str + ing.name + ", "
                countt += 1
        ing_lst.append(ing.name)
        new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 6,ing.meas,ing.desc,ing.prep))
        new_food_name_lst.append(ing.name)
        items_added.append(ing.name)

    if meat_str:
        step1 = "In a large stock pot, heat vegetable oil on low heat; cook " + meat_str + "until meat is cooked and no longer pink. Remove the meat, dice and return to stock pot."
        new_direc_obj_lst.append(direction(step1,ing_lst,['heat','cook','remove','dice'],['large stock pot'],[]))


    ing_lst_step2 = ['tomatoes','great Northern beans','chicken broth','tomato sauce','water','garlic','bacon','parsley','garlic powder','salt','pepper','basil']
    stepp2 = "In the stock pot, combine diced tomatoes, "
    for veg in veggie_obj_lst:
        stepp2 = stepp2 + veg.name + ", "
        ing_lst_step2.append(veg.name)
        new_food_lst.append(food(veg.name,veg.quant/recipe_obj.servings * 8,veg.meas,veg.desc,veg.prep))
        new_food_name_lst.append(veg.name)
        items_added.append(veg.name)

    stepp2pt2 = "beans, spinach, chicken broth, tomato sauce, water, garlic, bacon, parsley, garlic powder, salt, pepper, and basil. Bring to a boil, and let simmer for 40 minutes, covered."
    new_direc_obj_lst.append(direction(stepp2+stepp2pt2,ing_lst_step2,['combine','simmer','boil'],[],['40 minutes']))

    step3 = "Add pasta and cook uncovered until pasta is tender, approximately 10 minutes. Ladle soup into individual serving bowls, sprinkle cheese on top, and serve."
    new_direc_obj_lst.append(direction(step3,['pasta','cheese'],['add','cook','sprinkle','serve'],['serving bowls'],[]))

    food_obj_lst = new_food_lst
    food_name_lst = new_food_name_lst
    direc_obj_lst = new_direc_obj_lst

    strr = ''
    count = 0
    for item in items_added:
        if count == len(items_added) - 1:
            strr = strr + "and " + item
        else:
            if len(items_added) == 2:
                strr = strr + item + " "
                count += 1
            else:
                strr += item + ", "
                count += 1

    print("===============")
    print("== CHANGELOG ==")
    print("Based on the requirements, I've made the following updates to the recipe:")
    print("- Used key ingredients from the original recipe to make Greek Pasta Fagoli Soup!")
    if strr:
        print("- Key ingredients added from original recipe: ", strr)
    print("===============\n")

    recipe_obj.servings = 8
    recipe_obj.cuisine = "Greek"
    recipe_obj.name += " transformed into Greek"

    return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)

def transform_dessert_greek(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
    new_food_lst = []
    new_food_name_lst = []
    new_direc_obj_lst = []

    #makes 15 servings
    new_food_lst.append(food("milk", 6,"cups","whole",""))
    new_food_name_lst.append("milk")

    new_food_lst.append(food("semolina flour", 1,"cup","",""))
    new_food_name_lst.append("semolina flour")

    new_food_lst.append(food("cornstarch", 3.5,"tablespoons","",""))
    new_food_name_lst.append("cornstarch")

    new_food_lst.append(food("white sugar", 2.5,"cups","",""))
    new_food_name_lst.append("white sugar")

    new_food_lst.append(food("salt", 0.25,"teaspoon","",""))
    new_food_name_lst.append("salt")

    new_food_lst.append(food("eggs", 6,"","",""))
    new_food_name_lst.append("eggs")

    new_food_lst.append(food("vanilla extract", 1,"teaspoon","",""))
    new_food_name_lst.append("vanilla extract")

    new_food_lst.append(food("butter", 0.75,"cup","","melted"))
    new_food_name_lst.append("butter")

    new_food_lst.append(food("phyllo dough", 12,"sheets","",""))
    new_food_name_lst.append("phyllo dough")

    new_food_lst.append(food("water", 1,"cup","",""))
    new_food_name_lst.append("water")

    step11 = "Pour milk into a large saucepan, and bring to a boil over medium heat. In a medium bowl, whisk together the semolina, cornstarch, 1 cup sugar and salt so there are no cornstarch clumps. When milk comes to a boil, gradually add the semolina mixture, stirring constantly with a wooden spoon. Cook, stirring constantly until the mixture thickens and comes to a full boil. Remove from heat, and set aside. Keep warm."
    ii = ['milk','semolina','cornstarch','sugar','salt']
    new_direc_obj_lst.append(direction(step11,ii,['pour','boil','whisk','add','stir','cook','remove'],['saucepan','bowl','wooden spoon'],[]))


    items_added = []
    dessert_step = "In a large bowl, beat eggs with an electric mixer at high speed. Add 1/2 cup of sugar, and whip until thick and pale, about 10 minutes. Stir in "
    ingreed = ['eggs','sugar','vanilla extract']
    key_ingrr = get_key_food(recipe_obj)
    if key_ingrr:
        for food1 in key_ingrr:
            dessert_step = dessert_step + food1.name + ", "
            new_food_lst.append(food(food1.name,(food1.quant / recipe_obj.servings * 4),food1.meas,food1.desc,food1.prep))
            new_food_name_lst.append(food1.name)
            ingreed.append(food1.name)
            items_added.append(food1.name)
        dessert_step += "and"
    dessert_step2 = " vanilla."
    new_direc_obj_lst.append(direction(dessert_step+dessert_step2,ingreed,['beat','add','whip','stir'],['bowl','electric mixer'],['10 minutes']))

    step33 = "Fold the whipped eggs into the hot semolina mixture. Partially cover the pan, and set aside to cool."
    new_direc_obj_lst.append(direction(step33,['eggs','semolina'],['cover','set','cool'],['pan'],[]))

    step44 = "Preheat the oven to 350 degrees F (175 degrees C). Butter a 9x13 inch baking dish, and layer 7 sheets of phyllo into the pan, brushing each one with butter as you lay it in. Pour the custard into the pan over the phyllo, and cover with the remaining 5 sheets of phyllo, brushing each sheet with butter as you lay it down."
    new_direc_obj_lst.append(direction(step44,['phyllo dough','butter','custard'],['preheat','butter','layer','brush','pour','cover'],['oven','baking dish'],[]))

    step55 = "Bake for 40 to 45 minutes in the preheated oven, until the top crust is crisp and the custard filling has set. In a small saucepan, stir together the remaining cup of sugar and water. Bring to a boil. When the Galaktoboureko comes out of the oven, spoon the hot sugar syrup over the top, particularly the edges. Cool completely before cutting and serving. Store in the refrigerator."
    new_direc_obj_lst.append(direction(step55,['sugar','water'],['bake','stir','boil','spoon','cool','store'],['oven','saucepan'],[]))


    food_obj_lst = new_food_lst
    food_name_lst = new_food_name_lst
    direc_obj_lst = new_direc_obj_lst


    strr = ''
    count = 0
    for item in items_added:
        if count == len(items_added) - 1:
            strr = strr + "and " + item
        else:
            if len(items_added) == 2:
                strr = strr + item + " "
                count += 1
            else:
                strr += item + ", "
                count += 1

    print("===============")
    print("== CHANGELOG ==")
    print("Based on the requirements, I've made the following updates to the recipe:")
    print("- Used key ingredients from the original recipe to make Greek Galaktoboureko.")
    if strr:
        print("- Key ingredients added from original recipe: ", strr)
    print("===============\n")

    recipe_obj.servings = 15
    recipe_obj.cuisine = "Greek"
    recipe_obj.name += " transformed into Greek"

    return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)


def transform_cuisine_main_greek(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
    if recipe_obj.cuisine == "greek" or recipe_obj.cuisine == "Greek":
        print("recipe is already indian!")
        return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)
    # take care of soups
    soups = ["soup", "bisque", "stew", "gumbo"]
    if lookup(recipe_obj,soups):
        return transform_soup_greek(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst)

    # take care of desserts
    desserts = ['cookie', 'brownie','pie','cake','cupcake','ice cream','popsicle','donut','pastry','croissant','churro','chocolate','caramel','butterscotch','dessert','candy','m&m','meringue','bread','loaf','muffin','strudel','babka','gelato','sorbet','cracker','apple crisp','biscuit','cannoli','doughnut','eclair','flan','waffle','biscotti','pudding','pancake','cheesecake','frosting','mousse','roll','custard','crepe','frozen yogurt','fudge','froyo','gingersnap','gelatin','gingerbread','sundae','icing','jam','jellyroll','jelly','marshmallow','milkshake','macaroon','macaron','nougat','parfait','brittle','praline',"s'mores",'snickerdoodle','shortbread','scone','sugar','sweets','torte','tart','toffee','trifle','turnover']

    if lookup(recipe_obj,desserts) or "ice cream" in remove_punc_lower(recipe_obj.name):
        return transform_dessert_greek(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst)


    #basic lists to cycle through to make changes
    meat = ['chicken','turkey','fish','sausage','beef','pork','venison','bacon','ham']
    vegetable = ['asparagus','cucumber','celery','cabbage','spinach','lettuce','turnip','carrot','garlic','onion','parsnip','kale','brussels','tomato','okra','broccoli','radish','collard','artichoke','cauliflower','ginger','watercress','pumpkin','arugula','tomatillo','pepper','turnip','chard','horseradish','radish','fennel','pea','zucchini','rutabaga','eggplant','mushroom','squash']

    #initalize substitution list for making changes in the directions in reference to foods
    subs = []

    meat_lst = []
    veggie_lst = []
    meat_obj_lst = []
    veggie_obj_lst = []


    for ing in food_obj_lst:
        meat_present = lookup(ing,meat)
        veggie_present = lookup(ing,vegetable)
        if meat_present:
            meat_lst.append(meat_present)
            meat_obj_lst.append(ing)
        if veggie_present:
            veggie_lst.append(veggie_present)
            veggie_obj_lst.append(ing)

    new_food_lst = []
    new_food_name_lst = []
    new_direc_obj_lst = []
    items_added = []

    # makes 6 servings
    new_food_lst.append(food("olive oil", 3,"tablespoons","",""))
    new_food_name_lst.append("olive oil")

    new_food_lst.append(food("pita bread", 6,"6-inch","whole wheat",""))
    new_food_name_lst.append("pita bread")

    new_food_lst.append(food("tomato pesto", 6,"ounces","sun-dried",""))
    new_food_name_lst.append("tomato pesto")

    new_food_lst.append(food("tomatoes", 2,"plum","","chopped"))
    new_food_name_lst.append("tomatoes")

    new_food_lst.append(food("spinach", 1,"bunch","","rinsed chopped"))
    new_food_name_lst.append("spinach")

    new_food_lst.append(food("mushrooms", 4,"","fresh","sliced"))
    new_food_name_lst.append("mushrooms")

    new_food_lst.append(food("feta cheese", 0.5,"cup","crumbled",""))
    new_food_name_lst.append("feta cheese")

    new_food_lst.append(food("Parmesan cheese", 2,"tablespoons","","grated"))
    new_food_name_lst.append("Parmesan cheese")

    new_food_lst.append(food("black pepper", 1,"teaspoon","",""))
    new_food_name_lst.append("black pepper")

    steeep1 = "Preheat oven to 350 degrees F (175 degrees C)."
    new_direc_obj_lst.append(direction(steeep1,[],['oven'],[],[]))

    meat_str = ""
    ing_lst = ['black pepper','olive oil']
    met_lst = []
    iing = ['tomato pesto','tomatoes','spinach','mushrooms','feta cheese','Parmesan cheese']

    if meat_obj_lst:
        if len(meat_lst) > 2:
            count1 = 0
            for ing in meat_obj_lst:
                if count1 == len(meat_lst) - 1:
                    meat_str = meat_str + "and " + ing.name
                    ing_lst.append(ing.name)
                    new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 6,ing.meas,ing.desc,ing.prep))
                    new_food_name_lst.append(ing.name)
                    iing.append(ing.name)
                    items_added.append(ing.name)
                else:
                    meat_str = meat_str + ing.name + ", "
                    count1 += 1
                    ing_lst.append(ing.name)
                    new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 6,ing.meas,ing.desc,ing.prep))
                    new_food_name_lst.append(ing.name)
                    iing.append(ing.name)
                    items_added.append(ing.name)
        elif len(meat_lst) == 2:
            count = 0
            for ing in meat_obj_lst:
                if count == len(meat_lst) - 1:
                    meat_str = meat_str + "and " + ing.name
                    ing_lst.append(ing.name)
                    new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 6,ing.meas,ing.desc,ing.prep))
                    new_food_name_lst.append(ing.name)
                    iing.append(ing.name)
                    items_added.append(ing.name)
                else:
                    meat_str = meat_str + ing.name + " "
                    count += 1
                    ing_lst.append(ing.name)
                    new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 6,ing.meas,ing.desc,ing.prep))
                    new_food_name_lst.append(ing.name)
                    iing.append(ing.name)
                    items_added.append(ing.name)
        else:
            for ing in meat_obj_lst:
                meat_str = meat_str + ing.name
                ing_lst.append(ing.name)
                new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 6,ing.meas,ing.desc,ing.prep))
                new_food_name_lst.append(ing.name)
                iing.append(ing.name)
                items_added.append(ing.name)

        sttr = "Season " + meat_str + "with pepper to taste. Heat oil in a large skillet over medium high heat, then saute " + meat_str + " until browned. Remove " + meat_str + " from skillet and set aside."
        met_lst = ['season','heat','saute','remove','set']
    else:
        sttr = "Heat oil in a large skillet with salt and pepper over medium high heat."
        met_lst = ['heat']

    #step 2
    new_direc_obj_lst.append(direction(sttr,ing_lst,met_lst,['skillet'],[]))

    #step 3
    step2 = "Spread tomato pesto onto one side of each pita bread and place them pesto-side up on a baking sheet. Top pitas with tomatoes, spinach, mushrooms, "
    for veg in veggie_obj_lst:
        if veg.name not in new_food_name_lst:
            new_food_lst.append(food(veg.name,veg.quant/recipe_obj.servings * 6,veg.meas,veg.desc,veg.prep))
            new_food_name_lst.append(veg.name)
            iing.append(veg.name)
            items_added.append(veg.name)
            step2 += veg.name + ", "
    if meat_str:
        step2 += meat_str
    step2pt2 = "feta cheese, and Parmesan cheese; drizzle with olive oil and season with pepper."
    new_direc_obj_lst.append(direction(step2+step2pt2,iing,['spread','top','drizzle','season'],['baking sheet'],[]))

    #step 3
    step333 = "Bake in the preheated oven until pita breads are crisp, about 12 minutes. Cut pitas into quarters."
    new_direc_obj_lst.append(direction(step333,['pita breads'],['bake','cut'],['oven'],['12 minutes']))


    food_obj_lst = new_food_lst
    food_name_lst = new_food_name_lst
    direc_obj_lst = new_direc_obj_lst

    strr = ''
    count = 0
    for item in items_added:
        if count == len(items_added) - 1:
            strr = strr + "and " + item
        else:
            if len(items_added) == 2:
                strr = strr + item + " "
                count += 1
            else:
                strr += item + ", "
                count += 1

    print("===============")
    print("== CHANGELOG ==")
    print("Based on the requirements, I've made the following updates to the recipe:")
    print("- Used key ingredients from the original recipe to make Greek Spinach and Feta Pita Breads.")
    if strr:
        print("- Key ingredients added from original recipe: ", strr)
    print("===============\n")

    recipe_obj.servings = 6
    recipe_obj.cuisine = "Greek"
    recipe_obj.name += " transformed into Greek"


    return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)

def transform_cuisine_greek(recipe_obj):
    food_lst, food_name_lst, direc_lst, tools_lst, methods_lst = wrapper(recipe_obj.ingredients, recipe_obj.directions)
    return transform_cuisine_main_greek(recipe_obj, food_lst, food_name_lst, direc_lst, tools_lst, methods_lst)
