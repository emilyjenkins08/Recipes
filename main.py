import requests
from lxml import html
from bs4 import BeautifulSoup
from parse import wrapper, extract_food_info, extract_directional_info
from transform_vegetarian import vegetarian
from transform_healthy import to_healthy, from_healthy
from get_key_ingredient import get_key
from transform_amount import double_amount, half_amount
from transform_cuisine import transform_cuisine as transform_to_mexican
from transform_asian import transform_cuisine_asian as transform_to_asian
from transform_indian import transform_cuisine_indian as transform_to_indian

CUISINES = ['Italian', 'Mexican', 'Chinese', 'Indian', 'Thai', 'Japanese', 'Korean', 'Pakistani', 'Bangladeshi',
            'Persian', 'Filipino', 'Indonesian', 'Malaysian', 'Vietnamese', 'Asian', 'Caribbean', 'South American',
            'Latin American', 'Mediterranean', 'Lebanese', 'Turkish', 'Israeli', 'Middle Eastern',
            'North African', 'South African', 'East African', 'African', 'Greek', 'French', 'Spanish', 'German',
            'Portuguese', 'UK and Ireland', 'Czech', 'Hungarian', 'Polish', 'Russian', 'Eastern European', 'Dutch',
            'Belgian', 'Austrian', 'Scandinavian', 'Swiss', 'European', 'Australian and New Zealander', 'Canadian',
            'Amish and Mennonite', 'Jewish', 'Soul Food', 'Southern', 'Tex-Mex', 'Cajun and Creole', 'U.S.']


class recipe:
    def __init__(self, name, ingredient_groups, ingredients, directions, cuisine, servings):
        self.name = name
        self.ingredient_groups = ingredient_groups
        self.ingredients = ingredients
        self.directions = directions
        self.cuisine = cuisine
        self.servings = servings

    def print_recipe(self):
        print("Name: ", self.name.title())
        if self.cuisine:
            print("Cuisine: ", self.cuisine)
        if self.servings:
            print("Servings: ", self.servings)


def parse_ingredients(soup):
    ingredient_groups = [group.text for group in soup.find_all('span', {'data-id': '0'})]
    ingredients = [ingredient.text for ingredient in soup.find_all('span', {'itemprop': 'recipeIngredient'})
                   if ingredient.text not in ingredient_groups]
    return ingredient_groups, ingredients


def parse_directions(soup):
    directions = [direction.text.strip() for direction in
                  soup.find_all('span', {'class': 'recipe-directions__list--item'})
                  if direction.text.strip()]
    return directions


def parse_servings(soup):
    servings = soup.find('section', {'class': 'adjustServings'}).find('div', {'class': 'subtext'}).text.replace(
        "Original recipe yields", "").replace("servings", "")
    if "(" in servings:
        ind = servings.index("(")
        servings = int(servings[:ind].strip())
    else:
        servings = int(servings)
    return servings


def parse_cuisine(soup):
    cuisine = None
    breadcrumbs = soup.find('ol', {'class': 'breadcrumbs'})
    if breadcrumbs:
        for crumb in breadcrumbs.findAll('li'):
            poss_cuisine = crumb.find('span').text
            for cuis in CUISINES:
                if all([char in poss_cuisine for char in cuis]):
                    cuisine = cuis
    return cuisine


def parse_name(soup):
    name = soup.find("h1", {"id": "recipe-main-content"}).text
    return name.lower()

def print_information(recipe_obj):
    print("===============")
    print(recipe_obj.name.upper() + "\n")

    #print ingredients
    print("[INGREDIENTS]")
    for food in recipe_obj.ingredients:
        print(food)

    #print steps
    print("\n[STEPS]")
    count = 1
    for step in recipe_obj.directions:
        print("Step " + str(count) + ":", step)
        count += 1
    print("===============")

def more_verbose(recipe_obj):
    recipe_obj.print_recipe()
    print("\n")
    food_lst, food_name_lst, direc_lst, master_tools, master_methods = wrapper(recipe_obj.ingredients,recipe_obj.directions)

    #extract methods
    primary_methods = ['saute','sauté','broil','boil','fry','fried','poach','bake','roast']
    primary_methods_present = []
    secondary_methods_present = []
    for method in master_methods:
        if method in primary_methods:
            primary_methods_present.append(method)
        else:
            secondary_methods_present.append(method)
    print("Primary Methods Used: ", ", ".join(primary_methods_present))
    print("Secondary Methods Used: ", ", ".join(secondary_methods_present))

    #print tools
    print("Tools Used: ", ", ".join(master_tools))
    print("\n")
    print("Ingredients:")
    for food in food_lst:
        food.print_food()

    for direc in direc_lst:
        direc.print_dir()

    return


