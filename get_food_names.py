#from fuzzywuzzy import fuzz
from main import main as get_ing_lst


class food:
	def __init__(self, name, quant, meas, desc, prep):
		self.name = name
		self.quant = quant
		self.meas = meas
		self.desc = desc
		self.prep = prep
	def print_food(self):
		print("Name: ", self.name)
		if self.quant:
			print("Quantity: ", self.quant)
		if self.meas:
			print("Measurement: ", self.meas)
		if self.desc:
			print("Description: ", self.desc)
		if self.prep:
			print("Preparation: ", self.prep)
		print('\n\n')


preparation = ['beaten','chopped','cooked','condensed', 'crushed','cut', 'cubed','deveined','diced','divided', 'drained','finely','grated','juiced','minced','peeled','rinsed','seeded','shredded','sliced','steamed','uncooked']
description = ['dried','fresh','freshly','large','medium','seasoned','small','thinly']
measurements = ['bunch','can','clove', 'cup','ounce','package','pinch', 'pint', 'pound', 'teaspoon', 'tablespoon']


def get_num(text):
	num = None
	if not text[0].isdigit():
		return num
	if '/' in text:
		ind = text.index('/')
		top = text[:ind]
		bottom = text[ind+1:]
		num = int(top) / int(bottom)
	else:
		num = int(text)
	return num

def main(ing_lst):
	food_lst = []
	for item in ing_lst:
		slt = item.split()
		i,start,end = 0,0,len(slt)
		name = ''
		quant = None
		meas = None
		desc_lst = []
		desc = None
		prep_lst = []
		prep = None
		while i < len(slt):
			wrd = slt[i]
			if wrd[0] == '(':
				i += 1
				continue
			if i == 0:
				quant = get_num(wrd)
				if quant:
					start = max(start, i + 1)
					i += 1
					continue
			if wrd in measurements:
				meas = wrd
				start = max(start, i + 1)
			else:
				if wrd[-1] == 's':
					if wrd[:-1] in measurements:
						meas = wrd
						start = max(start, i + 1)
			if wrd[-1] == ',':
				end = min(end,i)
			if wrd == '-':
				end = min(end,i-1)
			prep_found = False
			if wrd in preparation:
				prep_found = True
				prep_lst.append(wrd)
			else:
				if wrd[-1] == ',':
					if wrd[:-1] in preparation:
						prep_found = True
						prep_lst.append(wrd[:-1])
			if not prep_found:
				if wrd in description:
					desc_lst.append(wrd)
				else:
					if wrd[-1] == ',':
						if wrd[:-1] in preparation:
							prep_lst.append(wrd[:-1])
			i += 1
		if prep_lst != []:
			prep = ' '.join(prep_lst)
		if desc_lst != []:
			desc = ' '.join(desc_lst)
		name = slt[start:end+1]
		j,start = 0,0
		while j < len(name):
			if name[j] in preparation or name[j] in description:
				start = max(start, j+1)
			j += 1
		name = ' '. join(name[start:])
		if name[-1] == ',':
			name = name[:-1]
		food_lst.append(food(name, quant, meas, desc, prep))
	return food_lst


if __name__ == '__main__':
	url = 'https://www.allrecipes.com/recipe/14054/lasagna/?internalSource=hub%20recipe&referringContentType=Search'
	ing_lst = get_ing_lst(url)[0]
	food_lst = main(ing_lst)
	for food in food_lst:
		food.print_food()

