# Recipes
COMP_SCI 337 Project #2
Authors: Saubhagya Shrestha, Emily Jenkins, Anu Raife

To run our recipe transformer, please run main.py.

The user is presented with an interface where s/he is welcomed to the
transformer and prompted to input a recipe URL from AllRecipes.com.
There is then a list of options to choose from: Transform to unhealthy,
to healthy, to vegetarian, to non-vegetarian, to vegan, Transform Amount
(double amount and cut in half), Transform Cuisine (Mexican, Asian, Indian,
Greek), to test a different recipe, or to view a more detailed/verbose output.

In the more verbose output, the user can see each of the ingredients parsed out,
listing name, quantity/measurement, descriptors, and preparation. For each step,
the user can see the actual direction as well as the ingredients, cooking methods,
tools, and time involved in the step.

To healthy...

To unhealthy...

To vegetarian...

To non-vegetarian...

To vegan...

Transform amount...

Transform cuisine takes a recipe object and transforms it to a new style of cuisine.
The user can transform their recipe to Mexican, Asian, Indian, or Greek cuisines.

PLEASE NOTE: Mexican is our required style for the transform cuisine requirement;
it is much more comprehensive since it was a required element, so we would like that
one to be graded as our required cuisine transformation.

  - Mexican (REQUIRED): if the dish is a casserole, the program keeps it as a casserole
    and adds beans, salsa, sour cream, and Mexican seasoning to the dish. If the dish
    is not a casserole and contains meat, it is made into tacos (served with rice on them
    if a starch like pasta, rice, etc is included). If the dish does not have meat but
    is a starch (such as pasta, rice, potatoes, etc), it is made into a rice dish. If there
    are key ingredients identified in the recipe, the dish becomes a Mexican rice with
    these key ingredients incorporated (ex. spinach tomato tortellini becomes Mexican
    rice with spinach and tomato included). If there are no identifiable ingredients
    (a function that we wrote), the dish is simply converted into rice with Mexican
    seasoning added. If there is no meat or starch (likely a vegetable), Mexican seasoning
    is added to the dish. If it is a soup, the program transforms it into an enchilada
    soup with any meats and vegetables pulled from the original soup recipe. If the
    recipe is a dessert, the program makes either a churro (for more pastry-like desserts)
    or a flan, with the key ingredients incorporated in (ex: key lime pie becomes a key
    lime flan). All dishes are served with beans, salsa, and sour cream on the side
    (excluding soups and desserts).

  - Asian (OPTIONAL): If the dish is a dessert, it makes an Asian rice pudding with key
    ingredients incorporated in (ex: chocolate chip cookies would become chocolate-flavored
    rice pudding). If the dessert is a soup, the recipe is transformed into Ginger Garlic
    Noodle Soup with Bok Choy, with any meat or vegetables from the original recipe
    incorporated. Otherwise, the dish is turned into a stir-fry, with any other meats or
    vegetables added to the dish.

  - Indian (OPTIONAL): If the dish is a dessert, it makes an Indian Vermicelli Pudding with key
    ingredients incorporated in (ex: chocolate chip cookies would become chocolate-flavored
    vermicelli pudding). If the dessert is a soup, the recipe is transformed into Indian
    Mulligatawny Soup, with any meat or vegetables from the original recipe
    incorporated. Otherwise, the dish is turned into a curry, with any other meats or
    vegetables added to the dish.

  - Greek (OPTIONAL): If the dish is a dessert, it makes a traditional Greek Galaktoboureko
    dessert with key ingredients incorporated in (ex: chocolate chip cookies would become
    chocolate-flavored Galaktoboureko). If the dessert is a soup, the recipe is transformed
    into Pasta Fagoli Soup, with any meat or vegetables from the original recipe
    incorporated. Otherwise, the dish is turned into Spinach and Feta Pita Breads, with any
    other meats or vegetables added to the dish.
