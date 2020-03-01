import string


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


class direction:
    def __init__(self, step, ingredient, method, tool, time):
        self.step = step
        self.ingredient = ingredient
        self.method = method
        self.tool = tool
        self.time = time

    def print_dir(self):
        print("step: ", self.step)
        if self.ingredient != []:
            print("Ingredients involved: ", self.ingredient)
        if self.method != []:
            print("methods used: ", self.method)
        if self.tool != []:
            print("tools used: ", self.tool)
        if self.time != []:
            print("time included in step: ", self.time)
        print('\n\n')


def remove_punc_lower(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation))


def get_num(arr):
    num = 0
    for text in arr:
        if not text[0].isdigit() or not remove_punc_lower(text).isdigit():
            return num
        if '/' in text:
            ind = text.index('/')
            top = text[:ind]
            bottom = text[ind + 1:]
            num += (int(top) / int(bottom))
        elif '.' in text:
            ind = text.index('.')
            top = text[:ind]
            bottom = text[ind + 1:]
            num += int(top) + int(bottom) / 10 ** len(bottom)
        else:
            num += float(text)
    return num


def get_meas(wrd_lst):
    better_measurements = ['bunch', 'clove', 'cup', 'ounce', 'pinch', 'pint', 'pound', 'teaspoon',
                           'tablespoon']
    for i in wrd_lst:
        if i in better_measurements:
            return i
        else:
            if i[-1] == 's' and i[:-1] in better_measurements:
                return i
    return False


def fix_name(name, prep_lst, des_lst):
    def lookup(str1, lst):
        str_lst = str1.split()
        for i in str_lst:
            if i in lst:
                return i
            elif i[-1] in [',', '.', ';', '-']:
                return i
        return False

    other_lst = ['and', 'into', 'to', 'for', 'while']
    prep_bool = lookup(name, prep_lst)
    while prep_bool:
        name = name.replace(prep_bool, "")
        prep_bool = lookup(name, prep_lst)
    des_bool = lookup(name, des_lst)
    while des_bool:
        name = name.replace(des_bool, "")
        des_bool = lookup(name, des_lst)
    other_bool = lookup(name, other_lst)
    while other_bool:
        name = name.replace(other_bool, "")
        other_bool = lookup(name, other_lst)
    while '  ' in name:
        name = name.replace('  ', ' ')
    while name[-1] == ' ':
        name = name[:-1]
    while name[0] == " ":
        name = name[1:]
    return name


def extract_food_info(ing_lst):
    preparation = ['beaten', 'boneless', 'chopped', 'cooked', 'condensed', 'crushed', 'cut', 'cubed', 'cored',
                   'deveined', 'diced',
                   'divided', 'drained', 'finely', 'grated', 'juiced', 'minced', 'peeled', 'rinsed', 'seeded',
                   'shredded', 'skinless', 'sliced', 'steamed', 'uncooked', 'shelled', 'thawed', 'shucked']
    description = ['dried', 'fresh', 'freshly', 'large', 'medium', 'seasoned', 'small', 'thinly', 'unopened',
                   'undrained', 'ground', 'spicy', 'bone-in', 'chilled']
    measurements = ['bunch', 'can', 'clove', 'cup', 'ounce', 'package', 'pinch', 'pint', 'pound', 'teaspoon',
                    'tablespoon', 'container', 'dash', 'quart']

    food_lst = []
    food_name_lst = []
    # print(ind_lst, '\n')
    for item in ing_lst:
        slt = item.split()
        i, start, end = 0, 0, len(slt)
        name = ''
        quant = None
        meas = None
        desc_lst = []
        desc = None
        prep_lst = []
        prep = None
        if "or to taste" in item:
            item.replace("or to taste", "")
        elif "to taste" in item:
            meas = "to taste"
            slt.remove("to")
            slt.remove("taste")
        while i < len(slt):
            wrd = slt[i]
            if wrd[0] == '(':
                i += 1
                continue
            if i == 0:
                if len(slt) == 1:
                    quant = get_num([wrd])
                else:
                    quant = get_num([wrd, slt[1]])
                if quant:
                    start = max(start, i + 1)
                    i += 1
                    continue
            if wrd in measurements:
                meas = wrd
                start = max(start, i + 1)
            else:
                if wrd[-1] == 's' and wrd[:-1] in measurements:
                    meas = wrd
                    start = max(start, i + 1)
            if wrd[-1] == ',' and wrd[:-1] not in preparation and wrd[:-1] not in description:
                end = min(end, i)
            if wrd == '-':
                end = min(end, i - 1)
            prep_found = False
            if wrd in preparation:
                prep_found = True
                prep_lst.append(wrd)
                # if end <= i:
                #    end = len(slt)
                # start = max(start,i+1)
            else:
                if wrd[-1] == ',':
                    if wrd[:-1] in preparation:
                        prep_found = True
                        prep_lst.append(wrd[:-1])
                        if end <= i:
                            end = len(slt)
                        # start = max(start,i+1)

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
        name = slt[start:end + 1]
        j, start = 0, 0
        while j < len(name):
            if name[j] in preparation or name[j] in description:
                # start = max(start, j + 1)
                pass
            j += 1
        name = ' '.join(name[start:])
        if name[-1] == ',':
            name = name[:-1]
        if 'apple' in item:
            print('3', name)
        name = fix_name(name, preparation, description)
        if 'apple' in item:
            print('2', name)
        if '(' in item and ')' in item:
            # modify name to get rid of parentheses
            name = name.replace(name[name.index('('):name.index(')') + 1], "")
            if name[-1] == " ":
                name = name[:-1]
            if name[0] == " ":
                name = name[1:]
        if " and " in name:
            multi_names = name.split(" and ")
            name1 = multi_names[0]
            name2 = multi_names[1]
            food_lst.append(food(name1, quant, meas, desc, prep))
            food_lst.append(food(name2, quant, meas, desc, prep))
            food_name_lst.append(name1)
            food_name_lst.append(name2)
        else:
            food_lst.append(food(name, quant, meas, desc, prep))
            food_name_lst.append(name)
    return food_lst, food_name_lst


