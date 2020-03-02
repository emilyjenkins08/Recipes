"""
- To healthy
    - Cut fats (butter, margarine, shortening, oil in 1/2), salt, sugar (1/3 or Splenda), low-fat milk and cheese, replace cream cheese w low fat cream cheese
    - Mayonnaise — natural yogurt, or vinaigrette dressing
    - For veggies, cut oil, flavor w/ herbs
    - Whole wheat pasta (whole grains)
    - Low sodium soy sauce
    - Meat
        - Replace w/ peas, beans, lentils
        - Trim fat and remove skin before cooking
        - Replace frying with bake, grill, microwave, roast, poach
    - Healthy techniques
        - Braising, broiling, grilling, poaching, sautéing, steaming
        - Basting liquid — use wine, fruit juice, veggie juice, veggie broth instead of oil or drippings
    - Grate cheese instead of slicing (use less)
    - Increase fiber
    - soups + stews
        - cool / skim off the fat on top
        - Replace fatty meats w/ peas, beans, lentils
    - Sauces and dips
        - Replace cream, whole milk, sour cream with skim milk, low-fat yogurt
"""

from parse import extract_food_info, extract_directional_info, food, direction, get_num, make_recipe_obj
import string
from collections import deque


# helper to lowercase and remove punctuation
def remove_punc_lower(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation))


def lookup(ing, lst):
    name_lst = remove_punc_lower(ing.name).split()
    for word in name_lst:
        if word in lst:
            return ing.name
        else:
            if word[-1] == 's' and word[:-1] in lst:
                return ing.name
    return False


# helper that goes through the step text and makes replacements for it based on the subs that is passed in
# sometimes the outputted text is missing punctutaions.
def make_substitutions(old_food, new_food, step_text):
    text_slt = step_text.split()
    old_food_slt = [remove_punc_lower(i) for i in old_food.split()]
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
    subs.sort(key=lambda x: -len(x))
    for i in subs:
        if i[-1] in [';', ',', '.']:
            step_text = step_text.replace(i, new_food + i[-1])
        else:
            step_text = step_text.replace(i, new_food)
    return step_text


def lookup_mod(sen, lst):
	name_lst = remove_punc_lower(sen).split()
	for word in name_lst:
		if word in lst:
			return True
		elif word[-1] == 's' and word[:-1] in lst:
			return True
	return False

def cut_amount(step_text):
	cut_half = ['butter', 'margarine','shortening','oil','sugar', 'chocolate', 'sugar', 'buttermilk','cheese','cream']
	cut_fourth = ['salt']
	def helper(sen, prop):
		sen_lst = sen.split()
		#print("GOT SENTENCE: ", sen)
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
		if lookup_mod(sen, cut_half):
			step_sen[ind] = helper(sen, 2)
		if lookup_mod(sen, cut_fourth):
			step_sen[ind] = helper(sen, 4)
	step_text = '. '.join(step_sen)
	return step_text

def healthy(recipe_obj, food_obj_lst, food_name_lst, direc_obj_lst, tools_lst, methods_lst):
	#basic lists to cycle through to make changes
	cut_half = ['butter', 'margarine','shortening','oil','sugar', 'chocolate', 'buttermilk', 'cheese','cream']
	cut_fourth = ['salt']
	low_fat = ['milk','cheese','cream','yogurt']
	whole_grain = ['pasta','bread','rice']
	low_sodium = ['soy sauce']
	ok_meat = ['chicken','turkey','fish']
	bad_meat = ['sausage','beef','pork','venison','bacon','ham','chop','lamb','rump','steak','ribeye','loin','brisket','ribs','veal','shoulder']
	#initalize substitution list for making changes in the directions in reference to foods
	subs = []
	#name of the meat to substitue is initialize as empty, list is to account for multiple meats
	meat_name_lst = []
	#boolean for if the 'trim meat fat and skin' is added to directions
	add_trim = False
	for ing in food_obj_lst:
		###Looking if meat exists in the food and then making the appropiate subsitution to it
		other_meat = lookup(ing, ok_meat)
		if other_meat and 'broth' not in ing.name.lower():
			add_trim = True
			meat_name_lst.append(other_meat)
		replace_meat = lookup(ing, bad_meat)
		if replace_meat	:
			ing.name = 'chicken breast'
			subs.append([replace_meat, 'chicken breast'])
			add_trim = True
			meat_name_lst.append(ing.name)
		#substituion for oil
		if 'oil' in ing.name.lower():
			subs.append([ing.name, 'extra-virgin olive oil'])
			ing.name = 'extra-virgin olive oil'
		if 'ranch' in ing.name.lower():
			subs.append([ing.name, 'italian dressing'])
			ing.name = 'italian dressing'
		###going through the other lists and seeing if chances have to be made
		if lookup(ing, cut_half) or other_meat or replace_meat:
			ing.quant = ing.quant / 2
			continue
		if lookup(ing, cut_fourth):
			ing.quant = ing.quant / 4
			continue
		if lookup(ing, low_fat):
			ing.name = 'low fat ' + ing.name
			continue
		if 'mayo' in ing.name.lower():
			subs.append([ing.name, 'low fat greek yogurt'])
			ing.name = 'low fat greek yogurt'
		if 'cream' in ing.name.lower() and 'cheese' not in ing.name.lower():
			subs.append([ing.name, 'low fat greek yogurt'])
			ing.name = 'low fat greek yogurt'
		if lookup(ing, whole_grain):
			ing.name = 'whole grain ' + ing.name
			continue
		if lookup(ing, low_sodium):
			ing.name = 'low sodium ' + ing.name
	#code that adds a direction to trim fat and skin off of meat
	if add_trim:
		meat_len = len(meat_name_lst)
		meat_name = ''
		if meat_len == 1:
			meat_name = meat_name_lst[0]
		elif meat_len == 2:
			meat_name = " and ".join(meat_name_lst)
		else:
			meat_name = ', '.join(meat_name_lst[:-1]) + ' and ' + meat_name_lst[-1]
		direc_obj_q = deque(direc_obj_lst)
		trim_fat = direction('Prep the ' + meat_name + ' by trimming the fat and removing the skin.',meat_name_lst,[],[],[])
		direc_obj_q.appendleft(trim_fat)
		direc_obj_lst = list(direc_obj_q)

	#making food substitutions to the directions list
	#print(subs)
	for direc in direc_obj_lst:
		for sub in subs:
			direc.step = make_substitutions(sub[0],sub[1],direc.step)
			if sub[0] in direc.ingredient:
				direc.ingredient[direc.ingredient.index(sub[0])] = sub[1]
		direc.step = cut_amount(direc.step)
		direc.step = direc.step.replace(' fry','sauté')
		direc.step = direc.step.replace(' Fry', 'Sauté')
		direc.step = direc.step.replace(' fried', 'sautéd')
		direc.step = direc.step.replace(' Fried', 'Sautéd')
		for n, i in enumerate(direc.method):
			if i == 'fry':
				direc.method[n] = 'saute'

	return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)


