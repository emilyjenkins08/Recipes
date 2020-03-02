from parse import extract_food_info, extract_directional_info, food, make_recipe_obj

SOUPS = ['soup', 'chili', 'stew', 'pho', 'miso', 'broth']
PASTAS = ['pasta', 'ziti', 'lasagna', 'lo mein', 'ravioli', 'fettuccine', 'penne', 'noodle',
          'macaroni', 'shells', 'spaghetti', 'tortellini', 'kugel', 'pasticcio', 'chow mein', 'chow fun']
RICE = ['fried rice', 'frutti de mar', 'jambalaya', 'gumbo']
MEATS = ['chop', 'lamb', 'mutton', 'beef', 'rump', 'steak', 'ribeye', 'fillet', 'loin',
         'brisket', 'pork', 'ribs', 'veal', 'turkey', 'wing', 'chicken', 'thigh', 'breast', 'liver',
         'bone', 'drum sticks', 'duck', 'belly', 'shoulder', 'fish', 'salmon', 'tuna', 'halibut', 'walleye crudo',
         'tilapia', 'sardine', 'mackerel', 'trout', 'cod', 'herring', 'anchovy', 'trout', 'perch', 'pollock', 'oyster',
         'mussels', 'lobster', 'carp', 'shrimp', 'snapper', 'bass', 'seafood', 'crab', 'squid', 'octopus', 'clam',
         'scallop', 'snail', 'escargot', 'prawn', 'langoustine']
MEAT_METHODS = ['skin', 'devein', 'trim', 'thaw', 'debone', 'shuck']
TOFU_METHODS = {'pan-fry':'7 minutes',
                'bake': '15 minutes'}
tofu_ingredient = food('tofu', 1, '(175 mL) packages', ['extra-firm', 'non-silken'], ['pressed','cubed'])


def remove_meat_methods(directions, recipe_meats, new_master_methods, new_directions):
    for direction in directions:
        if any([meat.name in direction.ingredient for meat in recipe_meats]):
            step_sents = direction.step.split(".")
            for method in direction.method:
                if method in MEAT_METHODS:
                    for sent in step_sents:
                        if method in sent:
                            step_sents.remove(sent)
                            new_master_methods.remove(method)
                            direction.method.remove(method)
                            for tool in direction.tool:
                                if tool in sent:
                                    direction.tool.remove(tool)
            direction_text = ".".join(step_sents)
            direction.step = direction_text
        new_directions.append(direction)
    return new_directions, new_master_methods


def remove_meat(new_ingredients, recipe_meats, new_ingredient_info, new_directions):
    new_ingredients.remove(recipe_meats[0].name)
    for ing in new_ingredient_info:
        if ing.name == recipe_meats[0].name:
            new_ingredient_info.remove(ing)
    for i, direction in enumerate(new_directions):
        if recipe_meats[0].name in direction.ingredient:
            step_sents = direction.step.split(".")
            for ind, sent in enumerate(step_sents):
                if any([meat in sent for meat in MEATS + ['meat']]):
                    if any([ingredient in sent for ingredient in new_ingredients]):
                        for word in recipe_meats[0].name.split() + ['meat']:
                            sent = sent.replace(word, "")
                        step_sents[ind] = sent
                    else:
                        step_sents.remove(sent)
                        if not any([ingredient in step_sents[ind] for ingredient in new_ingredients]):
                            step_sents.remove(step_sents[ind])
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


def replace_meat(servings, recipe_meats, new_ingredient_info, new_directions):
    new_ingredient_info.remove(recipe_meats[0])
    tofu_ingredient.quant *= servings[0]
    new_ingredient_info.append(tofu_ingredient)
    for i, direction in enumerate(new_directions):
        if recipe_meats[0].name in direction.ingredient:
            direction.ingredient.remove(recipe_meats[0].name)
            direction.ingredient.append('tofu')
            step_sents = direction.step.split(".")
            for ind, sent in enumerate(step_sents):
                if any([meat in sent for meat in MEATS + ['meat']]):
                    for word in recipe_meats[0].name.split() + ['meat']:
                        last_ind = 0
                        if word in sent:
                            last_ind = sent.index(word)
                            sent = sent.replace(word, "")
                    step_sents[ind] = sent[:last_ind] + 'tofu' + sent[last_ind:]
            direction_text = ".".join(step_sents)
            new_directions[i].step = direction_text
    return new_ingredient_info, new_directions


def clean_master_methods(new_master_methods, new_directions):
    pass


def clean_master_tools(new_master_tools, new_directions):
    pass


def vegetarian(recipe):
    full_ingredient_info, ingredients = extract_food_info(recipe.ingredients)
    new_ingredient_info = full_ingredient_info
    new_ingredients = ingredients
    directions, master_tools, master_methods = extract_directional_info(recipe.directions, ingredients)
    new_directions = []
    new_master_tools = master_tools
    new_master_methods = master_methods
    recipe_meats = []
    for ingredient in full_ingredient_info:
        if any([meat in ingredient.name for meat in MEATS]):
            recipe_meats.append(ingredient)
    if recipe_meats:
        new_directions, new_master_methods = remove_meat_methods(directions, recipe_meats, new_master_methods,
                                                                 new_directions)
        if any([meat in recipe.name for meat in MEATS]):
            new_ingredient_info, new_directions = replace_meat(recipe.servings, recipe_meats, new_ingredient_info,
                                                               new_directions)
        else:
            new_ingredient_info, new_directions = remove_meat(new_ingredients, recipe_meats, new_ingredient_info,
                                                              new_directions)
    else:
        return "already veg"
    for ing in new_ingredient_info:
        ing.print_food()
    for dir in new_directions:
        dir.print_dir()
    # return new_ingredient_info, new_directions, new_master_methods, new_master_tools
