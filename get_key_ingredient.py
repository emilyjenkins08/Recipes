from parse import extract_food_info, extract_directional_info, food, direction
import string
from collections import deque

def remove_punc_lower(text):
	return text.lower().translate(str.maketrans('', '', string.punctuation)) 

#modified lookup taken from transform_healthy
def lookup(recipe, food_lst):
	recipe_name_lst = remove_punc_lower(recipe.name).split()
	key_lst =[]
	for r_name in recipe_name_lst:
		for f_name in food_lst:
			if r_name in f_name:
				key_lst.append(f_name)
			elif r_name[-1] == 's':
				if r_name[:-1] in f_name:
					key_lst.append(f_name)
	return list(set(key_lst))


def get_key_helper(recipe, food_lst, food_name_lst):
	measurements = ['bunch', 'can', 'clove', 'cup', 'ounce', 'package', 'pinch', 'pint', 'pound', 'teaspoon','tablespoon', 'container','dash']
	key_lst = lookup(recipe, food_name_lst)
	return key_lst

def get_key(recipe):
	food_lst, food_name_lst = extract_food_info(recipe.ingredients)
	direc_lst, tools_lst, methods_lst = extract_directional_info(recipe.directions, food_name_lst)
	return get_key_helper(recipe, food_lst, food_name_lst)

#same fuction except it returns a list of food objects
def get_key_food_helper(recipe, food_obj_lst):
	recipe_name_lst = remove_punc_lower(recipe.name).split()
	key_lst =[]
	for r_name in recipe_name_lst:
		for food in food_obj_lst:
			f_name = food.name
			if r_name in f_name:
				key_lst.append(food)
			elif r_name[-1] == 's':
				if r_name[:-1] in f_name:
					key_lst.append(food)
	return list(set(key_lst))

def get_key_food(recipe):
	food_lst, food_name_lst = extract_food_info(recipe.ingredients)
	direc_lst, tools_lst, methods_lst = extract_directional_info(recipe.directions, food_name_lst)
	return get_key_food_helper(recipe, food_lst)