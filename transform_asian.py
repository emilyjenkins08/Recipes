# transform from recipe to asian

from main import main as get_recipe_info
from parse import wrapper
from parse import remove_punc_lower
from parse import food, direction
import string
from collections import deque
from get_key_ingredient import get_key, get_key_food
from transform_amount import cut_ing_amount

def lookup(ing, lst):
	name_lst = ing.name.lower().translate(str.maketrans('', '', string.punctuation)).split()
	for word in name_lst:
		if word in lst:
			return ing.name
		else:
			if word[-1] == 's' and word[:-1] in lst:
				return ing.name
	return False

#this is going to be the code for substituing 'corned beef' to 'turkey' instead of 'turkey turkey'
#this will also fix 'foil' turning into 'folive oil'
#still have to write it
def make_substitutions(old_food,new_food,step_text):
	text_slt = step_text.split()
	old_food_slt = [remove_punc_lower(i) for i in old_food.split()]
	old_food_slt.append("pasta")
	old_food_slt.append("noodle")
	ind = 0
	subs = []
	rmv = []
	while ind < len(text_slt):
		wrd = text_slt[ind]
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
	subs.sort(key = lambda x: -len(x))
	for i in subs:
		if i[-1] in ['.',',',';']:
			step_text = step_text.replace(i,new_food + i[-1])
		else:
			step_text = step_text.replace(i,new_food)
	return step_text

