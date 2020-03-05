from parse import extract_food_info, extract_directional_info, food, direction, make_recipe_obj
from transform_healthy import make_substitutions

SOUPS = ['soup', 'chili', 'stew', 'pho', 'miso', 'gazpacho', 'bisque', 'chowder']
PASTAS = ['pasta', 'ziti', 'lo mein', 'ravioli', 'fettuccine', 'penne', 'noodle', 'pad thai',
          'macaroni', 'shells', 'spaghetti', 'tortellini', 'chow mein', 'chow fun', 'scampi']
CASSEROLES = ['lasagna', 'pastitsio']
RICE = ['fried rice', 'frutti de mar', 'jambalaya', 'gumbo', 'stir fry']
SANDWICH = ['sandwich', 'panini', 'torta']
TACOS = ['taco', 'gordita', ]
MEATS = ['pork chop', 'lamb chop', 'lamb', 'mutton', 'beef', 'rump', 'steak', 'ribeye', 'fillet', 'loin',
         'brisket', 'pork', 'ribs', 'veal', 'turkey', 'wing', 'chicken', 'thigh', 'breast', 'liver',
         'bone', 'drum sticks', 'duck', 'belly', 'shoulder', 'fish', 'salmon', 'tuna', 'halibut', 'walleye crudo',
         'tilapia', 'sardine', 'mackerel', 'trout', 'cod', 'herring', 'anchovy', 'trout', 'perch', 'pollock', 'oyster',
         'mussels', 'lobster', 'carp', 'shrimp', 'snapper', 'bass', 'seafood', 'crab', 'squid', 'octopus', 'clam',
         'scallop', 'snail', 'escargot', 'prawn', 'langoustine', 'ham', 'bacon', 'pancetta', 'prosciutto', 'sausage',
         'calamari', 'venison', 'chuck']
VEG_TO_SUB = ['eggplant', 'tofu', 'jackfruit']
BROTHS = ['chicken broth', 'chicken stock', 'beef broth', 'beef stock']
MEAT_METHODS = ['skin', 'devein', 'trim', 'thaw', 'debone', 'shuck', 'shell']
TOFU_TIMES = {'ingredient': 'tofu',
              'pan-fry': '7 minutes',
              'grill': '7 minutes on each side',
              'bake': '15 minutes'}
MUSHROOM_TIMES = {'ingredient': 'mushrooms',
                  'pan-fry': '4 minutes',
                  'grill': '10 minutes',
                  'bake': '15 minutes'}
CHICKEN_TIMES = {'ingredient': 'chicken',
                 'pan-fry': '10 minutes',
                 'grill': '10 minutes',
                 'bake': '25 minutes'}
tofu_ingredient = food('tofu', 50, 'mL', 'extra-firm non-silken', 'pressed cubed')
portobello_ingredient = food('portobello mushrooms', 1, '', '', '')
baby_bella_ingredient = food('baby bella mushrooms', 0.5, 'cups', '', 'diced')


def remove_meat_methods(directions, recipe_meats, sub, new_directions):
    for direction in directions:
        if any([meat.name in direction.ingredient for meat in recipe_meats]) \
                or any([meat in direction.step for meat in ['meat', 'seafood', 'fish']]):
            step_sents = direction.step.split(".")
            for method in direction.method:
                if method in MEAT_METHODS:
                    for i, sent in enumerate(step_sents):
                        if method in sent:
                            if method != "shell":
                                step_sents.remove(sent)
                                for tool in direction.tool:
                                    if tool in sent:
                                        direction.tool.remove(tool)
                            else:
                                if "remove" in sent.lower() or "cut" in sent.lower():
                                    step_sents.remove(sent)
                                    for tool in direction.tool:
                                        if tool in sent:
                                            direction.tool.remove(tool)
                                else:
                                    step_sents[i] = make_substitutions("shell shells", sub.name, sent)
            direction_text = ".".join(step_sents)
            direction.step = direction_text
        new_directions.append(direction)
    return new_directions


