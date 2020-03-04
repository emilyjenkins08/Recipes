# transform from recipe to asian

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


def transform_soup_indian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
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

    # makes 6 servings
	new_food_lst.append(food("vegetable oil", 1,"tablespoons","",""))
	new_food_name_lst.append("vegetable oil")

	new_food_lst.append(food("onion", 1,"","","chopped"))
	new_food_name_lst.append("onion")

	new_food_lst.append(food("garlic", 4,"cloves","","minced"))
	new_food_name_lst.append("garlic")

	new_food_lst.append(food("ginger", 2,"teaspoons","fresh","grated"))
	new_food_name_lst.append("ginger")

	new_food_lst.append(food("green chile peppers", 2,"","","chopped"))
	new_food_name_lst.append("green chile peppers")

	new_food_lst.append(food("cinnamon", 0.25,"teaspoon","","ground"))
	new_food_name_lst.append("cinnamon")

	new_food_lst.append(food("cloves", 0.25,"teaspoon","","ground"))
	new_food_name_lst.append("cloves")

	new_food_lst.append(food("coriander seed", 2,"teaspoons","","ground"))
	new_food_name_lst.append("coriander seed")

	new_food_lst.append(food("cumin", 1.5,"teaspoons","","ground"))
	new_food_name_lst.append("cumin")

	new_food_lst.append(food("turmeric", 1,"teaspoon","","ground"))
	new_food_name_lst.append("turmeric")

	new_food_lst.append(food("cardamom", 4,"pods","","bruised"))
	new_food_name_lst.append("cardamom")

	new_food_lst.append(food("apple", 1,"","","peeled cored chopped"))
	new_food_name_lst.append("apple")

	new_food_lst.append(food("potato", 1,"","large","peeled diced"))
	new_food_name_lst.append("potato")

	new_food_lst.append(food("Masoor dhal (red lentils)", 1,"cup","","rinsed drained"))
	new_food_name_lst.append("Masoor dhal (red lentils)")

	new_food_lst.append(food("vegetable broth", 8,"cups","",""))
	new_food_name_lst.append("vegetable broth")

	new_food_lst.append(food("tamarind concentrate", 1,"tablespoon","",""))
	new_food_name_lst.append("tamarind concentrate")

	new_food_lst.append(food("lemon juice", 1,"tablespoon","",""))
	new_food_name_lst.append("lemon juice")

	new_food_lst.append(food("coconut milk", 2,"cups","",""))
	new_food_name_lst.append("coconut milk")

	new_food_lst.append(food("cilantro", 2,"tablespoons","fresh","chopped"))
	new_food_name_lst.append("cilantro")

	meat_str = ""
	step1 = ""
	ing_lst = []
	items_added = []

	for ing in meat_obj_lst:
		meat_str = meat_str + ing.name + ", "
		ing_lst.append(ing.name)
		new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 6,ing.meas,ing.desc,ing.prep))
		new_food_name_lst.append(ing.name)
		items_added.append(ing.name)

	if meat_str:
		step1 = "Heat vegetable oil in large pan (use low heat); cook " + meat_str + "onion, garlic, ginger, chilies, spices and curry leaves, stirring, until onion is browned lightly, meat is cooked, and mixture is fragrant. Do not over brown the onion or else it will give the soup a burnt taste."
	else:
		step1 = "Heat vegetable oil in large pan (use low heat); cook onion, garlic, ginger, chilies, spices and curry leaves, stirring, until onion is browned lightly and mixture is fragrant. Do not over brown the onion or else it will give the soup a burnt taste."

	met_lst = ['heat']
	t_lst = ['large pan']
	new_direc_obj_lst.append(direction(step1,ing_lst,met_lst,t_lst,[]))

	ing_lst_step2 = ['carrot','apple','potato','dhal','vegetable broth','cardamom','curry']
	stepp2 = "Add carrot, "
	for veg in veggie_obj_lst:
		stepp2 = stepp2 + veg.name + ", "
		ing_lst_step2.append(veg.name)
		new_food_lst.append(food(veg.name,veg.quant/recipe_obj.servings * 6,veg.meas,veg.desc,veg.prep))
		new_food_name_lst.append(veg.name)
		items_added.append(veg.name)

	stepp2pt2 = "apple, potato, dhal, and vegetable broth to pan; simmer, covered, for about 15 minutes or until vegetables are just tender. Discard cardamom pods and curry leaves."
	new_direc_obj_lst.append(direction(stepp2+stepp2pt2,ing_lst_step2,['add','simmer','discard'],[],['15 minutes']))

	step3 = "Blend or process soup mixture, in batches, until pureed; return to pan. Add tamarind, lemon juice, coconut milk and fresh coriander; stir until heated through."
	new_direc_obj_lst.append(direction(step3,['tamarind','lemon juice','coconut milk','coriander seed'],['blend','process','add','stir'],['pan'],[]))

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
	print("- Used key ingredients from the original recipe to make Indian Mulligatawny Soup.")
	if strr:
		print("- Key ingredients added from original recipe: ", strr)
	print("===============\n")

	recipe_obj.servings = 6
	recipe_obj.cuisine = "Indian"
	recipe_obj.name += " transformed into Indian"

	return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)

