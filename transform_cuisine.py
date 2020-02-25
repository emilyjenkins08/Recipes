# transform from recipe to mexican cuisine

from main import main as get_recipe_info
from parse import wrapper
from parse import remove_punc_lower
from parse import food, direction
import string
from collections import deque

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


def main(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
	#basic lists to cycle through to make changes
	cut_half = ['cheese']
	pasta = ['pasta','macaroni','noodle','spaghetti','fettucine','rotini','orzo']
	meat = ['chicken','turkey','fish','sausage','beef','pork','venison','bacon','ham']
	#initalize substitution list for making changes in the directions in reference to foods
	subs = []
	#name of the meat to substitue is initialize as empty, list is to account for multiple meats
	meat_name_lst = []
	#boolean for if the tortilla is added to directions
	add_tortilla_dir = False
	add_beans_bool = False
	add_taco_seasoning = False
	add_salsa_bool = False

	make_into_casserole = False
	make_into_tacos = False
	make_into_rice = False
	soup = False
	dessert = False
	meat_lst = []
	pasta_lst = []

	for ing in food_obj_lst:
		meat_present = lookup(ing,meat)
		pasta_present = lookup(ing,pasta)
		if meat_present:
			meat_lst.append(meat_present)
		if pasta_present:
			pasta_lst.append(pasta_present)
	print("meat list: ", meat_lst)
	print("pasta list: ", pasta_lst)

	if meat_lst and pasta_lst or meat_lst:
		make_into_tacos = True
		add_tortilla_dir = True
		food_lst.append(food("corn or flour tortillas", "2", [], [], []))
		print("making into tacos")
	elif pasta_lst:
		make_into_rice = True
		print("making into rice")


		# HARD CODING FOR NOW
	#make_into_rice = True
	#make_into_tacos = False


	food_lst.append(food("tomato salsa", "2 tbsp", [],[],[]))
	food_lst.append(food("black beans", "1/2 cup",[],[],[]))
	food_lst.append(food("sour cream", "2 tbsp", [],[],[]))
	add_beans_bool = True
	add_salsa_bool = True

	for ing in food_obj_lst:
		###Looking if meat exists in the food and then making the appropiate subsitution to it
		other_meat = lookup(ing, meat)
		replace_pasta = lookup(ing, pasta)

		if other_meat and 'broth' not in ing.name.lower():
			meat_name_lst.append(other_meat)
			add_taco_seasoning = True
			food_lst.append(food("taco seasoning", "1 packet (2 tbsp)",[],[],[]))


		elif replace_pasta:
			subs.append([replace_pasta, 'rice'])
			ing.name = 'rice'


		###going through the other lists and seeing if changes have to be made
		if lookup(ing, cut_half):
			ing.quant = ing.quant / 2



	#code that adds a direction to cook beans
	if add_beans_bool:
		direc_obj_q = deque(direc_obj_lst)
		add_beans = direction("Drain and rinse beans. Cook the beans in a saucepan with a bit of water and let simmer for about 30 minutes.",['black beans'],['drain', 'cook'],['saucepan'],['30 minutes'])
		direc_obj_q.appendleft(add_beans)
		direc_obj_lst = list(direc_obj_q)

	#code that adds a direction to put food in tortillas
	if add_tortilla_dir and make_into_tacos:
		add_tortilla = direction('Scoop the prepared food into tortillas. Serve with salsa and sour cream.',['salsa','corn tortillas','sour cream'],['scoop','serve'],[],[])
		direc_obj_lst.append(add_tortilla)

	if make_into_rice or make_into_tacos and add_beans_bool:
		direc_obj_lst[-1].step += " Serve with beans on the side."
		if "black beans" not in direc_obj_lst[-1].ingredient:
			direc_obj_lst[-1].ingredient.append("black beans")
		if "serve" not in direc_obj_lst[-1].method:
			direc_obj_lst[-1].method.append("serve")


	if add_taco_seasoning:
		for step in direc_obj_lst:
			for meatz in meat_name_lst:
				if meatz in step.ingredient:
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
					newest_step = newest_step + " Mix in the taco seasoning with the meat."
					while idx < len(new_step):
						if idx == len(new_step) - 1:
							newest_step = newest_step + new_step[idx]
						else:
							newest_step = newest_step + new_step[idx] + "."
						idx += 1

					step.step = newest_step
					step.ingredient.append("taco seasoning")

	#making food substitutions to the directions list
	print(subs)
	for direc in direc_obj_lst:
		mod_made = False
		added_rice = False
		for sub in subs:
			new_step = make_substitutions(sub[0], sub[1], direc.step)
			if new_step != direc.step:
				mod_made = True
				direc.step = new_step
			if 'rice' in direc.step:
				added_rice = True
				for time in direc.time:
					if ("to " + time) in direc.step:
						start = new_step.index("to " + time) - 2
						digits = ""
						while start > 0 and new_step[start] != " ":
							digits = new_step[start] + digits
							start -= 1
						if digits.isdigit():
							direc.step = direc.step.replace(digits + ' to ', "")
			if sub[0] in direc.ingredient:
				direc.ingredient[direc.ingredient.index(sub[0])] = sub[1]
			if added_rice and 'rice' not in direc.ingredient:
				direc.ingredient.append('rice')
				if direc.time and mod_made and added_rice:
					direc.step = direc.step.replace(direc.time[0].split()[0], "18")
					new_time = direc.time[0].split()
					direc.time = ["18 " + new_time[1]]

	for ing in food_obj_lst:
		ing.print_food()
	for step in direc_obj_lst:
		step.print_dir()

	return

### REMEMBER TO CHANGE CODE SO WE ADD TRANSFORMED INGREDIENT TO LIST IF NOT INITIALLY THERE

if __name__ == '__main__':
    url = 'https://www.allrecipes.com/recipe/14054/lasagna/'
    recipe = get_recipe_info(url)
    food_lst, food_name_lst, direc_lst, tools_lst, methods_lst = wrapper(recipe.ingredients, recipe.directions)
    main(recipe, food_lst, food_name_lst, direc_lst, tools_lst, methods_lst)