def meat_cooking(step, methods, times, tools, ingredients, dict):
    for method in methods:
        if method in step.lower():
            if not any([ing.name in step for ing in ingredients]):
                if method == "cook" or method == "saute":
                    if "oven" in step:
                        for time in times:
                            if time in step:
                                times.remove(time)
                                times.append(dict['bake'])
                                break
                        step = "Bake %s for %s" % (dict['ingredient'], dict['bake'])
                    elif "grill" in step:
                        for time in times:
                            if time in step:
                                times.remove(time)
                                times.append(dict['grill'])
                                break
                        step = "Grill %s for %s" % (dict['ingredient'], dict['grill'])
                    else:
                        for time in times:
                            if time in step:
                                times.remove(time)
                                times.append(dict['pan-fry'])
                                break
                        for tool in tools:
                            if tool in step:
                                step = "Cook %s for %s using the %s" % (dict['ingredient'], dict['pan-fry'], tool)
                                break
                        else:
                            step = "Cook %s for %s" % (dict['ingredient'], dict['pan-fry'])
                elif method == "bake" or "oven" in step:
                    for time in times:
                        if time in step:
                            times.remove(time)
                            times.append(dict['bake'])
                            break
                    step = "Bake %s for %s" % (dict['ingredient'], dict['bake'])
                elif method == "grill":
                    for time in times:
                        if time in step:
                            times.remove(time)
                            times.append(dict['grill'])
                            break
                    step = "Grill %s for %s" % (dict['ingredient'], dict['grill'])
    return step


def replace_meat(servings, meat_ing, sub, new_ingredient_info, new_directions, dict):
    new_ingredient_info.remove(meat_ing)
    sub.quant *= servings
    new_ingredient_info.append(sub)
    for i, direction in enumerate(new_directions):
        direction.step = direction.step.replace(" until pink", "")
        direction.step = direction.step.replace(", until no longer pink, ", "")
        direction.step = direction.step.replace(", until no longer pink inside, ", "")
        direction.step = direction.step.replace(" until seafood is opaque", "")
        direction.step = direction.step.replace(" check for and remove any dark veins", "")
        if meat_ing.name in direction.ingredient:
            direction.ingredient.remove(meat_ing.name)
            direction.ingredient.append(sub.name)
            step_sents = direction.step.split(".")
            for ind, sent in enumerate(step_sents):
                if any([meat in sent for meat in MEATS + ['meat', 'seafood', 'fish']]):
                    sent = meat_cooking(sent, direction.method, direction.time, direction.tool, new_ingredient_info,
                                        dict)
                    step_sents[ind] = sent
            step_sents = ".".join(step_sents)
            make_subs_desc = ""
            if meat_ing.desc:
                if type(meat_ing.desc) == str:
                    make_subs_desc = " " + meat_ing.desc
                else:
                    for desc in meat_ing.desc:
                        make_subs_desc += " " + desc
            direction.step = make_substitutions(meat_ing.name + ' meat seafood fish' + make_subs_desc, sub.name,
                                                step_sents)
    return new_ingredient_info, new_directions


def remove_meat(meat, new_ingredient_info, new_directions):
    new_ingredient_info.remove(meat)
    for ing in new_ingredient_info:
        if ing.name == meat.name:
            new_ingredient_info.remove(ing)
    for i, direction in enumerate(new_directions):
        if meat.name in direction.ingredient:
            direction.ingredient.remove(meat.name)
            step_sents = direction.step.split(".")
            for index, sent in enumerate(step_sents):
                if any([word in sent for word in meat.name.split()]):
                    if any([ingredient.name in sent for ingredient in new_ingredient_info]):
                        ind = 0
                        for char in [';', ',']:
                            sent = sent.replace(char, "")
                        sent_lst = sent.split()
                        for word in meat.name.split():
                            if word in sent_lst:
                                ind = sent_lst.index(word)
                                sent_lst.remove(word)
                        if "and" == sent_lst[ind - 1]:
                            del sent_lst[ind - 1]
                        step_sents[index] = " ".join(sent_lst)
                    else:
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