def main(url):
    website_url = requests.get(url).text
    soup = BeautifulSoup(website_url, 'lxml')
    groups, ingredients = parse_ingredients(soup)
    directions = parse_directions(soup)
    servings = parse_servings(soup)
    cuisine = parse_cuisine(soup)
    name = parse_name(soup)
    rp = recipe(name, groups, ingredients, directions, cuisine, servings)
    return rp


if __name__ == '__main__':
    print("Welcome to Recipe Transformer!!")
    case = '0'
    url = ''
    recipe_obj = None
    arr = ['0','1','2','3','4','5','6','7','8','9','10','-1']
    while case in arr:
        if case == '0':
            url = input('Enter Valid URL from AllRecipes: ')
            try:
                recipe_obj = main(url)
                print('\nPrinting Parsed Recipe...\n')
                print_information(recipe_obj)
                case = '-1'
                continue
            except:
                case = '0'
                print('URL was not valid...')
                continue
        if case == '-1':
            print('\nWhich transformation would you like to perform now?\n\nPlease enter the appropiate number...')
            print('\n1: Tranform to healthy\n2: Transform to unhealthy\n3: Transform to Vegetarian\n4: Transform to Non-Vegetarian\n5: Transform to Vegan\n6: Transform Amount\n7: Transform Cuisine Style\n8: Try a different recipe\n9: More Detailed Output\n10: Exit')
            case = input('Enter number here: ')
            if case not in arr:
                print('Invalid Input...\n')
                case = '-1'
                continue
        if case == '1':
            print('Printing Transformed Recipe...\n')
            recipe_obj = to_healthy(recipe_obj)
            print_information(recipe_obj)
            print('\nRecipe Transformed')
            case = '-1'
            continue
        if case == '2':
            print('Printing Transformed Recipe...\n')
            recipe_obj = from_healthy(recipe_obj)
            print_information(recipe_obj)
            print('\nRecipe Transformed')
            case = '-1'
            continue
        if case == '3':
            print('Printing Transformed Recipe...\n')
            #recipe_obj = vegetarian(recipe_obj)
            print_information(recipe_obj)
            print('\nRecipe Transformed')
            case = '-1'
            continue
        if case == '4':
            print('Printing Transformed Recipe...\n')
            #recipe_obj = vegetarian(recipe_obj)
            print_information(recipe_obj)
            print('\nRecipe Transformed')
            case = '-1'
            continue
        if case == '5':
            print('Printing Transformed Recipe...\n')
            #recipe_obj = vegetarian(recipe_obj)
            print_information(recipe_obj)
            print('\nRecipe Transformed')
            case = '-1'
            continue
        if case == '6':
            print('\nHow would you like to transform amount?')
            print('1: Double Serving Size\n2: Halve Serving Size\n3: Go Back')
            option = input('Enter number here: ')
            if option not in ['1','2','3']:
                print("Invalid Input...")
                continue
            if option == '1':
                case = '11'
            if option == '2':
                case = '12'
            if option == '3':
                case = '-1'
        if case == '7':
            print('\nHow would you like to transform cuisine?')
            print('1: Mexican\n2: Asian\n3: Indian\n4: Go Back')
            option = input('Enter number here: ')
            if option not in ['1','2','3','4']:
                print("Invalid Input...")
                continue
            if option == '1':
                case = '13'
            if option == '2':
                case = '14'
            if option == '3':
                case = '15'
            if option == '4':
                case = '-1'
        if case == '8':
            case = '0'
            continue
        if case == '9':
            print('Printing more detailed output...')
            more_verbose(recipe_obj)
            case = '-1'
        if case == '10':
            break
        if case == '11':
            print('Printing Transformed Recipe...\n')
            recipe_obj = double_amount(recipe_obj)
            print_information(recipe_obj)
            print('\nRecipe Transformed')
            case = '-1'
            continue
        if case == '12':
            print('Printing Transformed Recipe...\n')
            recipe_obj = half_amount(recipe_obj)
            print_information(recipe_obj)
            print('\nRecipe Transformed')
            case = '-1'
            continue
        if case == '13':
            print('Printing Transformed Recipe...\n')
            recipe_obj = transform_to_mexican(recipe_obj)
            print_information(recipe_obj)
            print('\nRecipe Transformed')
            case = '-1'
            continue
        if case == '14':
            print('Printing Transformed Recipe...\n')
            recipe_obj = transform_to_asian(recipe_obj)
            print_information(recipe_obj)
            print('\nRecipe Transformed')
            case = '-1'
            continue
        if case == '15':
            print('Printing Transformed Recipe...\n')
            recipe_obj = transform_to_indian(recipe_obj)
            print_information(recipe_obj)
            print('\nRecipe Transformed')
            case = '-1'
            continue