def transform_dessert_indian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
	new_food_lst = []
	new_food_name_lst = []
	new_direc_obj_lst = []

	#makes 8 servings
	new_food_lst.append(food("ghee (clarified butter)", 3,"tablespoons","",""))
	new_food_name_lst.append("ghee (clarified butter)")

	new_food_lst.append(food("vermicelli pasta", 3.5,"cups","",""))
	new_food_name_lst.append("vermicelli pasta")

	new_food_lst.append(food("milk", 3.75,"cups","",""))
	new_food_name_lst.append("milk")

	new_food_lst.append(food("evaporated milk", 0.75,"cup","",""))
	new_food_name_lst.append("evaporated milk")

	new_food_lst.append(food("cashews", 0.5,"cup","",""))
	new_food_name_lst.append("cashews")

	new_food_lst.append(food("raisins", 0.5,"cup","",""))
	new_food_name_lst.append("raisins")

	new_food_lst.append(food("white sugar", 8,"tablespoons","",""))
	new_food_name_lst.append("white sugar")

	new_food_lst.append(food("vanilla extract", 0.5,"teaspoon","",""))
	new_food_name_lst.append("vanilla extract")

	items_added = []
	dessert_step = "Melt ghee in a large saucepan over medium-high heat. Add vermicelli; cook and stir until golden, 3 to 5 minutes. Pour in milk and bring to a boil. Reduce heat to medium-low. Add evaporated milk, cashews, raisins, "
	ingreed = ['ghee','vermicelli pasta','milk','evaporated milk','cashews','raisins','sugar']
	key_ingrr = get_key_food(recipe_obj)
	if key_ingrr:
		for food1 in key_ingrr:
			dessert_step = dessert_step + food1.name + ", "
			new_food_lst.append(food(food1.name,(food1.quant / recipe_obj.servings * 4),food1.meas,food1.desc,food1.prep))
			new_food_name_lst.append(food1.name)
			ingreed.append(food1.name)
			items_added.append(food1.name)
	dessert_step2 = " and sugar. Simmer until pudding begins to thicken, about 10 minutes. Serve warm or cold."
	new_direc_obj_lst.append(direction(dessert_step+dessert_step2,ingreed,['melt','add','cook','stir','pour','boil','simmer','serve'],['large saucepan'],['3 to 5 minutes','10 minutes']))

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
	print("- Used key ingredients from the original recipe to make Indian Vermicelli Pudding.")
	if strr:
		print("- Key ingredients added from original recipe: ", strr)
	print("===============\n")

	recipe_obj.servings = 8
	recipe_obj.cuisine = "Indian"
	recipe_obj.name += " transformed into Indian"

	return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)