def to_vegetarian(recipe):
    print("===============")
    print("== CHANGELOG ==")
    full_ingredient_info, ingredients = extract_food_info(recipe.ingredients)
    new_ingredient_info = full_ingredient_info
    directions, master_tools, master_methods = extract_directional_info(recipe.directions, ingredients)
    recipe_meats = []
    main_meat = ""
    for ingredient in full_ingredient_info:
        if any([ingredient.name == broth for broth in BROTHS]):
            print("Replacing %s with vegetable broth" % ingredient.name)
            new_broth_name = "vegetable broth"
            new_broth_quant = ingredient.quant
            new_broth_meas = ingredient.meas
            new_broth = food(new_broth_name, new_broth_quant, new_broth_meas, [], [])
            new_ingredient_info.remove(ingredient)
            new_ingredient_info.append(new_broth)
            for dir in directions:
                if ingredient.name in dir.ingredient:
                    dir.step = make_substitutions(ingredient.name, new_broth_name, dir.step)
                    dir.ingredient.remove(ingredient.name)
                    dir.ingredient.append(new_broth_name)
    for ingredient in full_ingredient_info:
        if any([meat in ingredient.name for meat in MEATS]):
            if any([word in recipe.name for word in ingredient.name.split()]):
                main_meat = ingredient
            else:
                recipe_meats.append(ingredient)
    if main_meat:
        if any(["mushrooms" in ingredient for ingredient in ingredients]):
            print("Replacing %s with tofu" %main_meat.name)
            sub = tofu_ingredient
            times = TOFU_TIMES
        else:
            if "fry" not in master_methods and "grill" not in master_methods and "bake" not in master_methods:
                print("Replacing %s with diced portobello mushrooms" %main_meat.name)
                portobello_ingredient.prep = 'diced'
            else:
                print("Replacing %s with whole portobello mushrooms" % main_meat.name)
                portobello_ingredient.prep = []
            sub = portobello_ingredient
            times = MUSHROOM_TIMES
        if recipe_meats:
            directions = remove_meat_methods(directions, recipe_meats + [main_meat], sub, [])
            new_ingredient_info, new_directions = replace_meat(recipe.servings, main_meat,
                                                               sub,
                                                               new_ingredient_info,
                                                               directions, times)
            for meat in recipe_meats:
                print("Removing %s from recipe" %meat.name)
                new_ingredient_info, new_directions = remove_meat(meat, new_ingredient_info, new_directions)
        else:
            directions = remove_meat_methods(directions, [main_meat], sub, [])
            new_ingredient_info, new_directions = replace_meat(recipe.servings, main_meat,
                                                               sub,
                                                               new_ingredient_info,
                                                               directions, times)
    elif recipe_meats:
        if any(["mushrooms" in ingredient for ingredient in ingredients]):
            print("Replacing %s with tofu" % recipe_meats[0].name)
            sub = tofu_ingredient
            times = TOFU_TIMES
        else:
            print("Replacing %s with baby bella mushrooms" % recipe_meats[0].name)
            sub = baby_bella_ingredient
            times = MUSHROOM_TIMES
        directions = remove_meat_methods(directions, recipe_meats, sub, [])
        new_ingredient_info, new_directions = replace_meat(recipe.servings, recipe_meats[0],
                                                           sub,
                                                           new_ingredient_info,
                                                           directions, times)
        if len(recipe_meats) > 1:
            for meat in recipe_meats[1:]:
                new_ingredient_info, new_directions = remove_meat(meat, new_ingredient_info, new_directions)
    else:
        print("This recipe is already vegetarian")
        return recipe
    return make_recipe_obj(recipe, new_ingredient_info, new_directions)


