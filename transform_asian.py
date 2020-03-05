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


def transform_soup_asian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
	meat = ['pork chop', 'lamb chop', 'lamb', 'mutton', 'beef', 'rump', 'steak', 'ribeye', 'fillet', 'loin',
	         'brisket', 'pork', 'ribs', 'veal', 'turkey', 'wing', 'chicken', 'thigh', 'breast', 'liver',
	         'bone', 'drum sticks', 'duck', 'belly', 'shoulder', 'fish', 'salmon', 'tuna', 'halibut', 'walleye crudo',
	         'tilapia', 'sardine', 'mackerel', 'trout', 'cod', 'herring', 'anchovy', 'trout', 'perch', 'pollock', 'oyster',
	         'mussels', 'lobster', 'carp', 'shrimp', 'snapper', 'bass', 'seafood', 'crab', 'squid', 'octopus', 'clam',
	         'scallop', 'snail', 'escargot', 'prawn', 'langoustine', 'ham', 'bacon', 'pancetta', 'prosciutto', 'sausage',
	         'calamari', 'venison', 'chuck','pork']
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

    # makes 4 servings
	new_food_lst.append(food("olive oil", 2,"tablespoons","",""))
	new_food_name_lst.append("olive oil")

	new_food_lst.append(food("shallots", 6,"whole","","diced"))
	new_food_name_lst.append("shallots")

	new_food_lst.append(food("green onions", 2,"bunch","","chopped"))
	new_food_name_lst.append("green onions")

	new_food_lst.append(food("garlic", 8,"cloves","","minced"))
	new_food_name_lst.append("garlic")

	new_food_lst.append(food("ginger", 4,"tablespoons","fresh","minced"))
	new_food_name_lst.append("ginger")

	new_food_lst.append(food("vegetable broth", 11,"cups","low sodium",""))
	new_food_name_lst.append("vegetable broth")

	new_food_lst.append(food("star anise", 4,"whole","",""))
	new_food_name_lst.append("star anise")

	new_food_lst.append(food("soy sauce", 4,"tablespoons","",""))
	new_food_name_lst.append("soy sauce")

	new_food_lst.append(food("crimini mushrooms", 20,"ounces","","sliced"))
	new_food_name_lst.append("crimini")

	new_food_lst.append(food("rice noodles", 12,"ounces","",""))
	new_food_name_lst.append("rice noodles")

	new_food_lst.append(food("bok choy", 3,"heads","","chopped"))
	new_food_name_lst.append("bok choy")

	new_food_lst.append(food("sesame seeds", 2,"tablespoons","",""))
	new_food_name_lst.append("sesame seeds")

	new_food_lst.append(food("red pepper flakes", 2,"tablespoons","",""))
	new_food_name_lst.append("red pepper flakes")

	step1 = "Heat 1-2 tablespoons olive oil in a medium-sized stockpot over medium heat. Add the "
	items_added = []
	ing_lst = []
	if len(meat_lst) > 2:
		count = 0
		for ing in meat_obj_lst:
			if count == len(meat_lst) - 1:
				step1 = step1 + "and " + ing.name
				ing_lst.append(ing.name)
				new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
				new_food_name_lst.append(ing.name)
				items_added.append(ing.name)
			else:
				step1 = step1 + ing.name + ", "
				count += 1
				ing_lst.append(ing.name)
				new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
				new_food_name_lst.append(ing.name)
				items_added.append(ing.name)
	elif len(meat_lst) == 2:
		count = 0
		for ing in meat_obj_lst:
			if count == len(meat_lst) - 1:
				step1 = step1 + "and " + ing.name
				ing_lst.append(ing.name)
				new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
				new_food_name_lst.append(ing.name)
				items_added.append(ing.name)
			else:
				step1 = step1 + ing.name + " "
				count += 1
				ing_lst.append(ing.name)
				new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
				new_food_name_lst.append(ing.name)
				items_added.append(ing.name)
	else:
		for ing in meat_obj_lst:
			step1 = step1 + ing.name
			items_added.append(ing.name)
	step1 = step1 + " to the pot. Saute until meat is fully cooked and no longer pink."
	ing_lst.append("olive oil")
	new_direc_obj_lst.append(direction(step1,ing_lst,['saute','heat','add'],['stockpot'],[]))

	step2 = "To the oil add the diced shallots and mix well. Cook over medium heat for 4-5 minutes, or until the shallots turn translucent and start to soften. Stir often."
	new_direc_obj_lst.append(direction(step2,['olive oil','shallots'],['add','mix','cook','stir'],[],['4-5 minutes']))

	step3 = "Chop the end off of each green onion- dividing the white part from the green part. Chop and set aside the green part for topping. Meanwhile, finely chop the white part of each green onion."
	new_direc_obj_lst.append(direction(step3,['green onion'],['chop'],[],[]))

	step4 = "Add the white part of the green onions, "
	ing_invol = ['green onion','garlic','ginger','shallots']
	for ing in veggie_obj_lst:
		if ing.name not in new_food_name_lst:
			new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
			new_food_name_lst.append(ing.name)
			ing_invol.append(ing.name)
			step4 += ing.name + ", "
			items_added.append(ing.name)

	step4pt2 = "minced garlic, and ginger to the shallots and mix. Cook, stirring occasionally, for 1-2 minutes or until garlic and ginger is fragrant."
	new_direc_obj_lst.append(direction(step4 + step4pt2,ing_invol,['add','mix','cook','stir'],[],['1-2 minutes']))

	step5 = "Carefully pour the vegetable broth into the pot and bring to a simmer. To the pot add the star anise and soy sauce. Cover and continue to simmer for 10 minutes."
	new_direc_obj_lst.append(direction(step5,['vegetable broth','star anise','soy sauce'],['pour','simmer','add','cover'],['stockpot'],['10 minutes']))

	step6 = "Remove lid from the pot and carefully remove and discard each star anise from the soup. Add the sliced mushrooms, uncooked noodles, and bok choy to the pot and simmer for 5-8 minutes, or until noodles and bok choy are tender. Season to taste with red pepper flakes, sesame seeds, and the green parts of the green onions."
	new_direc_obj_lst.append(direction(step6,['star anise','mushrooms','noodles','bok choy','red pepper flakes','sesame seeds','green onions'],['remove','discard','add','simmer','season'],['stockpot'],['5-8 minutes']))

	food_obj_lst = new_food_lst
	food_name_lst = new_food_name_lst
	direc_obj_lst = new_direc_obj_lst

	strr = ''
	count = 0
	for item in items_added:
		if len(items_added) == 1:
			strr = item
		elif count == len(items_added) - 1:
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
	print("- Used key ingredients from the original recipe to make an Asian Ginger Garlic Noodle Soup with Bok Choy.")
	if strr:
		print("- Key ingredients added from original recipe: ", strr)
	print("===============\n")

	recipe_obj.servings = 4
	recipe_obj.cuisine = "Asian"
	recipe_obj.name += " transformed into Asian"

	return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)