def transform_soup_asian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
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

	print("meat list: ", meat_lst)
	print("veggie list: ", veggie_lst)

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
	ing_lst = []
	if len(meat_lst) > 2:
		count = 0
		for ing in meat_obj_lst:
			if count == len(meat_lst) - 1:
				step1 = step1 + "and " + ing.name
				ing_lst.append(ing.name)
				new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
				new_food_name_lst.append(ing.name)
			else:
				step1 = step1 + ing.name + ", "
				count += 1
				ing_lst.append(ing.name)
				new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
				new_food_name_lst.append(ing.name)
	elif len(meat_lst) == 2:
		count = 0
		for ing in meat_obj_lst:
			if count == len(meat_lst) - 1:
				step1 = step1 + "and " + ing.name
				ing_lst.append(ing.name)
				new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
				new_food_name_lst.append(ing.name)
			else:
				step1 = step1 + ing.name + " "
				count += 1
				ing_lst.append(ing.name)
				new_food_lst.append(food(ing.name,ing.quant/recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
				new_food_name_lst.append(ing.name)
	else:
		for ing in meat_obj_lst:
			step1 = step1 + ing.name
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

	step4pt2 = "minced garlic, and ginger to the shallots and mix. Cook, stirring occasionally, for 1-2 minutes or until garlic and ginger is fragrant."
	new_direc_obj_lst.append(direction(step4 + step4pt2,ing_invol,['add','mix','cook','stir'],[],['1-2 minutes']))

	step5 = "Carefully pour the vegetable broth into the pot and bring to a simmer. To the pot add the star anise and soy sauce. Cover and continue to simmer for 10 minutes."
	new_direc_obj_lst.append(direction(step5,['vegetable broth','star anise','soy sauce'],['pour','simmer','add','cover'],['stockpot'],['10 minutes']))

	step6 = "Remove lid from the pot and carefully remove and discard each star anise from the soup. Add the sliced mushrooms, uncooked noodles, and bok choy to the pot and simmer for 5-8 minutes, or until noodles and bok choy are tender. Season to taste with red pepper flakes, sesame seeds, and the green parts of the green onions."
	new_direc_obj_lst.append(direction(step6,['star anise','mushrooms','noodles','bok choy','red pepper flakes','sesame seeds','green onions'],['remove','discard','add','simmer','season'],['stockpot'],['5-8 minutes']))

	food_obj_lst = new_food_lst
	food_name_lst = new_food_name_lst
	direc_obj_lst = new_direc_obj_lst

	for ing in food_obj_lst:
		ing.print_food()
	for step in direc_obj_lst:
		step.print_dir()


	return

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
	if key_ingrr:
		for food1 in key_ingrr:
			step2 = step2 + food1.name + ", "
			new_food_lst.append(food(food1.name,(food1.quant / recipe_obj.servings * 4),food1.meas,food1.desc,food1.prep))
			new_food_name_lst.append(food1.name)
			ingreed.append(food1.name)
	new_direc_obj_lst.append(direction(step2+step2pt2,ingreed,['combine','cook','stir','remove'],['saucepan'],['15 to 20 minutes']))

	food_obj_lst = new_food_lst
	food_name_lst = new_food_name_lst
	direc_obj_lst = new_direc_obj_lst

	for ing in food_obj_lst:
		ing.print_food()
	for step in direc_obj_lst:
		step.print_dir()

	return


def transform_cuisine_main_asian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
	if recipe_obj.cuisine == "asian" or recipe_obj.cuisine == "Asian":
		print("recipe is already asian!")
		return
	# take care of soups
	soups = ["soup", "bisque", "stew", "gumbo"]
	if lookup(recipe_obj,soups):
		transform_soup_asian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst)
		return

	# take care of desserts
	desserts = ['cookie', 'brownie','pie','cake','cupcake','ice cream','popsicle','donut','pastry','croissant','churro','chocolate','caramel','butterscotch','dessert','candy','m&m','meringue','bread','loaf','muffin','strudel','babka','gelato','sorbet','cracker','apple crisp','biscuit','cannoli','doughnut','eclair','flan','waffle','biscotti','pudding','pancake','cheesecake','frosting','mousse','roll','custard','crepe','frozen yogurt','fudge','froyo','gingersnap','gelatin','gingerbread','sundae','icing','jam','jellyroll','jelly','marshmallow','milkshake','macaroon','macaron','nougat','parfait','brittle','praline',"s'mores",'snickerdoodle','shortbread','scone','sugar','sweets','torte','tart','toffee','trifle','turnover']

	if lookup(recipe_obj,desserts) or "ice cream" in remove_punc_lower(recipe_obj.name):
		print("making dessert transformation")
		transform_dessert_asian(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst)
		return


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

	print("meat list: ", meat_lst)
	print("veggie list: ", veggie_lst)


	new_food_lst = []
	new_food_name_lst = []
	new_direc_obj_lst = []

    # makes 4 servings
	new_food_lst.append(food("vegetable oil", 2,"tablespoons","",""))
	new_food_name_lst.append("vegetable oil")

	new_food_lst.append(food("garlic", 2,"cloves","","chopped"))
	new_food_name_lst.append("oil")

	new_food_lst.append(food("broccoli", 1,"cup","","chopped"))
	new_food_name_lst.append("oil")

	new_food_lst.append(food("green bell pepper", 1,"cup","","sliced"))
	new_food_name_lst.append("oil")

	new_food_lst.append(food("carrots", 1,"cup","","sliced"))
	new_food_name_lst.append("oil")

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

	step1pt1 = "Heat oil in a wok or large heavy skillet."
	step1intermediate = " Add "
	for ing in meat_obj_lst:
		step1intermediate = step1intermediate + ing.name + ", "
		new_food_lst.append(food(ing.name,ing.quant / recipe_obj.servings * 4,ing.meas,ing.desc,ing.prep))
		new_food_name_lst.append(ing.name)
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
	step2pt2 = "broccoli, green pepper, carrots, cabbage, celery, bean sprouts, zucchini, and green onions. Season with salt, and stir-fry for 6 to 8 minutes."
	step2 = step2pt1 + step2intermediate + step2pt2
	new_direc_obj_lst.append(direction(step2,['broccoli','green pepper','carrots','cabbage','celery','bean sprouts','zucchini','green onions','salt'],['stir','season','stir-fry'],[],['6 to 8 minutes']))

	step3 = "In a small bowl, mix together water, soy sauce and cornstarch. Stir into vegetables, and cook for 1 to 2 minutes, or until sauce is thickened."
	new_direc_obj_lst.append(direction(step3,['water','soy sauce','cornstarch'],['mix','cook'],['bowl'],['1 to 2 minutes']))


	food_obj_lst = new_food_lst
	food_name_lst = new_food_name_lst
	direc_obj_lst = new_direc_obj_lst

	for ing in food_obj_lst:
		ing.print_food()
	for step in direc_obj_lst:
		step.print_dir()

def transform_cuisine_asian():
	#url = 'https://www.allrecipes.com/recipe/14054/lasagna/'
	#url = 'https://www.allrecipes.com/recipe/220346/eggplant-and-ground-beef-lasagna/?internalSource=staff%20pick&referringId=16806&referringContentType=Recipe%20Hub'
	url = 'https://www.allrecipes.com/recipe/232897/classic-key-lime-pie/'
	#url = 'https://www.allrecipes.com/recipe/230103/buttery-garlic-green-beans/'
	#url = 'https://www.allrecipes.com/recipe/12974/butternut-squash-soup/?internalSource=hub%20recipe&referringId=94&referringContentType=Recipe%20Hub'
	#url = 'https://www.allrecipes.com/recipe/11679/homemade-mac-and-cheese/'
	#url = 'https://www.allrecipes.com/recipe/76129/spinach-tomato-tortellini/'
	#url = 'https://www.allrecipes.com/recipe/15925/creamy-au-gratin-potatoes/'
	#url = 'https://www.allrecipes.com/recipe/23431/to-die-for-fettuccine-alfredo/'
	#url = 'https://www.allrecipes.com/recipe/12040/spaghetti-with-marinara-sauce/'
	#url = 'https://www.allrecipes.com/recipe/15004/award-winning-soft-chocolate-chip-cookies/?internalSource=hub%20recipe&referringId=839&referringContentType=Recipe%20Hub'
	#url = 'https://www.allrecipes.com/recipe/56927/delicious-ham-and-potato-soup/?internalSource=hub%20recipe&referringId=94&referringContentType=Recipe%20Hub'
	recipe = get_recipe_info(url)
	food_lst, food_name_lst, direc_lst, tools_lst, methods_lst = wrapper(recipe.ingredients, recipe.directions)
	transform_cuisine_main_asian(recipe, food_lst, food_name_lst, direc_lst, tools_lst, methods_lst)

transform_cuisine_asian()