def add_meat(servings, ingredients, directions, meat, recipe_name):
    meat.quant *= servings
    ingredients.append(meat)
    if meat.name == "bacon":
        directions.insert(0,
                          direction(
                              "Place bacon in a skillet over medium-high heat and cook until crispy. "
                              "Chop into small pieces and save for later.",
                              ['bacon'],
                              ['place', 'cook', 'chop'],
                              ['skillet'], []))
        directions.insert(len(directions),
                          direction("Sprinkle bacon bits over the top and serve.",
                                    ['bacon'],
                                    ['sprinkle', 'serve'], [], []))
    elif meat.name == "ham":
        for dir in directions:
            if any(["bread" in ing for ing in dir.ingredient]):
                if "layer" in dir.method:
                    split_step = dir.step.split(".")
                    for i, sent in enumerate(split_step):
                        if "layer" in sent:
                            splt = sent.split()
                            ind = splt.index("layer")
                            try:
                                ind2 = splt[ind:].index("with")
                                splt.insert(len(splt[:ind]) + ind2 + 1, "ham")
                                splt.insert(len(splt[:ind]) + ind2 + 2, "and")
                                sent = " ".join(splt)
                                split_step[i] = sent
                            except ValueError:
                                split_step.insert(i + 1, "Add a layer of ham.")
                    dir.step = ".".join(split_step)
                elif "add" in dir.method:
                    split_step = dir.step.split(".")
                    for i, sent in enumerate(split_step):
                        if "add" in sent:
                            splt = sent.split()
                            ind = splt.index("add")
                            splt.insert(ind + 1, "ham")
                            splt.insert(ind + 2, "and")
                            sent = " ".join(splt)
                            split_step[i] = sent
                    dir.step = ".".join(split_step)

    elif meat.name == "shrimp":
        directions.insert(0,
                          direction(
                              "Cook shrimp in a skillet until pink. Save for later.",
                              ['shrimp'],
                              ['cook'],
                              ['skillet'], []))
        directions.insert(len(directions),
                          direction("Mix the shrimp into the dish and serve.",
                                    ['shrimp'],
                                    ['mix', 'serve'], [], []))
    elif meat.name == "ground beef":
        directions.insert(0,
                          direction(
                              'Place the ground beef into a skillet over medium heat.'
                              'Cook the meat, chopping it into small chunks as it cooks, until no longer pink, about 10 minutes.',
                              ['ground beef'],
                              ['place', 'cook', 'chop'],
                              ['skillet'],
                              ['10 minutes']
                          ))
        for dir in directions:
            if (any(["noodle" in ingredient for ingredient in
                    dir.ingredient]) or "sauce" in dir.step) and ("layer" in dir.step or "arrange" in dir.step):
                splt = dir.step.split(".")
                for i, sent in enumerate(splt):
                    if "layer" in sent:
                        splt.insert(i + 1, "Layer the meat on top")
                        dir.step = ".".join(splt)
                        break
                        break
                    elif "arrange" in sent:
                        splt.insert(i+1, "Layer the meat on top")
                        dir.step = ".".join(splt)
                        break
                        break
    elif meat.name == "chicken breast":
        if "salad" in recipe_name:
            directions.insert(0,
                              direction('Cook chicken breast in a pan over medium heat until cooked through.'
                                        'Slice chicken breast into strips and save for later.',
                                        ['chicken breast'],
                                        ['cook', 'slice'],
                                        ['pan'],
                                        []))
            directions.insert(len(directions),
                              direction("Top salad with chicken strips and serve.",
                                        ['chicken breast'],
                                        ['top', 'serve'],
                                        [],
                                        []))
        else:
            for dir in directions:
                if "heat" in dir.method:
                    split = dir.step.split(".")
                    for i, sent in enumerate(split):
                        if "heat" in sent.lower() and ("skillet" in sent or "pan" in sent or "pot" in sent):
                            split.insert(i + 1, "Add chicken breast and cook for about 10 minutes, until cooked through")
                            break
                            break
                    dir.step = ".".join(split)
    return ingredients, directions


