from parse import extract_food_info, extract_directional_info, food
from transform_healthy import make_substitutions


SOUPS = ['soup', 'chili', 'stew', 'pho', 'miso', 'broth']
PASTAS = ['pasta', 'ziti', 'lasagna', 'lo mein', 'ravioli', 'fettuccine', 'penne', 'noodle',
          'macaroni', 'shells', 'spaghetti', 'tortellini', 'kugel', 'pasticcio', 'chow mein', 'chow fun']
RICE = ['fried rice', 'frutti de mar', 'jambalaya', 'gumbo']
MEATS = ['pork chop', 'lamb chop', 'lamb', 'mutton', 'beef', 'rump', 'steak', 'ribeye', 'fillet', 'loin',
         'brisket', 'pork', 'ribs', 'veal', 'turkey', 'wing', 'chicken', 'thigh', 'breast', 'liver',
         'bone', 'drum sticks', 'duck', 'belly', 'shoulder', 'fish', 'salmon', 'tuna', 'halibut', 'walleye crudo',
         'tilapia', 'sardine', 'mackerel', 'trout', 'cod', 'herring', 'anchovy', 'trout', 'perch', 'pollock', 'oyster',
         'mussels', 'lobster', 'carp', 'shrimp', 'snapper', 'bass', 'seafood', 'crab', 'squid', 'octopus', 'clam',
         'scallop', 'snail', 'escargot', 'prawn', 'langoustine', 'ham', 'bacon', 'pancetta', 'prosciutto', 'sausage']
BROTHS = ['chicken broth', 'chicken stock', 'beef broth', 'beef stock']
MEAT_METHODS = ['skin', 'devein', 'trim', 'thaw', 'debone', 'shuck']
tofu_ingredient = food('tofu', 175, 'mL', ['extra-firm', 'non-silken'], ['pressed', 'cubed'])
mushroom_ingredient = food('baby bella mushrooms', 1, 'cup', [], ['diced'])


def meat_cooking(step, methods, times, ingredients):
    for method in methods:
        if method in step:
            if not any([ing.name in step for ing in ingredients]):
                if method == "cook":
                    if "oven" in step:
                        for time in times:
                            if time in step:
                                times.remove(time)
                                times.append('15 minutes')
                                break
                        step = "Bake mushrooms for 15 minutes"
                    elif "grill" in step:
                        for time in times:
                            if time in step:
                                times.remove(time)
                                times.append('10 minutes')
                                break
                        step = "Grill mushrooms for 10 minutes"
                    else:
                        for time in times:
                            if time in step:
                                times.remove(time)
                                times.append('4 minutes')
                                break
                        step = "Cook mushrooms for 4 minutes on each side"
                elif method == "bake" or "oven" in step:
                    for time in times:
                        if time in step:
                            times.remove(time)
                            times.append('15 minutes')
                            break
                    step = "Bake mushrooms for 15 minutes"
                elif method == "grill":
                    for time in times:
                        if time in step:
                            times.remove(time)
                            times.append('10 minutes')
                            break
                    step = "Grill mushrooms for 10 minutes"
        else:
            step = step.replace("until pink", "")
            step = step.replace(", until no longer pink, ", "")
    return step


def replace_meat(servings,  meat_ing,  new_ingredient_info, new_directions, sub):
    new_ingredient_info.remove(meat_ing)
    sub.quant *= servings
    new_ingredient_info.append(sub)
    for i, direction in enumerate(new_directions):
        if meat_ing.name in direction.ingredient:
            direction.ingredient.remove(meat_ing.name)
            direction.ingredient.append(sub.name)
            step_sents = direction.step.split(".")
            for ind, sent in enumerate(step_sents):
                for char in [',', ';', ':']:
                    sent = sent.replace(char, "")
                if any([meat in sent for meat in MEATS + ['meat']]):
                    sent = meat_cooking(sent, direction.method, direction.time, new_ingredient_info)
                    last_ind = 0
                    sent = sent.split()
                    desc = meat_ing.desc
                    if type(meat_ing.desc) == str:
                        desc = [desc, 'meat']
                    elif desc:
                        desc = desc.append('meat')
                    else:
                        desc = ['meat']
                    for meat in meat_ing.name.split() + desc:
                        for word in sent:
                            if meat in word:
                                last_ind = sent.index(word)
                                sent.remove(word)
                    sent.insert(last_ind, sub.name)
                    sent = " ".join(sent)
                    step_sents[ind] = sent
            direction_text = ".".join(step_sents)
            new_directions[i].step = direction_text
    return new_ingredient_info, new_directions


