from transform_vegetarian import to_vegetarian
from parse import food, make_recipe_obj
from transform_healthy import make_substitutions
from parse import extract_food_info, extract_directional_info

CHEESE_NAMES = ['gouda', 'brie', 'parmesan', 'mozzarella', 'cheddar', 'pepper jack']


SUBS = {"milk": "soy milk",
        "cream cheese": "vegan cream cheese",
        "creme fraiche": "vegan cream cheese",
        "cottage cheese": "silken tofu",
        "ice cream": "soy ice cream",
        "sour cream": "vegan sour cream",
        "whipped cream": "soy ice cream",
        "cream": "coconut cream",
        "cheese": "vegan cheese",
        "egg": "banana",
        "butter": "olive oil",
        "yogurt": "soy yogurt",
        "mayonnaise": "vegan mayo",
        "gelatin": "agar powder",
        "honey": "maple syrup",
        "chocolate": "non-dairy chocolate",
        "whey protein": "pea protein"
        }


def to_vegan(recipe):
    recipe = to_vegetarian(recipe)
    ingredient_info, ingredient_names = extract_food_info(recipe.ingredients)
    directions, tools, methods = extract_directional_info(recipe.directions, ingredient_names)
    for non_vegan in SUBS.keys():
        for dir in directions:
            for ing in dir.ingredient:
                if non_vegan in ing and SUBS[non_vegan] not in ing:
                    dir.step = dir.step.replace(ing, SUBS[non_vegan])
                    dir.ingredient.remove(ing)
                    for ingredient in ingredient_info:
                        if ingredient.name == ing:
                            ingredient_info.remove(ingredient)
                            sub_name = SUBS[non_vegan]
                            if sub_name not in ["banana", "silken tofu"]:
                                sub_quant = ingredient.quant
                                sub_meas = ingredient.meas
                                sub_prep = ingredient.prep
                            elif sub_name == "banana":
                                sub_quant = ingredient.quant * .25
                                sub_meas = "cups"
                                sub_prep = "mashed"
                            else:
                                sub_quant = ingredient.quant
                                sub_meas = ingredient.meas
                                sub_prep = "mashed"
                            sub = food(sub_name, sub_quant, sub_meas, [], sub_prep)
                            dir.ingredient.append(sub.name)
                            ingredient_info.append(sub)
                            break
                elif any([cheese in ing and "cheese" not in ing for cheese in CHEESE_NAMES]):
                    dir.step = make_substitutions(ing, SUBS["cheese"], dir.step)
                    dir.ingredient.remove(ing)
                    for ingredient in ingredient_info:
                        if ingredient.name == ing:
                            ingredient_info.remove(ingredient)
                            sub_name = SUBS["cheese"]
                            sub_quant = ingredient.quant
                            sub_meas = ingredient.meas
                            sub_prep = ingredient.prep
                            sub = food(sub_name, sub_quant, sub_meas, [], sub_prep)
                            dir.ingredient.append(sub.name)
                            ingredient_info.append(sub)

    return make_recipe_obj(recipe, ingredient_info, directions)