def replace_with_meat(servings, ingredients, directions, meat, veg):
    ingredients.remove(veg)
    meat.quant *= servings
    ingredients.append(meat)
    if meat.name == "shredded chicken":
        for dir in directions:
            if veg.name in dir.ingredient:
                split = dir.split(".")
                for i, sent in enumerate(split):
                    if "cook" in sent.lower() or "saute" in sent.lower() and any([w in sent for w in veg.name.split()]):
                        sent = "Cook %s for 8-10 minutes" % meat.name
                        split[i] = sent
                    elif "rinse" in sent.lower() and len(dir.ingredient) == 1:
                        split.remove(sent)
                dir.step = ".".join(split)
    else:
        for dir in directions:
            if veg.name in dir.ingredient:
                dir.ingredient.remove(veg.name)
                dir.ingredient.append(meat.name)
                step_sents = dir.step.split(".")
                for ind, sent in enumerate(step_sents):
                    if "tofu" in sent:
                        sent = meat_cooking(sent, dir.method, dir.time, dir.tool, ingredients, CHICKEN_TIMES)
                        step_sents[ind] = sent
                dir.step = ".".join(step_sents)
    for dir in directions:
        if veg.name in dir.ingredient:
            dir.step = make_substitutions(veg.name, meat.name, dir.step)
            dir.ingredient.remove(veg.name)
            dir.ingredient.append(meat.name)

    return ingredients, directions


def from_vegetarian(recipe):
    full_ingredient_info, ingredients = extract_food_info(recipe.ingredients)
    directions, master_tools, master_methods = extract_directional_info(recipe.directions, ingredients)
    chicken_breast = food("chicken breast", .25, "pounds", [], ['boneless', 'skinless'])
    shredded_chicken = food("shredded chicken", 0.5, "cups", [], [])
    bacon = food("bacon", 1, "strips", [], [])
    ground_beef = food("ground beef", 1.5, "ounces", [], [])
    ham = food("ham", 2, "ounces", [], 'sliced')
    shrimp = food("shrimp", 2, "ounces", 'tailless', ['peeled', 'deveined'])
    subbed = False
    print("===============")
    print("== CHANGELOG ==")
    for ingredient in full_ingredient_info:
        if any([meat in ingredient.name for meat in MEATS]):
            print("This recipe already contains meat!")
            return recipe
    for ingredient in full_ingredient_info:
        if "jackfruit" in ingredient.name:
            print("- Replacing jackfruit with shredded chicken")
            subbed = True
            full_ingredient_info, directions = replace_with_meat(recipe.servings, full_ingredient_info, directions, shredded_chicken,
                                                                 ingredient)
        elif "tofu" in ingredient.name:
            subbed = True
            if "grilled" in recipe.name.lower() or "fried" in recipe.name.lower():
                print("- Replacing tofu with whole chicken breast")
                chicken_breast.prep = []
            else:
                print("- Replacing tofu with cut chicken breast")
                chicken_breast.prep = 'cubed'
            full_ingredient_info, directions = replace_with_meat(recipe.servings, full_ingredient_info, directions, chicken_breast,
                                                                 ingredient)
    if not subbed:
        if "salad" in recipe.name:
            print("- Adding chicken breast to salad")
            meat_sub = chicken_breast
        elif any([soup in recipe.name for soup in SOUPS]):
            print("- Adding bacon bits to soup")
            meat_sub = bacon
        elif any([cass in recipe.name for cass in CASSEROLES]):
            print("- Adding ground beef to casserole")
            meat_sub = ground_beef
        elif any([sandwich in recipe.name for sandwich in SANDWICH]):
            print("- Adding ham to sandwich")
            meat_sub = ham
        elif any([pasta in recipe.name for pasta in PASTAS]) or any([rice in recipe.name for rice in RICE]):
            print("- Mixing shrimp into rice or pasta")
            meat_sub = shrimp
        else:
            print("- Adding cut chicken breast to dish")
            chicken_breast.prep = 'cubed'
            meat_sub = chicken_breast
        full_ingredient_info, directions = add_meat(recipe.servings, full_ingredient_info, directions, meat_sub,
                                                    recipe.name)
    return make_recipe_obj(recipe, full_ingredient_info, directions)