def transform_dessert_asian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
	new_food_lst = []
	new_food_name_lst = []
	new_direc_obj_lst = []

	#makes 4 servings
	new_food_lst.append(food("white rice", 0.75,"cup","uncooked",""))
	new_food_name_lst.append("white rice")

	new_food_lst.append(food("milk", 2,"cups","","divided"))
	new_food_name_lst.append("milk")

	new_food_lst.append(food("white sugar", 0.33333,"cup","",""))
	new_food_name_lst.append("white sugar")

	new_food_lst.append(food("salt", 0.25,"teaspoon","",""))
	new_food_name_lst.append("salt")

	new_food_lst.append(food("egg", 1,"","","beaten"))
	new_food_name_lst.append("egg")

	new_food_lst.append(food("raisins", 0.6666667,"cup","golden",""))
	new_food_name_lst.append("raisins")

	new_food_lst.append(food("butter", 1,"tablespoon","",""))
	new_food_name_lst.append("butter")

	new_food_lst.append(food("vanilla extract", 0.5,"teaspoon","",""))
	new_food_name_lst.append("vanilla extract")

	step1 = "Bring 1 1/2 cups water to a boil in a saucepan; stir rice into boiling water. Reduce heat to low, cover, and simmer for 20 minutes."
	new_direc_obj_lst.append(direction(step1,['water','rice'],['boil','stir','reduce','simmer'],['saucepan'],["20 minutes"]))

	step2 = "In a clean saucepan, combine 1 1/2 cups cooked rice, 1 1/2 cups milk, "
	step2pt2 = "sugar and salt. Cook over medium heat until thick and creamy, 15 to 20 minutes. Stir in remaining 1/2 cup milk, beaten egg, and raisins; cook 2 minutes more, stirring constantly. Remove from heat and stir in butter and vanilla."
	ingreed = ['rice','milk','sugar','salt','egg','raisins','butter','vanilla extract']
	key_ingrr = get_key_food(recipe_obj)
	items_added = []
	if key_ingrr:
		for food1 in key_ingrr:
			step2 = step2 + food1.name + ", "
			new_food_lst.append(food(food1.name,(food1.quant / recipe_obj.servings * 4),food1.meas,food1.desc,food1.prep))
			new_food_name_lst.append(food1.name)
			ingreed.append(food1.name)
			items_added.append(food1.name)
	new_direc_obj_lst.append(direction(step2+step2pt2,ingreed,['combine','cook','stir','remove'],['saucepan'],['15 to 20 minutes']))

	food_obj_lst = new_food_lst
	food_name_lst = new_food_name_lst
	direc_obj_lst = new_direc_obj_lst

	strr = ''
	count = 0
	for item in items_added:
		if len(items_added) == 1:
			strr = item
		elif count == len(items_added) - 1:
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
	print("- Used key ingredients from the original recipe to make an Asian Rice Pudding.")
	if strr:
		print("- Key ingredients added from original recipe: ", strr)
	print("===============\n")

	recipe_obj.servings = 4
	recipe_obj.cuisine = "Asian"
	recipe_obj.name += " transformed into Asian"

	return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)


