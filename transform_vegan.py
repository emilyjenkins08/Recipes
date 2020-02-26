from transform_vegetarian import vegetarian
from parse import food

soy_milk = food("soy_milk", 1, "cup", [], [])
vegan_cheese = food("vegan_cheese", 1, "cup", [], [])
banana = food("banana", .25, "cup", ["mashed"], [])
vegetable_broth = food("vegetable broth", 1, "cup", [], [])
olive_oil = food("olive oil", 1, "tablespoon", [], [])
soy_yogurt = food("soy yogurt", 1, "cup", ["plain"], [])
vegan_sour_cream = food()
vegan_mayo = food()
agar_powder = food()
maple_syrup = food()
vegan_cream_cheese = food()
non_dairy_choc = food()
soy_ice_cream = food()
coconut_cream = food()

SUBS = {"milk": soy_milk,
        "cream cheese": vegan_cream_cheese,
        "cream": coconut_cream,
        "cheese": vegan_cheese,
        "egg": banana,
        "broth": vegetable_broth,
        "stock": vegetable_broth,
        "butter": olive_oil,
        "yogurt": soy_yogurt,
        "sour cream": vegan_sour_cream,
        "mayonaisse": vegan_mayo,
        "gelatin": agar_powder,
        "honey": maple_syrup,
        "chocolate": non_dairy_choc,
        "ice cream": soy_ice_cream,
        }


def sub_food(recipe, food, sub):
    return recipe


def vegan(recipe):
    ingredients, ingredient_info, directions, master_tools, master_methods = vegetarian(recipe)
    for non_vegan in SUBS.keys():
        for ing in ingredient_info:
            if non_vegan in ing.name:
                recipe = sub_food(recipe, ing, SUBS[non_vegan])
    return recipe