def transform_cuisine_main_indian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
	if recipe_obj.cuisine == "indian" or recipe_obj.cuisine == "Indian":
		print("recipe is already indian!")
		return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)
	# take care of soups
	soups = ["soup", "bisque", "stew", "gumbo"]
	if lookup(recipe_obj,soups):
		return transform_soup_indian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst)

	# take care of desserts
	desserts = ['cookie', 'brownie','pie','cake','cupcake','ice cream','popsicle','donut','pastry','croissant','churro','chocolate','caramel','butterscotch','dessert','candy','m&m','meringue','bread','loaf','muffin','strudel','babka','gelato','sorbet','cracker','apple crisp','biscuit','cannoli','doughnut','eclair','flan','waffle','biscotti','pudding','pancake','cheesecake','frosting','mousse','roll','custard','crepe','frozen yogurt','fudge','froyo','gingersnap','gelatin','gingerbread','sundae','icing','jam','jellyroll','jelly','marshmallow','milkshake','macaroon','macaron','nougat','parfait','brittle','praline',"s'mores",'snickerdoodle','shortbread','scone','sugar','sweets','torte','tart','toffee','trifle','turnover']

	if lookup(recipe_obj,desserts) or "ice cream" in remove_punc_lower(recipe_obj.name):
		return transform_dessert_indian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst)


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
	new_food_lst.append(food("olive oil", 1,"tablespoons","",""))
	new_food_name_lst.append("olive oil")

	new_food_lst.append(food("onions", 2,"","","peeled quartered"))
	new_food_name_lst.append("onions")

	new_food_lst.append(food("ginger root", 1,"teaspoon","","finely chopped"))
	new_food_name_lst.append("ginger root")

	new_food_lst.append(food("garlic", 1,"teaspoon","","crushed"))
	new_food_name_lst.append("garlic")

	new_food_lst.append(food("hot (Madras) curry powder", 1,"tablespoon","",""))
	new_food_name_lst.append("hot (Madras) curry powder")

	new_food_lst.append(food("tomato sauce", 15,"ounces","",""))
	new_food_name_lst.append("tomato sauce")

	new_food_lst.append(food("coconut milk", 10,"ounces","",""))
	new_food_name_lst.append("coconut milk")

	new_food_lst.append(food("cardamom", 4,"pods","",""))
	new_food_name_lst.append("cardamom")

	new_food_lst.append(food("cinnamon stick", 1,"","",""))
	new_food_name_lst.append("cinnamon stick")

	new_food_lst.append(food("salt", 1,"teaspoon","",""))
	new_food_name_lst.append("salt")

	new_food_lst.append(food("cloves", 4,"","",""))
	new_food_name_lst.append("cloves")

	meat_str = ""
	ing_lst = ['salt','pepper','olive oil']
	met_lst = []
	if meat_obj_lst:
		if len(meat_lst) > 2:
			count1 = 0
			for ing in meat_obj_lst:
				if count1 == len(meat_lst) - 1:
					meat_str = meat_str + "and " + ing.name
					ing_lst.append(ing.name)
					new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
					new_food_name_lst.append(ing.name)
				else:
					meat_str = meat_str + ing.name + ", "
					count1 += 1
					ing_lst.append(ing.name)
					new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
					new_food_name_lst.append(ing.name)
		elif len(meat_lst) == 2:
			count = 0
			for ing in meat_obj_lst:
				if count == len(meat_lst) - 1:
					meat_str = meat_str + "and " + ing.name
					ing_lst.append(ing.name)
					new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
					new_food_name_lst.append(ing.name)
				else:
					meat_str = meat_str + ing.name + " "
					count += 1
					ing_lst.append(ing.name)
					new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
					new_food_name_lst.append(ing.name)
		else:
			for ing in meat_obj_lst:
				meat_str = meat_str + ing.name
				ing_lst.append(ing.name)
				new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
				new_food_name_lst.append(ing.name)

		sttr = "Rinse " + meat_str + " and pat dry; season with salt and pepper to taste. Heat oil in a large skillet over medium high heat, then saute " + meat_str + " until browned. Remove " + meat_str + " from skillet and set aside."
		met_lst = ['rinse','dry','season','heat','saute','remove','set']
	else:
		sttr = "Heat oil in a large skillet with salt and pepper over medium high heat."
		met_lst = ['heat']

    #step 1
	new_direc_obj_lst.append(direction(sttr,ing_lst,met_lst,['skillet'],[]))

    #step 2
	step2 = "Saute onions in skillet until translucent; add ginger and garlic and saute until fragrant, then stir in curry powder."
	new_direc_obj_lst.append(direction(step2,['onions','ginger root','garlic','curry powder'],['saute','add','stir'],['skillet'],[]))

    #step 3
	step3ingr = ['tomato sauce','coconut milk','cloves','cardamom','cinnamon stick','salt']
	step3met = ['add','season','stir']
	step4ingr = []
	if meat_str:
		step3 = "Return " + meat_str + " to skillet and add tomato sauce, coconut milk, cloves, cardamom and cinnamon stick to skillet. Season with salt to taste and stir all together."
		step4 = "Reduce heat to low and simmer until " + meat_str + " is tender and cooked through (no longer pink inside), about 20 to 25 minutes."
		for item in meat_lst:
			step3ingr.append(item)
			step4ingr.append(item)
			items_added.append(item)
		step3met.append("return")
	else:
		step3 = "Add tomato sauce, coconut milk, cloves, cardamom and cinnamon stick to skillet. Season with salt to taste and stir all together."
		step4 = "Reduce heat to low and simmer about 20 to 25 minutes."
	new_direc_obj_lst.append(direction(step3,step3ingr,step3met,['skillet'],[]))

    #step 4
	new_direc_obj_lst.append(direction(step4,step4ingr,['reduce','simmer'],[],['20 to 25 minutes']))

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
	print("- Used key ingredients from the original recipe to make Indian Curry.")
	if strr:
		print("- Key ingredients added from original recipe: ", strr)
	print("===============\n")

	recipe_obj.servings = 6
	recipe_obj.cuisine = "Indian"
	recipe_obj.name += " transformed into Indian"


	return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)

def transform_cuisine_indian(recipe_obj):
	food_lst, food_name_lst, direc_lst, tools_lst, methods_lst = wrapper(recipe_obj.ingredients, recipe_obj.directions)
	return transform_cuisine_main_indian(recipe_obj, food_lst, food_name_lst, direc_lst, tools_lst, methods_lst)
