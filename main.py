import requests
from lxml import html
from bs4 import BeautifulSoup


def parse_ingredients(soup):
    ingredients = []
    site_content = soup.find('div', {"class": "site-content"}).find('div', {"class": "container-content body-content"}). \
        find('div', {"class": "recipe-container-outer"}).find('section', {"class": "ar_recipe_index"}). \
        find('section', {"class": "recipe-ingredients"}).find('div', {'id': "polaris-app"})
    ingredient_list = site_content.find('ul', {'id': "lst_ingredients_1"}).findAll('li', {"class": "checkList__line"}) + \
                      site_content.find('ul', {'id': 'lst_ingredients_2'}).findAll('li', {"class": "checkList__line"})
    for ingredient in ingredient_list:
        t = ingredient.find(['span', 'p'])
        if t is not None:
            ing_text = t.text
            ingredients.append(ing_text)

    ingredients.remove("Add all ingredients to list")
    return ingredients


def parse_directions(soup):
    directions = []
    site_content = soup.find('div', {"class": "site-content"}).find('div', {"class": "container-content body-content"}). \
        find('div', {"class": "recipe-container-outer"}).find('section', {"class": "ar_recipe_index"}). \
        find('section', {"class": "recipe-directions"}).find('div', {'class': "directions--section"}).\
        find('div', {'class': "directions--section__steps"}).find('ol', {"class":"list-numbers"})
    direction_list = site_content.findAll('li', {'class':"step"})
    for step in direction_list:
        t = step.find(['span', 'p'])
        if t is not None:
            step_text = t.text
            directions.append(step_text.rstrip())

    return directions


def main(url):
    website_url = requests.get(url).text
    soup = BeautifulSoup(website_url, 'lxml')
    ingredients = parse_ingredients()
    directions = parse_directions(soup)
    return ingredients, directions


if __name__ == '__main__':
    print(main(
        'https://www.allrecipes.com/recipe/273326/parmesan-crusted-shrimp-scampi-with-pasta/?internalSource=previously%20viewed&referringContentType=Homepage&clickId=cardslot%202'))
