#from fuzzywuzzy import fuzz
from main import main as get_ind_lst

class ingredient:
	def __init__(self, name, quant, meas, desc, prep):
		self.name = name
		self.quant = quant
		self.meas = meas
		self.desc = desc
		self.prep = prep
	def print_ing(self):
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

#ind_lst = ['2 cups angel hair pasta', '1/2 cup butter, divided', '4 cloves garlic, minced', '1 pound uncooked medium shrimp, peeled and deveined', '1/2 cup white cooking wine','1 lemon, juiced', '1 teaspoon red pepper flakes', '3/4 cup seasoned bread crumbs', '3/4 cup freshly grated Parmesan cheese, divided', '2 tablespoon finely chopped fresh parsley']

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

def main(ind_lst):
	ing_lst = []
	#print(ind_lst, '\n')
	for item in ind_lst:
		item = item.replace("-","")
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
			mflag = True
			if wrd in measurements:
				meas = wrd
				mflag = False
				start = max(start, i + 1)
			if mflag and wrd[-1] == 's':
				if wrd[:-1] in measurements:
					meas = wrd
					start = max(start, i + 1)
			if wrd[-1] == ',':
				end = i
			if wrd in preparation:
				prep_lst.append(wrd)
			else:
				if wrd in description:
					desc_lst.append(wrd)
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
		ing_lst.append(ingredient(name, quant, meas, desc, prep))
	return ing_lst

if __name__ == '__main__':
	url = 'https://www.allrecipes.com/recipe/13436/italian-sausage-soup-with-tortellini/?internalSource=hub%20recipe&referringContentType=Search'
	lst = get_ind_lst(url)[0]
	ing_lst = main(lst)
	for ing in ing_lst:
		ing.print_ing()