def cut_amount_mod(step_text):
	double_it = ['butter', 'margarine','shortening','oil','sugar', 'chocolate', 'sugar', 'buttermilk','cheese','cream','salt']
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
		if lookup_mod(sen, double_it):
			step_sen[ind] = helper(sen, .5)
		else:
			step_sen[ind] = helper(sen, .75)
	step_text = '. '.join(step_sen)
	return step_text


def unhealthy(recipe_obj, food_obj_lst, direc_obj_lst, methods_lst):
	#basic lists to cycle through to make changes
	double = ['butter', 'margarine','shortening','oil','sugar', 'chocolate', 'buttermilk', 'cheese','cream','salt']
	remove_arr = ['low fat','Low fat','low-fat','Low-fat','whole grain','Whole grain','Multi-grain','multi-grain','lean','Lean','low sodium','Low sodium']
	#initalize substitution list for making changes in the directions in reference to foods
	subs = []

	for ing in food_obj_lst:
		if 'oil' in ing.name.lower():
			subs.append([ing.name, 'vegetable oil'])
			ing.name = 'vegetable oil'
		if 'dressing' in ing.name.lower():
			subs.append([ing.name, "ranch"])
			ing.name = 'ranch'
		if 'yogurt' in ing.name.lower():
			subs.append([ing.name, 'cream'])
			ing.name = 'cream'
		###going through the other lists and seeing if chances have to be made
		if lookup(ing, double): #or other_meat or replace_meat:
			ing.quant = ing.quant / .5
			continue
		for i in remove_arr:
			ing.name = ing.name.replace(i, '')
		ing.name.replace('  ',' ')
		if 'milk' in ing.name.lower():
			subs.append([ing.name, 'whole milk'])
			ing.name = 'whole milk'
	for direc in direc_obj_lst:
		for sub in subs:
			direc.step = make_substitutions(sub[0],sub[1],direc.step)
			if sub[0] in direc.ingredient:
				direc.ingredient[direc.ingredient.index(sub[0])] = sub[1]
		direc.step = cut_amount_mod(direc.step)
		sau_to_fry = [[' sautéd', 'fried'],[' Sautéd', 'Fried'],[' sauté','fry'],[' Sauté', 'Fry'],[' Sauted', ' Fried'], [' sauted', ' fried'],[' saute',' fry'],[' Saute', ' Fry']]
		for i in sau_to_fry:
			direc.step = direc.step.replace(i[0],i[1])
		for i in remove_arr:
			direc.step = direc.step.replace(i, '')
		direc.step = direc.step.replace('  ',' ')
		for n, i in enumerate(direc.method):
			if i == 'saute' or i == 'sauté':
				direc.method[n] = 'fry'

	return make_recipe_obj(recipe_obj,food_obj_lst,direc_obj_lst)

def to_healthy(recipe_obj):
	food_lst, food_name_lst = extract_food_info(recipe_obj.ingredients)
	direc_lst, tools_lst, methods_lst = extract_directional_info(recipe_obj.directions, food_name_lst)
	return healthy(recipe_obj, food_lst, food_name_lst, direc_lst, tools_lst, methods_lst)


def from_healthy(recipe_obj):
	food_lst, food_name_lst = extract_food_info(recipe_obj.ingredients)
	direc_lst, tools_lst, methods_lst = extract_directional_info(recipe_obj.directions, food_name_lst)
	return unhealthy(recipe_obj, food_lst, direc_lst, methods_lst)
