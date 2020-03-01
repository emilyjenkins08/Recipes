# transform from recipe to mexican cuisine

from main import main as get_recipe_info
from parse import wrapper
from parse import remove_punc_lower
from parse import food, direction, get_num
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
	if new_food == 'rice':
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

def transform_soup(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
	meat = ['chicken','turkey','fish','sausage','beef','pork','venison','bacon','ham']
	pasta = ['pasta','rice', 'macaroni','noodle','spaghetti','fettucine','rotini','orzo','tortellini','potato','potatoe']


	# this is for 4 servings
	new_food_lst = []
	new_food_name_lst = []
	new_direc_obj_lst = []

	new_food_lst.append(food("olive oil", 0.5,"teaspoon","",""))
	new_food_name_lst.append("olive oil")

	new_food_lst.append(food("garlic", 0.5,"teaspoon","","minced"))
	new_food_name_lst.append("garlic")

	new_food_lst.append(food("cumin", 0.25,"teaspoon","","ground"))
	new_food_name_lst.append("cumin")

	new_food_lst.append(food("corn kernels", 1,"cup","frozen",""))
	new_food_name_lst.append("corn kernels")

	new_food_lst.append(food("onion", 1,"cup","","chopped"))
	new_food_name_lst.append("onion")

	new_food_lst.append(food("chili powder", 0.5,"teaspoon","",""))
	new_food_name_lst.append("chili powder")

	new_food_lst.append(food("salsa", 1,"cup","","chunky"))
	new_food_name_lst.append("salsa")

	new_food_lst.append(food("corn tortilla chips", 8,"ounces","",""))
	new_food_name_lst.append("corn tortilla chips")

	new_food_lst.append(food("Monterey Jack cheese", 0.5,"cup","","shredded"))
	new_food_name_lst.append("Monterey Jack cheese")

	#get broth
	meat_present = False
	broth = False
	pasta_present = False
	pasta_sp = ""
	meat_sp = ""
	for ing in food_obj_lst:
		if "broth" in ing.name or lookup(ing,meat) or lookup(ing,pasta):
			new_food_lst.append(food(ing.name,(ing.quant / recipe_obj.servings * 4),ing.meas,ing.desc,ing.prep))
			new_food_name_lst.append(ing.name)
		if "broth" in ing.name:
			broth = True
		if lookup(ing,meat) and meat_present == False:
			meat_present = True
			meat_sp = ing.name
		if lookup(ing,pasta):
			pasta_present = True
			pasta_sp = ing.name

	if not broth:
		if meat_present and "chicken" in food_name_lst:
			new_food_lst.append(food("chicken broth", 20,"ounces",[],[]))
			new_food_name_lst.append("chicken broth")
		else:
			new_food_lst.append(food("vegetable broth", 20,"ounces",[],[]))
			new_food_name_lst.append("vegetable broth")

	if pasta_present:
		str = "Boil water in a pot and cook " + pasta_sp + ". Drain."
		new_direc_obj_lst.append(direction(str,[pasta_sp],['boil', 'cook','drain'],['pot'],[]))

	if meat_present:
		str = "In a large pot over medium heat, cook and stir the " + meat_sp + " in the oil for 5 minutes."
		new_direc_obj_lst.append(direction(str,[meat_sp,"olive oil"],["cook","stir"],["pot"],["5 minutes"]))


	new_str = "Add the garlic and cumin and mix well. Then add the "
	last_food = ""
	foodz_to_add = []
	key_ingredients = get_key(recipe_obj)
	key_ingr_obj_lst = get_key_food(recipe_obj)
	print("key ingredients are ", key_ingredients)
	for foodz in new_food_name_lst:
		if foodz != meat_sp and foodz != pasta_sp and "broth" not in foodz and "cheese" not in foodz and "chips" not in foodz:
			new_str += (foodz + ", ")
			foodz_to_add.append(foodz)
	if key_ingr_obj_lst:
		for item in key_ingr_obj_lst:
			if item.name not in new_food_name_lst:
				new_food_lst.append(food(item.name, (item.quant / recipe_obj.servings * 4),item.meas,item.desc,item.prep))
				new_food_name_lst.append(item.name)
				foodz_to_add.append(item.name)
				new_str += (item.name + ", ")
	new_str = new_str[:len(new_str)-2] + "."
	new_str = new_str[:(new_str.index(foodz_to_add[-1])-1)] + " and " + new_str[new_str.index(foodz_to_add[-1]):]
	new_str += " Reduce heat to low and simmer for about 20 to 30 minutes."
	new_direc_obj_lst.append(direction(new_str,foodz_to_add,["simmer"],[],["20 to 30 minutes"]))

	final_step = "Break up some tortilla chips into individual bowls and pour soup over chips. Top with the Monterey Jack cheese."
	new_direc_obj_lst.append(direction(final_step,["corn tortilla chips", "Monterey Jack cheese"],["break","pour",'top'],[],[]))


	food_obj_lst = new_food_lst
	food_name_lst = new_food_name_lst
	direc_obj_lst = new_direc_obj_lst

	for ing in new_food_lst:
		ing.print_food()
	for step in direc_obj_lst:
		step.print_dir()

	return

def transform_dessert(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
	desserts = ['cookie', 'brownie','pie','cake','cupcake','ice cream','popsicle','donut','pastry','croissant','churro','chocolate','caramel','butterscotch','dessert','candy','m&m','meringue','bread','loaf','muffin','strudel','babka','gelato','sorbet','cracker','apple crisp','biscuit','cannoli','doughnut','eclair','flan','waffle','biscotti','pudding','pancake','cheesecake','frosting','mousse','cinnamon roll','custard','crepe','frozen yogurt','fudge','froyo','gingersnap','gelatin','gingerbread','sundae','icing','jam','jellyroll','jelly','marshmallow','milkshake','macaroon','macaron','nougat','parfait','brittle','praline',"s'mores",'snickerdoodle','shortbread','scone','sugar','sweets','torte','tart','toffee','trifle','turnover']

	new_food_lst = []
	new_food_name_lst = []
	new_direc_obj_lst = []

	flan_desserts = ['pie','cake','cupcake','ice cream','popsicle','flan','pudding','frosting','custard','gelato','sorbet','mousse','frozen yogurt','fudge','froyo','gelatin','sundae','icing','jam','jelly','jellyroll','marshmallow','milkshake','parfait','praline',"s'mores",'sugar','tart','torte','toffee','trifle','turnover']
	churro_desserts = ['cookie','brownie','donut','doughnut','pastry','croissant','churro','caramel','butterscotch','candy','m&m','meringue','bread','loaf','muffin','strudel','babka','cracker','apple crisp','biscuit','cannoli','eclair','waffle','pancake','biscotti','cinnamon roll','crepe','gingersnap','gingerbread','macaron','macaroon','nougat','shortbread','scone']
	type_churro = lookup(recipe_obj,churro_desserts)
	if True: # makes four servings
		if type_churro:
			new_food_lst.append(food("water", 1,"cup","",""))
			new_food_name_lst.append("water")

			new_food_lst.append(food("white sugar", 10.5,"tablespoons","",""))
			new_food_name_lst.append("white sugar")

			new_food_lst.append(food("salt", 0.5,"teaspoon","",""))
			new_food_name_lst.append("salt")

			new_food_lst.append(food("vegetable oil", 2,"tablespoons","",""))
			new_food_name_lst.append("vegetable oil")

			new_food_lst.append(food("all-purpose flour", 1,"cup","",""))
			new_food_name_lst.append("all-purpose flour")

			new_food_lst.append(food("oil", 2,"quarts","",""))
			new_food_name_lst.append("oil")

			new_food_lst.append(food("cinnamon", 1,"teaspoon","","ground"))
			new_food_name_lst.append("cinnamon")

			str = "In a small saucepan over medium heat, combine water, 2 1/2 tablespoons sugar, salt and 2 tablespoons vegetable oil. Bring to a boil and remove from heat. Stir in flour until mixture forms a ball."
			new_direc_obj_lst.append(direction(str,['water','sugar','salt','vegetable oil','flour'],['combine','boil','stir'],['saucepan'],[]))

			str2 = "Heat oil for frying in deep-fryer or deep skillet to 375 degrees F (190 degrees C). Pipe strips of dough into hot oil using a pastry bag. Fry until golden; drain on paper towels."
			new_direc_obj_lst.append(direction(str2,['oil'],['heat','pipe','fry','drain'],['deep-fryer or deep skillet''pastry bag','paper towels'],[]))

			str3 = "Combine 1/2 cup sugar,"
			str4 = "and cinnamon. Roll drained churros in the mixture."
			ingree = ['sugar','cinnamon']
			key_ingrr = get_key_food(recipe_obj)
			if key_ingrr:
				for food1 in key_ingrr:
					str3 = str3 + " " + food1.name + ", "
					new_food_lst.append(food(food1.name,(food1.quant / recipe_obj.servings * 4),food1.meas,food1.desc,food1.prep))
					new_food_name_lst.append(food1.name)
					ingree.append(food1.name)
			new_direc_obj_lst.append(direction(str3+str4,[ingree],['combine','roll'],[],[]))

		else:
		#if wrd in flan_desserts: # one flan, 12 servings
			new_food_lst.append(food("white sugar", 0.25,"cup","",""))
			new_food_name_lst.append("white sugar")

			new_food_lst.append(food("sweetened condensed milk", 14,"ounces","",""))
			new_food_name_lst.append("condensed milk")

			new_food_lst.append(food("evaporated milk", 14,"ounces","",""))
			new_food_name_lst.append("evaporated milk")

			new_food_lst.append(food("eggs", 5,"","",""))
			new_food_name_lst.append("eggs")

			new_food_lst.append(food("cream cheese", 8,"ounces","","softened"))
			new_food_name_lst.append("cream cheese")

			new_food_lst.append(food("vanilla extract", 1,"teaspoon","",""))
			new_food_name_lst.append("vanilla extract")

			str = "Place sugar into a 9-inch ring mold and cook over medium-high heat, stirring constantly, until sugar melts and turns golden, about 10 minutes. Watch carefully for syrup to start to change color as it burns easily. Let caramel cool and harden, about 20 minutes."
			new_direc_obj_lst.append(direction(str,["sugar"],['place', 'cook','stir','cool'],['ring mold'],["10 minutes"]))

			str2 = "Combine"
			key_ingredients = get_key_food(recipe_obj)
			str3 = " sweetened condensed milk, evaporated milk, eggs, cream cheese, and vanilla extract in a blender; blend until smooth, about 1 minute. Pour mixture over the hard caramel syrup in the tin and cover with aluminum foil. Pierce foil in the center hole of the ring with a knife; peel back foil, leaving hole uncovered for steam to circulate."

			ingredients_involved = []
			if key_ingredients:
				for item in key_ingredients:
					if item.name not in new_food_name_lst:
						str3 = " " + item.name + "," + str3
						new_food_lst.append(food(item.name,(item.quant / recipe_obj.servings * 12),item.meas,item.desc,item.prep))
						new_food_name_lst.append(item.name)
						ingredients_involved.append(item.name)
			ingredients_involved = ingredients_involved + ["sweetened condensed milk","evaporated milk","eggs","cream cheese","vanilla extract"]
			new_direc_obj_lst.append(direction(str2 + str3,ingredients_involved,["blend","combine","pour","cover","pierce","peel"],["blender","tin","aluminum foil"],["1 minute"]))

			str4 = "Place a metal rack inside a large pot over medium heat. Add water to almost reach the rack; bring to a boil. Place the mold on the rack, cover the pot, and steam until flan is set and firm, about 45 minutes. Unmold flan onto a serving plate and let cool before serving."
			new_direc_obj_lst.append(direction(str4,["water","flan"],["place","add","boil","steam","unmold","cool"],["metal rack",'large pot','mold','serving plate'],['45 minutes']))


	food_obj_lst = new_food_lst
	food_name_lst = new_food_name_lst
	direc_obj_lst = new_direc_obj_lst

	for ing in food_obj_lst:
		ing.print_food()
	for step in direc_obj_lst:
		step.print_dir()

	return


def lookup_mod(sen, lst):
	name_lst = remove_punc_lower(sen).split()
	for word in name_lst:
		if word in lst:
			return True
		elif word[-1] == 's' and word[:-1] in lst:
			return True
	return False

def cut_amount_mod(step_text,lst,prop):
	def helper(sen, prop):
		sen_lst = sen.split()
		for ind in range(len(sen_lst)):
			word = sen_lst[ind]
			num = get_num([word])
			if num != 0:
				if ind + 1 < len(sen_lst) and not lookup_mod(sen_lst[ind + 1], ['more','degree','minute', 'hour', 'second', 'to']):
					num = str(num/prop)
					if num[-2:] == '.0':
						num = num[:-2]
					sen_lst[ind] = num
		sen = ' '.join(sen_lst)
		return(sen)
	step_sen = step_text.split('. ')
	for ind in range(len(step_sen)):
		sen = step_sen[ind]
		if lookup_mod(sen, lst):
			step_sen[ind] = helper(sen, prop)
	step_text = '. '.join(step_sen)
	return step_text

def transform_cuisine_main(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
	if recipe_obj.cuisine == "mexican" or recipe_obj.cuisine == "Mexican":
		print("recipe is already mexican!")
		return
	# take care of soups
	soups = ["soup", "bisque", "stew", "gumbo"]
	if lookup(recipe_obj,soups):
		transform_soup(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst)
		return

	# take care of desserts
	desserts = ['cookie', 'brownie','pie','cake','cupcake','ice cream','popsicle','donut','pastry','croissant','churro','chocolate','caramel','butterscotch','dessert','candy','m&m','meringue','bread','loaf','muffin','strudel','babka','gelato','sorbet','cracker','apple crisp','biscuit','cannoli','doughnut','eclair','flan','waffle','biscotti','pudding','pancake','cheesecake','frosting','mousse','roll','custard','crepe','frozen yogurt','fudge','froyo','gingersnap','gelatin','gingerbread','sundae','icing','jam','jellyroll','jelly','marshmallow','milkshake','macaroon','macaron','nougat','parfait','brittle','praline',"s'mores",'snickerdoodle','shortbread','scone','sugar','sweets','torte','tart','toffee','trifle','turnover']

	if lookup(recipe_obj,desserts) or "ice cream" in remove_punc_lower(recipe_obj.name):
		print("making dessert transformation")
		transform_dessert(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst)
		return
	#if lookup(recipe_obj, desserts):
	#	transform_dessert(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst)
	#	return


	#basic lists to cycle through to make changes
	cut_half = ['cheese']
	pasta = ['pasta','macaroni','noodle','spaghetti','fettucine','fettuccini','rotini','orzo','tortellini','potatoes','potato']
	meat = ['chicken','turkey','fish','sausage','beef','pork','venison','bacon','ham']
	#initalize substitution list for making changes in the directions in reference to foods
	subs = []
	#name of the meat to substitue is initialize as empty, list is to account for multiple meats
	meat_name_lst = []
	#boolean for if the tortilla is added to directions
	add_tortilla_dir = False
	add_beans_bool = False
	add_taco_seasoning = False
	add_sour_cream_bool = False
	add_salsa_bool = False

	make_into_casserole = False
	no_starch_meat = False
	make_into_tacos = False
	make_into_rice = False
	dessert = False
	meat_lst = []
	pasta_lst = []

	for direc in direc_obj_lst:
		direc.step = cut_amount_mod(direc.step,cut_half,2)

	for ing in food_obj_lst:
		if lookup(ing, cut_half):
			ing.quant = ing.quant / 2
		meat_present = lookup(ing,meat)
		pasta_present = lookup(ing,pasta)
		if meat_present:
			meat_lst.append(meat_present)
		if pasta_present:
			pasta_lst.append(pasta_present)
			if "rice" not in food_name_lst:
				subs.append([ing.name, "rice"])
				ing.name = "rice"
				food_name_lst.append("rice")
		if remove_punc_lower(ing.name) == "basil" or remove_punc_lower(ing.name) == "basil leaves":
			ing.name = "garlic powder"
			if ing.meas != "teaspoons" and ing.meas != "tablespoons" and ing.meas != "teaspoon" and ing.meas != "tablespoon":
				ing.quant = 2
				ing.meas = "tbsp"
			ing.desc = ""
			ing.prep = ""
		if remove_punc_lower(ing.name) == "oregano" or remove_punc_lower(ing.name) == "oregano leaves":
			ing.name = "cumin"
			if ing.meas != "teaspoons" and ing.meas != "tablespoons" and ing.meas != "teaspoon" and ing.meas != "tablespoon":
				ing.quant = 2
				ing.meas = "tbsp"
			ing.desc = ""
			ing.prep = ""
		if remove_punc_lower(ing.name) == "rosemary" or remove_punc_lower(ing.name) == "rosemary leaves":
			ing.name = "thyme"
			if ing.meas != "teaspoons" and ing.meas != "tablespoons" and ing.meas != "teaspoon" and ing.meas != "tablespoon":
				ing.quant = 2
				ing.meas = "tbsp"
			ing.desc = ""
			ing.prep = ""
		if remove_punc_lower(ing.name) == "parsley" or remove_punc_lower(ing.name) == "parsley leaves":
			ing.name = "chili powder"
			if ing.meas != "teaspoons" and ing.meas != "tablespoons" and ing.meas != "teaspoon" and ing.meas != "tablespoon":
				ing.quant = 2
				ing.meas = "tbsp"
			ing.desc = ""
			ing.prep = ""
		for diir in direc_obj_lst:
			if "parsley" in diir.step:
				diir.step = diir.step.replace("parsley","chili powder")
			if "rosemary" in diir.step:
				diir.step = diir.step.replace("rosemary","thyme")
			if "oregano" in diir.step:
				diir.step = diir.step.replace("oregano","cumin")
			if "basil" in diir.step:
				diir.step = diir.step.replace("basil","garlic powder")


	print("meat list: ", meat_lst)
	print("pasta list: ", pasta_lst)
	print("tools used: ", tools_lst)
	if "baking dish" in tools_lst or "dish" in tools_lst or ("bake" in methods_lst and "oven" in tools_lst):
		make_into_casserole = True
		print("making into casserole")
	elif meat_lst:
		make_into_tacos = True
		add_tortilla_dir = True
		if "corn or flour tortillas" not in food_name_lst:
			food_obj_lst.append(food("corn or flour tortillas", 2 * recipe_obj.servings, "", "", ""))
			print("making into tacos")
			add_taco_seasoning = True
			food_name_lst.append("corn or flour tortillas")
		if "mexican seasoning" not in food_name_lst:
			food_obj_lst.append(food("mexican seasoning", 2,"tbsp","",""))
			food_name_lst.append("mexican seasoning")
	elif pasta_lst:
		make_into_rice = True
		print("making into rice")
		if "mexican seasoning" not in food_name_lst:
			food_obj_lst.append(food("mexican seasoning", 2,"tbsp","",""))
			food_name_lst.append("mexican seasoning")
	else:
		no_starch_meat = True
		print("no meat or starch. most likely a veggie")
		if "mexican seasoning" not in food_name_lst:
			food_obj_lst.append(food("mexican seasoning", 2,"tbsp","",""))
			food_name_lst.append("mexican seasoning")



		# HARD CODING FOR NOW
	#make_into_rice = True
	#make_into_tacos = False

	if "tomato salsa" not in food_name_lst:
		food_obj_lst.append(food("tomato salsa", 2 * recipe_obj.servings, "tbsp","",""))
		food_name_lst.append("tomato salsa")
		add_salsa_bool = True
	if "black beans" not in food_name_lst:
		food_obj_lst.append(food("black beans", 0.5 * recipe_obj.servings,"cup","",""))
		food_name_lst.append("black beans")
		add_beans_bool = True
	if "sour cream" not in food_name_lst:
		food_obj_lst.append(food("sour cream", 2 * recipe_obj.servings, "tbsp","",""))
		food_name_lst.append("sour cream")
		add_sour_cream_bool = True

	#code that adds a direction to cook beans
	if add_beans_bool:
		direc_obj_q = deque(direc_obj_lst)
		add_beans = direction("Drain and rinse beans. Cook the beans in a saucepan with a bit of water and let simmer for about 30 minutes.",['black beans'],['drain', 'cook'],['saucepan'],['30 minutes'])
		direc_obj_q.appendleft(add_beans)
		direc_obj_lst = list(direc_obj_q)

	if not make_into_casserole and not make_into_tacos:
		if add_beans_bool:
			if add_salsa_bool and add_sour_cream_bool:
				direc_obj_lst[-1].step += " Serve with beans, salsa and sour cream."
				direc_obj_lst[-1].ingredient += ["black beans", "salsa", "sour cream"]

			elif add_sour_cream_bool:
				direc_obj_lst[-1].step += " Serve with beans and sour cream."
				direc_obj_lst[-1].ingredient += ["black beans", "sour cream"]
			elif add_salsa_bool:
				direc_obj_lst[-1].step += " Serve with beans and salsa."
				direc_obj_lst[-1].ingredient += ["black beans", "salsa"]
			else:
				direc_obj_lst[-1].step += " Serve with beans."
				direc_obj_lst[-1].ingredient += ["black beans"]

		elif not add_beans_bool and add_salsa_bool and add_sour_cream_bool:
			direc_obj_lst[-1].step += " Serve with salsa and sour cream."
			direc_obj_lst[-1].ingredient += ["salsa", "sour cream"]

		elif add_salsa_bool:
			direc_obj_lst[-1].step += " Serve with salsa."
			direc_obj_lst[-1].ingredient += ["salsa"]

		elif add_sour_cream_bool:
			direc_obj_lst[-1].step += " Serve with sour cream."
			direc_obj_lst[-1].ingredient += ["sour cream"]

	if no_starch_meat:
		found = False
		key_ingredients = get_key(recipe_obj)
		for step in direc_obj_lst:
			if found == False:
				for i in key_ingredients:
					if i in step.ingredient:
						found = True
						step.step = step.step + " Mix in the mexican seasoning with the " + i + "."


	#code that adds a direction to put food in tortillas
	if make_into_tacos: # and add_tortilla_dir
		add_tortilla = direction('Scoop the prepared food into tortillas. Serve with salsa, beans, and sour cream.',['salsa','black beans','corn tortillas','sour cream'],['scoop','serve'],[],[])
		direc_obj_lst.append(add_tortilla)

	if make_into_casserole:
		str = "Add beans, salsa, and mexican seasoning to the baking dish. "
		food_obj_lst.append(food("mexican seasoning",2,"tablespoons","",""))
		found = False
		for step in direc_obj_lst:

			if found == True:
				break
			if "bake" in step.step.lower():
				found == True
				new_step = step.step.split(".")

				stopper = -1
				idx = 0
				counter = 0
				newest_step = ""
				for sentence in new_step:
					if "bake" in sentence.lower():
						stopper = counter
						break
					counter += 1
				while idx <= stopper:
					newest_step = newest_step + new_step[idx] + "."
					idx += 1
				newest_step = str + newest_step
				while idx < len(new_step):
					if idx == len(new_step) - 1:
						newest_step = newest_step + new_step[idx]
					else:
						newest_step = newest_step + new_step[idx] + "."
					idx += 1

				step.step = newest_step
				step.ingredient.append("black beans")
				step.ingredient.append("salsa")
				step.ingredient.append("mexican seasoning")
		direc_obj_lst[-1].step += " Serve with sour cream on top."
		direc_obj_lst[-1].ingredient.append("sour cream")


	if make_into_rice:
		key_ingr = get_key_food(recipe_obj)
		if key_ingr: # there exists key ingredient
			new_food_lst = []
			new_food_name_lst = []
			new_dir_obj_lst = []
			# 4 servings
			new_food_lst.append(food("vegetable oil", 3,"tablespoons","",""))
			new_food_name_lst.append("vegetable oil")

			new_food_lst.append(food("long-grain rice", 1,"cup","uncooked",""))
			new_food_name_lst.append("long-grain rice")

			new_food_lst.append(food("garlic salt", 1,"teaspoon","",""))
			new_food_name_lst.append("garlic salt")

			new_food_lst.append(food("cumin", 0.5,"teaspoon","","ground"))
			new_food_name_lst.append("cumin")

			new_food_lst.append(food("onion", 0.25,"cup","","chopped"))
			new_food_name_lst.append("onion")

			new_food_lst.append(food("tomato sauce", 0.5,"cup","",""))
			new_food_name_lst.append("tomato sauce")

			new_food_lst.append(food("chicken broth", 0.5,"cup","",""))
			new_food_name_lst.append("chicken broth")

			step1 = "Heat oil in a large saucepan over medium heat and add rice. Cook, stirring constantly, until puffed and golden. While rice is cooking, sprinkle with salt and cumin."
			new_dir_obj_lst.append(direction(step1,["vegetable oil","long-grain rice","garlic salt","cumin"],["heat","add","cook","sprinkle"],["saucepan"],[]))

			step2pt1 = "Stir in"
			step2pt2 = " onions, and cook until tender. Stir in tomato sauce and chicken broth; bring to a boil. Reduce heat to low, cover and simmer for 20 to 25 minutes. Fluff with a fork."
			made_sub = False
			ingred = ['onion','tomato sauce','chicken broth']
			for item in key_ingr:
				found = False
				if item.name in new_food_name_lst:
					found = True
				for wrd in item.name.split():
					if wrd in pasta:
						found = True
				if not found:
					if len(key_ingr) > 1:
						step2pt1 = step2pt1 + " " + item.name + ","
						made_sub = True
						ingred.append(item.name)
						new_food_lst.append(food(item.name,item.quant / recipe_obj.servings * 4,item.meas,item.desc,item.prep))
						new_food_name_lst.append(item.name)
					else:
						step2pt1 = step2pt1 + " " + item.name
						made_sub = True
						ingred.append(item.name)
						new_food_lst.append(food(item.name,item.quant / recipe_obj.servings *4,item.meas,item.desc,item.prep))
						new_food_name_lst.append(item.name)
			if made_sub:
				step2pt1 += " and"

			new_dir_obj_lst.append(direction(step2pt1 + step2pt2,ingred,['stir','cook','boil','cover','simmer','fluff'],['fork'],["20 to 25 minutes"]))



			direc_obj_lst = new_dir_obj_lst
			food_obj_lst = new_food_lst
			food_name_lst = new_food_name_lst
		else:
			#find first step where rice is present and add mexican seasoning
			#for step in direc_obj_lst:
			#	if "rice" in step.step:

			added = False
			for step in direc_obj_lst:
				if "cream" in step.step and "sour cream" not in step.step:
					step.step = step.step.replace("cream","mexican seasoning")
					for ingrr in step.ingredient:
						if "cream" in ingrr.lower() and ingrr.lower() != "sour cream":
							step.ingredient.remove(ingrr)
							step.ingredient.append("mexican seasoning")
			for ing in food_obj_lst:
				if "cream" in ing.name and "sour cream" not in ing.name and not added:
					ing.name = "mexican seasoning"
					ing.quant = 2
					ing.meas = "tablespoons"
					ing.desc = []
					ing.prep = []
					added = True
			if not added:
				food_obj_lst.append(food("mexican seasoning",2,"tablespoons","",""))
				for oob in direc_obj_lst:
					for ob in pasta_lst:
						for wrd in ob.split():
							if not added:
								if wrd in oob.step:
									oob.step += " Mix in mexican seasoning."
									added = True



	if add_taco_seasoning and meat_present: # currently, mexican seasoning only added to the meat
		for meatz in meat_name_lst:
			found = False
			for step in direc_obj_lst:
				if found == True:
					break
			#for meatz in meat_name_lst:
				if meatz in step.ingredient:
					found = True
					new_step = step.step.split(".")
					stopper = -1
					idx = 0
					counter = 0
					newest_step = ""
					for sentence in new_step:
						if meatz in sentence:
							stopper = counter
							break
						counter += 1
					while idx <= stopper:
						newest_step = newest_step + new_step[idx] + "."
						idx += 1
					newest_step = newest_step + " Mix in the mexican seasoning with the meat."
					while idx < len(new_step):
						if idx == len(new_step) - 1:
							newest_step = newest_step + new_step[idx]
						else:
							newest_step = newest_step + new_step[idx] + "."
						idx += 1

					step.step = newest_step
					step.ingredient.append("mexican seasoning")

	#making food substitutions to the directions list
	print(subs)
	for direc in direc_obj_lst:
		for sub in subs:
			if sub[0] in direc.ingredient:
				direc.ingredient[direc.ingredient.index(sub[0])] = sub[1]
				direc.step = make_substitutions(sub[0], sub[1], direc.step)
				if 'rice' in direc.ingredient:
					for time in direc.time:
						if ("to " + time) in direc.step:
							start = direc.step.index("to " + time) - 2
							digits = ""
							while start > 0 and direc.step[start] != " ":
								digits = direc.step[start] + digits
								start -= 1
							if digits.isdigit():
								direc.step = direc.step.replace(digits + ' to ', "")

					if direc.time and ("cook" in direc.method or "boil" in direc.method):
						direc.step = direc.step.replace(direc.time[0].split()[0], "18")
						new_time = direc.time[0].split()
						direc.time = ["18 " + new_time[1]]

	for ing in food_obj_lst:
		ing.print_food()
	for step in direc_obj_lst:
		step.print_dir()

	recipe_obj.cuisine = "Mexican"
	recipe_obj.name += " transformed into Mexican"

	print(recipe_obj.name)

	return

### REMEMBER TO CHANGE CODE SO WE ADD TRANSFORMED INGREDIENT TO LIST IF NOT INITIALLY THERE

def transform_cuisine():
	url = 'https://www.allrecipes.com/recipe/14054/lasagna/'
	#url = 'https://www.allrecipes.com/recipe/232897/classic-key-lime-pie/'
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
	transform_cuisine_main(recipe, food_lst, food_name_lst, direc_lst, tools_lst, methods_lst)

transform_cuisine()
