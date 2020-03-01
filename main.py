import requests
from lxml import html
from bs4 import BeautifulSoup
from parse import wrapper, extract_food_info
from transform_vegetarian import vegetarian
from transform_healthy import to_healthy, from_healthy
from get_key_ingredient import get_key
from transform_amount import double_amount, half_amount
from transform_cuisine import transform_cuisine as transform_to_mexican
from transform_asian import transform_cuisine_asian as transform_to_asian

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
        print("Name: ", self.name)
        if self.ingredient_groups:
            print("Ingredient groups: ", self.ingredient_groups)
        if self.ingredients:
            print("Ingredients: ", self.ingredients)
        if self.directions:
            print("Directions: ", self.directions)
        if self.cuisine:
            print("Cuisine: ", self.cuisine)
        if self.servings:
            print("Servings: ", self.servings)
        print('\n\n')


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
    arr = ['0','1','2','3','4','5','6','7','8','9','10','11','12']
    while case in arr:
        if case == '0':
            url = input('Enter Valid URL from AllRecipes: ')
            try:
                recipe_obj = main(url)
                print('\nPrinting parsed Recipe...')
                #print_recipe_obj(recipe)
                case = '12'
                continue
            except:
                case = '0'
                print('URL was not valid...')
                continue
        if case == '12':
            print('\nWhich transformation would you like to perform now?\n\nPlease enter the appropiate number...')
            print('\n1: Tranform to healthy\n2: Transform to unhealthy\n3: Transform to Vegetarian\n4: Transform to Non-Vegetarian\n5: Transform to Vegan\n6: Make it for double the people\n7: Make it for half the people\n8: Transform to Mexican Style\n9: Transform to Asian Stylye\n10: Try a differnt recipe\n11: Exit')
            case = input('Enter number here: ')
            if case not in arr:
                print('Invalid Input...\n')
                case = '12'
                continue
        if case == '1':
            print('Printing Transformed Recipe...\n')
            to_healthy(recipe_obj)
            print('\nRecipe Transfomed')
            case = '12'
            continue
        if case == '2':
            print('Printing Transformed Recipe...\n')
            from_healthy(recipe_obj)
            print('\nRecipe Transfomed')
            case = '12'
            continue
        if case == '3':
            print('Printing Transformed Recipe...\n')
            vegetarian(recipe_obj)
            print('\nRecipe Transfomed')
            case = '12'
            continue
        if case == '4':
            print('Printing Transformed Recipe...\n')
            vegetarian(recipe_obj)
            print('\nRecipe Transfomed')
            case = '12'
            continue
        if case == '5':
            print('Printing Transformed Recipe...\n')
            vegetarian(recipe_obj)
            print('\nRecipe Transfomed')
            case = '12'
            continue
        if case == '6':
            print('Printing Transformed Recipe...\n')
            double_amount(recipe_obj)
            print('\nRecipe Transfomed')
            case = '12'
            continue
        if case == '7':
            print('Printing Transformed Recipe...\n')
            half_amount(recipe_obj)
            print('\nRecipe Transfomed')
            case = '12'
            continue
        if case == '1':
            print('Printing Transformed Recipe...\n')
            to_healthy(recipe_obj)
            print('\nRecipe Transfomed')
            case = '12'
            continue
        if case == '8':
            print('Printing Transformed Recipe...\n')
            transform_to_mexican(recipe_obj)
            print('\nRecipe Transfomed')
            case = '12'
            continue
        if case == '9':
            print('Printing Transformed Recipe...\n')
            transform_to_asian(recipe_obj)
            print('\nRecipe Transfomed')
            case = '12'
            continue
        if case == '10':
            case = '0'
            continue
        if case == '11':
            break
