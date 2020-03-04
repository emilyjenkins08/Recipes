from parse import extract_food_info, extract_directional_info, food, direction, get_num, make_recipe_obj
from transform_healthy import lookup_mod
#modified cut_amount taken from the transform_healthy recipe
def cut_dir_amount(step_text,prop):
	def helper(sen, prop):
		sen_lst = sen.split()
		for ind in range(len(sen_lst)):
			word = sen_lst[ind]
			num = get_num([word])
			if num != 0:
				if ind + 1 < len(sen_lst) and not lookup_mod(sen_lst[ind + 1], ['more','degree', 'minute', 'hour', 'second', 'to']):
					if get_num([sen_lst[ind+1]]) != 0:
						num += get_num([sen_lst[ind+1]])
						sen_lst[ind +  1] = '%^&'
					num = str(num/prop)
					if len(num) >= 2 and num[-2:] == '.0':
						num = num[:-2]
					sen_lst[ind] = num
		while '%^&' in sen_lst:
			sen_lst.remove('%^&')
		sen = ' '.join(sen_lst)
		return(sen)
	step_sen = step_text.split('. ')
	for ind in range(len(step_sen)):
		sen = step_sen[ind]
		step_sen[ind] = helper(sen, prop)
	step_text = '. '.join(step_sen)
	return step_text


def cut_ing_amount(food_obj_lst, direc_obj_lst,prop):
	for ing in food_obj_lst:
		ing.quant = ing.quant / prop
	for direc in direc_obj_lst:
		direc.step = cut_dir_amount(direc.step, prop)
	return

def double_amount(recipe_obj):
	food_lst, food_name_lst = extract_food_info(recipe_obj.ingredients)
	direc_lst, tools_lst, methods_lst = extract_directional_info(recipe_obj.directions, food_name_lst)
	cut_ing_amount(food_lst, direc_lst,.5)
	recipe_obj.servings *= 2

	return make_recipe_obj(recipe_obj,food_lst,direc_lst)

def half_amount(recipe_obj):
	food_lst, food_name_lst = extract_food_info(recipe_obj.ingredients)
	direc_lst, tools_lst, methods_lst = extract_directional_info(recipe_obj.directions, food_name_lst)
	cut_ing_amount(food_lst, direc_lst,2)
	recipe_obj.servings *= 0.5

	return make_recipe_obj(recipe_obj,food_lst,direc_lst)
