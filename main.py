import requests
from lxml import html
from bs4 import BeautifulSoup
from parse import wrapper

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
        "Original recipe yields", "")
    if "(" in servings:
        ind = servings.index("(")
        servings_pan = servings[ind + 1:-1]
        servings_num = int(servings[:ind].replace("servings", "").strip())
        servings = [servings_num, servings_pan]
    else:
        servings = [servings]
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
    return name


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
    url = 'https://www.allrecipes.com/recipe/14746/mushroom-pork-chops/'
    recipe = main(url)
    ing_lst, step_lst = recipe.ingredients, recipe.directions
    wrapper(ing_lst, step_lst)
