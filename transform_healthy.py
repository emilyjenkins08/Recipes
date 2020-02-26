"""
- To healthy
    - Cut fats (butter, margarine, shortening, oil in 1/2), salt, sugar (1/3 or Splenda), low-fat milk and cheese, replace cream cheese w low fat cream cheese
    - Mayonnaise — natural yogurt, or vinaigrette dressing
    - For veggies, cut oil, flavor w/ herbs
    - Whole wheat pasta (whole grains)
    - Low sodium soy sauce
    - Meat
        - Replace w/ peas, beans, lentils
        - Trim fat and remove skin before cooking
        - Replace frying with bake, grill, microwave, roast, poach
    - Healthy techniques
        - Braising, broiling, grilling, poaching, sautéing, steaming
        - Basting liquid — use wine, fruit juice, veggie juice, veggie broth instead of oil or drippings
    - Grate cheese instead of slicing (use less)
    - Increase fiber
    - soups + stews
        - cool / skim off the fat on top
        - Replace fatty meats w/ peas, beans, lentils
    - Sauces and dips
        - Replace cream, whole milk, sour cream with skim milk, low-fat yogurt
"""

from main import main as get_recipe_info
from parse import wrapper
from parse import food, direction
import string
from collections import deque


# helper to lowercase and remove punctuation
def remove_punc_lower(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation))


def lookup(ing, lst):
    name_lst = remove_punc_lower(ing.name).split()
    for word in name_lst:
        if word in lst:
            return ing.name
        else:
            if word[-1] == 's' and word[:-1] in lst:
                return ing.name
    return False


# helper that goes through the step text and makes replacements for it based on the subs that is passed in
# sometimes the outputted text is missing punctutaions.
def make_substitutions(old_food, new_food, step_text):
    text_slt = step_text.split()
    old_food_slt = [remove_punc_lower(i) for i in old_food.split()]
    ind = 0
    subs = []
    rmv = []
    while ind < len(text_slt):
        wrd = text_slt[ind]
        # print("Word: ", wrd)
        wrd_mod = remove_punc_lower(wrd)
        if wrd_mod in old_food_slt:
            rmv.append(wrd)
        elif wrd_mod[-1] == 's' and wrd_mod[:-1] in old_food_slt:
            rmv.append(wrd)
        else:
            if rmv != []:
                subs.append(" ".join(rmv))
                rmv = []
        ind += 1
    subs = list(set(subs))
    subs.sort(key=lambda x: -len(x))
    for i in subs:
        if i[-1] in [';', ',', '.']:
            step_text = step_text.replace(i, new_food + i[-1])
        else:
            step_text = step_text.replace(i, new_food)
    return step_text


def main(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
    # basic lists to cycle through to make changes
    cut_half = ['butter', 'margarine', 'shortening', 'oil', 'sugar', 'chocolate']
    cut_fourth = ['salt']
    low_fat = ['milk', 'cheese', 'cream', 'yogurt']
    whole_grain = ['pasta', 'bread', 'rice']
    low_sodium = ['soy sauce']
    ok_meat = ['chicken', 'turkey', 'fish']
    bad_meat = ['sausage', 'beef', 'pork', 'venison', 'bacon', 'ham']
    # initalize substitution list for making changes in the directions in reference to foods
    subs = []
    # name of the meat to substitue is initialize as empty, list is to account for multiple meats
    meat_name_lst = []
    # boolean for if the 'trim meat fat and skin' is added to directions
    add_trim = False
    for ing in food_obj_lst:
        ###Looking if meat exists in the food and then making the appropiate subsitution to it
        other_meat = lookup(ing, ok_meat)
        if other_meat and 'broth' not in ing.name.lower():
            add_trim = True
            meat_name_lst.append(other_meat)
        replace_meat = lookup(ing, bad_meat)
        if replace_meat:
            ing.name = 'turkey'
            subs.append([replace_meat, 'turkey'])
            add_trim = True
            meat_name_lst.append(ing.name)
        # substituion for oil
        if 'oil' in ing.name.lower():
            subs.append([ing.name, 'olive oil'])
            ing.name = 'olive oil'
        ###going through the other lists and seeing if chances have to be made
        if lookup(ing, cut_half) or other_meat or replace_meat:
            ing.quant = ing.quant / 2
            continue
        if lookup(ing, cut_fourth):
            ing.quant = ing.quant / 4
            continue
        if lookup(ing, low_fat):
            ing.name = 'low fat ' + ing.name
            continue
        if lookup(ing, whole_grain):
            ing.name = 'whole grain ' + ing.name
            continue
        if lookup(ing, low_sodium):
            ing.name = 'low sodium ' + ing.name
    # code that adds a direction to trim fat and skin off of meat
    if add_trim:
        meat_len = len(meat_name_lst)
        meat_name = ''
        if meat_len == 1:
            meat_name = meat_name_lst[0]
        elif meat_len == 2:
            meat_name = " and ".join(meat_name_lst)
        else:
            meat_name = ', '.join(meat_name_lst[:-1]) + ' and ' + meat_name_lst[-1]
        direc_obj_q = deque(direc_obj_lst)
        trim_fat = direction('Prep the ' + meat_name + ' by trimming the fat and removing the skin.', meat_name_lst, [],
                             [], [])
        direc_obj_q.appendleft(trim_fat)
        direc_obj_lst = list(direc_obj_q)

    # making food substitutions to the directions list
    # print(subs)
    for direc in direc_obj_lst:
        for sub in subs:
            direc.step = make_substitutions(sub[0], sub[1], direc.step)
            if sub[0] in direc.ingredient:
                direc.ingredient[direc.ingredient.index(sub[0])] = sub[1]
    for ing in food_obj_lst:
        ing.print_food()
    for step in direc_obj_lst:
        step.print_dir()
    return


if __name__ == '__main__':
    url = 'https://www.allrecipes.com/recipe/14054/lasagna/'
    recipe = get_recipe_info(url)
    food_lst, food_name_lst, direc_lst, tools_lst, methods_lst = wrapper(recipe.ingredients, recipe.directions)
    main(recipe, food_lst, food_name_lst, direc_lst, tools_lst, methods_lst)