# helper to lowercase and remove punctuation
def remove_punc_lower(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation))


# helper modified/based off of make_substitutions() written in transform_healthy
def exist(old_food, step_text):
    text_slt = step_text.split()
    old_food_slt = [remove_punc_lower(i) for i in old_food.split()]
    ind = 0
    while ind < len(text_slt):
        wrd = text_slt[ind]
        wrd_mod = remove_punc_lower(wrd)
        if wrd_mod in old_food_slt:
            return True
        elif wrd_mod[-1] == 's' and wrd_mod[:-1] in old_food_slt:
            return True
        ind += 1
    return False


def extract_directional_info(steps, ingredient_lst):
    tools = ["pot", "pan", "oven", "oven rack", "broiler", "skillet", "saute pan", "bowl", "plate", "tongs", "fork",
             "whisk", "microwave", "baking dish", "dish"]
    times = ["minute", "hour", "second"]
    methods = ["saute", 'sauté', "broil", "boil", "fry", "fried", "poach", "cook", "whisk", "bake", "stir", "mix",
               "preheat", "set", "heat",
               "add", "remove", "place", "grate", "shake", "stir", "crush", "squeeze", "beat", "toss", "top",
               "sprinkle", "chop ", "dice", "mince", "cut", "drain", "coat", "serve", "combine", "marinate", "transfer",
               "layer", "microwave", "spoon", "pour", "season", 'shell', 'thaw', 'shuck', 'devein', 'roast']
    direc_lst = []
    master_methods = []
    master_tools = []
    for step in steps:
        tools_needed = []
        methods_used = []
        times_included = []
        ingredients_used = []
        new_step = step.lower().replace(",", "").replace(".", "").replace(";", "")
        for tool in tools:
            if tool in new_step and tool not in tools_needed:
                tools_needed.append(tool)
                if tool not in master_tools:
                    master_tools.append(tool)
        for method in methods:
            if method in new_step and method not in methods_used:
                methods_used.append(method)
                if method not in master_methods:
                    master_methods.append(method)
        for ingredient in ingredient_lst:
            if exist(ingredient, new_step) and ingredient not in ingredients_used:
                ingredients_used.append(ingredient)
        for time in times:
            if time in new_step and time not in times_included:
                start = new_step.index(time) - 2
                digits = ""
                while start > 0 and new_step[start] != " ":
                    digits = new_step[start] + digits
                    start -= 1
                times_included.append(digits + " " + time)
        direc_lst.append(
            direction(step.replace("Watch Now", ""), ingredients_used, methods_used, tools_needed, times_included))
    return direc_lst, master_tools, master_methods


def wrapper(ing_lst, step_lst):
    food_lst, food_name_lst = extract_food_info(ing_lst)
    direc_lst, master_tools, master_methods = extract_directional_info(step_lst, food_name_lst)
    return food_lst, food_name_lst, direc_lst, master_tools, master_methods
