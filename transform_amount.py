from parse import extract_food_info, extract_directional_info, food, direction, get_num, make_recipe_obj
from transform_healthy import lookup_mod
#modified cut_amount taken from the transform_healthy recipe
def cut_dir_amount(step_text,prop):
	def helper(sen, prop):
		sen_lst = sen.split()
		for ind in range(len(sen_lst)):
			word = sen_lst[ind]
			num = get_num([word])
			tools = ['pan','dish','pot','skillet','saucepan','sheet','broiler','stockpot']
			before = ['saute','baking','frying','sauce','casserole', 'sauté']
			dic = {2: ['small'], .5 : ['large','big']}
			size = ''
			other = 0
			if prop == 2:
				size = 'small '
				other = .5
			else:
				size = 'large '
				other = 2
			boo = True
			if lookup_mod(word,tools):
				if boo and ind > 1  and lookup_mod(sen_lst[ind - 1], before) and 'x' in sen_lst[ind - 2]:
					first = sen_lst[ind - 2][:sen_lst[ind - 2].index('x')]
					if first.isdigit():
						first = str(int((1/prop)*int(first)))
						sen_lst[ind - 2] = first + sen_lst[ind - 2][sen_lst[ind - 2].index('x'):]
					boo = False
				if boo and ind > 1  and  lookup_mod(sen_lst[ind - 1], before) and lookup_mod(sen_lst[ind - 2], before):
					if sen_lst[ind - 2] in dic[other]:
						sen_lst[ind - 2] = size
					elif sen_lst[ind - 2] not in dic[prop]:
						sen_lst[ind - 2] = size + sen_lst[ind - 2]
					boo = False
				if boo and ind > 0 and lookup_mod(sen_lst[ind - 1], before) and 'x' not in sen_lst[ind - 1]:
					if sen_lst[ind - 1] in dic[other]:
						sen_lst[ind - 1] = size
					elif sen_lst[ind - 1] not in dic[prop]:
						sen_lst[ind-1] = size + sen_lst[ind - 1]
					boo = False
				if boo and ind > 0  and 'x' in sen_lst[ind - 1]:
					first = sen_lst[ind - 1][:sen_lst[ind - 1].index('x')]
					if first.isdigit():
						first = str(2*int(first))
						sen_lst[ind - 1] = first + sen_lst[ind - 1][sen_lst[ind - 1].index('x')+1:]
					boo = False
				if boo and ind > 0 and not lookup_mod(sen_lst[ind - 1], before):
					if sen_lst[ind - 1] in dic[other]:
						sen_lst[ind - 1] = size
					elif sen_lst[ind - 1] not in dic[prop]:
						sen_lst[ind] = size + sen_lst[ind]
					boo = False
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

	print("===============")
	print("== CHANGELOG ==")
	print("Based on the requirements, I've made the following updates to the recipe:")
	print("- Doubled the amount of each ingredient")
	print("- Doubled the serving size for the recipe")
	print("- Adjusted the size of cooking tools used to 'large'")
	print("===============\n")

	return make_recipe_obj(recipe_obj,food_lst,direc_lst)

def half_amount(recipe_obj):
	food_lst, food_name_lst = extract_food_info(recipe_obj.ingredients)
	direc_lst, tools_lst, methods_lst = extract_directional_info(recipe_obj.directions, food_name_lst)
	cut_ing_amount(food_lst, direc_lst,2)
	recipe_obj.servings *= 0.5

	print("===============")
	print("== CHANGELOG ==")
	print("Based on the requirements, I've made the following updates to the recipe:")
	print("- Halved the amount of each ingredient")
	print("- Halved the serving size for the recipe")
	print("- Adjusted the size of cooking tools used to 'small'")
	print("===============\n")
	return make_recipe_obj(recipe_obj,food_lst,direc_lst)
