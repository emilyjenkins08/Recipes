from transform_vegetarian import to_vegetarian
from parse import food, make_recipe_obj
from transform_healthy import make_substitutions


SUBS = {"milk": "soy milk",
        "cream cheese": "vegan cream cheese",
        "cottage cheese": "silken tofu",
        "ice cream": "soy ice cream",
        "cream": "coconut cream",
        "cheese": "vegan cheese",
        "egg": "bananas",
        "chicken broth": "vegetable broth",
        "chicken stock": "vegetable broth",
        "beef broth": "vegetable broth",
        "beef stock": "vegetable broth",
        "butter": "olive oil",
        "yogurt": "soy yogurt",
        "sour cream": "vegan sour cream",
        "mayonaisse": "vegan mayo",
        "gelatin": "agar powder",
        "honey": "maple syrup",
        "chocolate": "non-dairy chocolate",
        }


def to_vegan(recipe):
    ingredient_info, directions = to_vegetarian(recipe)
    for non_vegan in SUBS.keys():
        for dir in directions:
            for ing in dir.ingredients:
                if non_vegan in ing.name and SUBS[non_vegan] not in ing.name:
                    recipe = make_substitutions(recipe, ing, SUBS[non_vegan])
                    dir.ingredients.remove(ing)
                    ingredient_info.remove(ing)
                    sub_name = SUBS[non_vegan]
                    if sub_name not in ["bananas", "silken tofu"]:
                        sub_quant = ing.quant
                        sub_meas = ing.meas
                        sub_prep = ing.prep
                    elif sub_name == "bananas":
                        sub_quant = ing.quant * .25
                        sub_meas = "cups"
                        sub_prep = ["mashed"]
                    else:
                        sub_quant = ing.quant
                        sub_meas = ing.meas
                        sub_prep = ["mashed"]
                    sub = food(sub_name, sub_quant, sub_meas, [], sub_prep)
                    dir.ingredients.append(sub.name)
                    ingredient_info.append(sub)