def transform_cuisine_main_asian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
	if recipe_obj.cuisine == "asian" or recipe_obj.cuisine == "Asian":
		print("recipe is already asian!")
		return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)
	# take care of soups
	soups = ["soup", "bisque", "stew", "gumbo"]
	if lookup(recipe_obj,soups):
		return transform_soup_asian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst)

	# take care of desserts
	desserts = ['cookie', 'brownie','pie','cake','cupcake','ice cream','popsicle','donut','pastry','croissant','churro','chocolate','caramel','butterscotch','dessert','candy','m&m','meringue','bread','loaf','muffin','strudel','babka','gelato','sorbet','cracker','apple crisp','biscuit','cannoli','doughnut','eclair','flan','waffle','biscotti','pudding','pancake','cheesecake','frosting','mousse','roll','custard','crepe','frozen yogurt','fudge','froyo','gingersnap','gelatin','gingerbread','sundae','icing','jam','jellyroll','jelly','marshmallow','milkshake','macaroon','macaron','nougat','parfait','brittle','praline',"s'mores",'snickerdoodle','shortbread','scone','sugar','sweets','torte','tart','toffee','trifle','turnover']

	if lookup(recipe_obj,desserts) or "ice cream" in remove_punc_lower(recipe_obj.name):
		return transform_dessert_asian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst)


	#basic lists to cycle through to make changes
	meat = ['pork chop', 'lamb chop', 'lamb', 'mutton', 'beef', 'rump', 'steak', 'ribeye', 'fillet', 'loin',
	         'brisket', 'pork', 'ribs', 'veal', 'turkey', 'wing', 'chicken', 'thigh', 'breast', 'liver',
	         'bone', 'drum sticks', 'duck', 'belly', 'shoulder', 'fish', 'salmon', 'tuna', 'halibut', 'walleye crudo',
	         'tilapia', 'sardine', 'mackerel', 'trout', 'cod', 'herring', 'anchovy', 'trout', 'perch', 'pollock', 'oyster',
	         'mussels', 'lobster', 'carp', 'shrimp', 'snapper', 'bass', 'seafood', 'crab', 'squid', 'octopus', 'clam',
	         'scallop', 'snail', 'escargot', 'prawn', 'langoustine', 'ham', 'bacon', 'pancetta', 'prosciutto', 'sausage',
	         'calamari', 'venison', 'chuck','pork']
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

    # makes 4 servings
	new_food_lst.append(food("vegetable oil", 2,"tablespoons","",""))
	new_food_name_lst.append("vegetable oil")

	new_food_lst.append(food("garlic", 2,"cloves","","chopped"))
	new_food_name_lst.append("garlic")

	new_food_lst.append(food("broccoli", 1,"cup","","chopped"))
	new_food_name_lst.append("brocoli")

	new_food_lst.append(food("green bell pepper", 1,"cup","","sliced"))
	new_food_name_lst.append("green bell pepper")

	new_food_lst.append(food("carrots", 1,"cup","","sliced"))
	new_food_name_lst.append("carrots")

	new_food_lst.append(food("napa cabbage", 1,"cup","","sliced"))
	new_food_name_lst.append("napa cabbage")

	new_food_lst.append(food("celery", 1,"cup","","sliced"))
	new_food_name_lst.append("celery")

	new_food_lst.append(food("bean sprouts", 1,"cup","fresh",""))
	new_food_name_lst.append("bean sprouts")

	new_food_lst.append(food("zucchini", 1,"cup","","sliced"))
	new_food_name_lst.append("zucchini")

	new_food_lst.append(food("green onions", 1,"cup","","chopped"))
	new_food_name_lst.append("green onions")

	new_food_lst.append(food("salt", 1,"teaspoon","",""))
	new_food_name_lst.append("salt")

	new_food_lst.append(food("water", 0.5,"cup","",""))
	new_food_name_lst.append("water")

	new_food_lst.append(food("mushroom soy sauce", 2,"tablespoons","",""))
	new_food_name_lst.append("mushroom soy sauce")

	new_food_lst.append(food("cornstarch", 1,"tablespoon","",""))
	new_food_name_lst.append("cornstarch")

	items_added = []
	step1pt1 = "Heat oil in a wok or large heavy skillet."
	step1intermediate = " Add "
	for ing in meat_obj_lst:
		step1intermediate = step1intermediate + ing.name + ", "
		new_food_lst.append(food(ing.name,ing.quant / recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
		new_food_name_lst.append(ing.name)
		items_added.append(ing.name)
	step1pt2 = "garlic, and oyster sauce, and stir-fry for 10 minutes."
	step1 = step1pt1 + step1intermediate + step1pt2
	new_direc_obj_lst.append(direction(step1,["oil","garlic",'oyster sauce'],['heat','add','stir-fry'],['wok or large heavy skillet'],['10 minutes']))

	step2pt1 = "Stir in "
	step2intermediate = ""
	for ing in veggie_obj_lst:
		if ing.name not in new_food_name_lst:
			step1intermediate = step1intermediate + ing.name + ", "
			new_food_lst.append(food(ing.name,ing.quant / recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
			new_food_name_lst.append(ing.name)
			items_added.append(ing.name)
	step2pt2 = "broccoli, green pepper, carrots, cabbage, celery, bean sprouts, zucchini, and green onions. Season with salt, and stir-fry for 6 to 8 minutes."
	step2 = step2pt1 + step2intermediate + step2pt2
	new_direc_obj_lst.append(direction(step2,['broccoli','green pepper','carrots','cabbage','celery','bean sprouts','zucchini','green onions','salt'],['stir','season','stir-fry'],[],['6 to 8 minutes']))

	step3 = "In a small bowl, mix together water, soy sauce and cornstarch. Stir into vegetables, and cook for 1 to 2 minutes, or until sauce is thickened."
	new_direc_obj_lst.append(direction(step3,['water','soy sauce','cornstarch'],['mix','cook'],['bowl'],['1 to 2 minutes']))


	food_obj_lst = new_food_lst
	food_name_lst = new_food_name_lst
	direc_obj_lst = new_direc_obj_lst

	strr = ''
	count = 0
	for item in items_added:
		if len(items_added) == 1:
			strr = item
		elif count == len(items_added) - 1:
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
	print("- Used key ingredients from the original recipe to make an Asian stir-fry.")
	if strr:
		print("- Key ingredients added from original recipe: ", strr)
	print("===============\n")

	recipe_obj.servings = 4
	recipe_obj.cuisine = "Asian"
	recipe_obj.name += " transformed into Asian"
	return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)

def transform_cuisine_asian(recipe_obj):
	food_lst, food_name_lst, direc_lst, tools_lst, methods_lst = wrapper(recipe_obj.ingredients, recipe_obj.directions)
	return transform_cuisine_main_asian(recipe_obj, food_lst, food_name_lst, direc_lst, tools_lst, methods_lst)
