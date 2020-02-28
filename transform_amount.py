from parse import extract_food_info, extract_directional_info, food, direction, get_num
from transform_healthy import lookup_mod
#modified cut_amount taken from the transform_healthy recipe
def cut_dir_amount(step_text,prop):
	def helper(sen, prop):
		sen_lst = sen.split()
		#print("GOT SENTENCE: ", sen)
		for ind in range(len(sen_lst)):
			word = sen_lst[ind]
			num = get_num(word)
			if num != 0:
				if ind + 1 < len(sen_lst) and not lookup_mod(sen_lst[ind + 1], ['minute', 'hour', 'second', 'to']):
					num = str(num/prop)
					if num[-2:] == '.0':
						num = num[:-2]
					sen_lst[ind] = num
		sen = ' '.join(sen_lst)
		return(sen)
	step_sen = step_text.split('.')
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

	for ing in food_obj_lst:
		ing.print_food()
	for step in direc_obj_lst:
		step.print_dir()
	return

def double_amount(recipe):
	food_lst, food_name_lst = extract_food_info(recipe.ingredients)
	direc_lst, tools_lst, methods_lst = extract_directional_info(recipe.directions, food_name_lst)
	cut_ing_amount(food_lst, direc_lst,.5)

def half_amount(recipe):
	food_lst, food_name_lst = extract_food_info(recipe.ingredients)
	direc_lst, tools_lst, methods_lst = extract_directional_info(recipe.directions, food_name_lst)
	cut_ing_amount(food_lst, direc_lst,2)