def to_vegetarian(recipe):
    full_ingredient_info, ingredients = extract_food_info(recipe.ingredients)
    new_ingredient_info = full_ingredient_info
    new_ingredients = ingredients
    directions, master_tools, master_methods = extract_directional_info(recipe.directions, ingredients)
    new_directions = []
    new_master_tools = master_tools
    new_master_methods = master_methods
    recipe_meats = []
    for ingredient in full_ingredient_info:
        if any([ingredient.name == broth for broth in BROTHS]):
            new_broth_name = "vegetable broth"
            new_broth_quant = ingredient.quant
            new_broth_meas = ingredient.meas
            new_broth = food(new_broth_name, new_broth_quant, new_broth_meas, [], [])
            full_ingredient_info.remove(ingredient)
            full_ingredient_info.append(new_broth)
            for dir in directions:
                if ingredient.name in dir.ingredient:
                    dir.step = make_substitutions(ingredient.name, new_broth_name, dir.step)
                    dir.ingredient.remove(ingredient.name)
                    dir.ingredient.append(new_broth_name)
                new_directions.append(dir)
    for ingredient in full_ingredient_info:
        if any([meat in ingredient.name for meat in MEATS]):
            recipe_meats.append(ingredient)
    if recipe_meats:
        if any([meat in recipe.name for meat in MEATS]):
            new_ingredient_info, new_directions = replace_meat(recipe.servings, recipe_meats[0],
                                                               new_ingredient_info,
                                                               new_directions, tofu_ingredient)
        else:
            new_ingredient_info, new_directions = replace_meat(recipe.servings, recipe_meats[0],
                                                               new_ingredient_info,
                                                               new_directions, mushroom_ingredient)
    if len(recipe_meats) > 1:
        for meat in recipe_meats[1:]:
            new_ingredient_info, new_directions = remove_meat(meat, new_ingredient_info, new_directions)
    else:
        return "already veg"
    return new_ingredient_info, new_directions
    # return new_ingredient_info, new_directions, new_master_methods, new_master_tools


def remove_meat(meat, new_ingredient_info, new_directions):
    new_ingredient_info.remove(meat)
    for ing in new_ingredient_info:
        if ing.name == meat.name:
            new_ingredient_info.remove(ing)
    for i, direction in enumerate(new_directions):
        if meat.name in direction.ingredient:
            step_sents = direction.step.split(".")
            for ind, sent in enumerate(step_sents):
                if meat.name in sent:
                    if any([ingredient.name in sent for ingredient in new_ingredient_info]):
                        for word in meat.name.split():
                            sent = sent.replace(word, "")
                        step_sents[ind] = sent
                    else:
                        print(sent)
                        step_sents.remove(sent)
                        for tool in direction.tool:
                            if tool in sent:
                                if tool in step_sents[ind]:
                                    step_sents[ind] = step_sents[ind].replace("another", "a")
                                elif not any([tool in s for s in step_sents[ind:]]):
                                    direction.tool.remove(tool)
                        for method in direction.method:
                            if method in sent and not any([method in s for s in step_sents[ind:]]):
                                direction.method.remove(method)
            direction_text = ".".join(step_sents)
            new_directions[i].step = direction_text
            new_directions[i].tool = direction.tool
            new_directions[i].method = direction.method
    return new_ingredient_info, new_directions

#
# def remove_meat_methods(directions, recipe_meats, new_master_methods, new_directions):
#     for direction in directions:
#         if any([meat.name in direction.ingredient for meat in recipe_meats]):
#             step_sents = direction.step.split(".")
#             for method in direction.method:
#                 if method in MEAT_METHODS:
#                     for sent in step_sents:
#                         if method in sent:
#                             step_sents.remove(sent)
#                             new_master_methods.remove(method)
#                             direction.method.remove(method)
#                             for tool in direction.tool:
#                                 if tool in sent:
#                                     direction.tool.remove(tool)
#             direction_text = ".".join(step_sents)
#             direction.step = direction_text
#         new_directions.append(direction)
#     return new_directions, new_master_methods


def from_vegetarian():
    pass