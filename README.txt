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

To healthy takes a recipe object and transforms it to a healthier version of it while 
still trying to maintain the overall flavor of the recipe. The function first identifies 
meat and substitutes it with chicken breasts for meats that are identified as 'unhealthy' 
(such as beef, pork, vension, etc). If fish, turkery, or chicken is encountered, no 
substitutions are made. The function will also make common healthy substitutions such as 
'extra-virgin olive oil' for 'vegetable oil' and 'egg whites' for 'eggs'. The function also 
runs through and identifies specific ingredients to cut by half or fourth, some of these items
include butter, salt, sugar, oil, cheeese, and cream. The function will add 'whole wheat' to 
foods such as flour, rice, and bread, add 'low fat' to foods like milk, and cream, add 
'low sodium' to foods like soy sauce. The function will also change any frying cooking methods 
to saute. If meat was detected before-hand, a step will be added to trim the fat and skin off 
the meat. Finally, the function will increase the serving size so the serving portion is reduced.

To unhealthy takes a recipe object and transforms it to a unhealthy version of it. It does this 
by increasing the amount of commonly known 'unhealthy' foods such as salt, sugar, butter, oil etc.
Substitutions for foods are also made. For example, 'eggs' is substituted for 'egg whites' and 'cream'
will be substituted for 'yogurt'. Along with this, foods that contain healthy descripters such as 
'whole grain' or 'low fat' or 'lean' are turned to regular version of those foods (without the 
'whole grain' and 'low fat' for example). The function will also turn any sauteing cooking methods 
to frying and decreasing the serving size so the serving portion is increased.

To vegetarian...

To non-vegetarian...

To vegan...

Transform amount can either double the amount of food or cut it in half.
    - Double: the function will go through and double the amount of each of the ingredients.
      The change for this is also echoed through the directions. For example, if the recipe
      called for 2 cups of flour, it will double it to 4 cups of flour in the ingredient list 
      and also change instances of 2 cups in the direction to 4 cups. This function will also 
      change all of the cooking utensils such as pots, pans, skillets etc. to a large size. If
      the size was already large before-hand, then it is not modified. It will increase the
      size of baking-pans if it is referenced in terms of dimensions (change 9x13 to 18x13).
      The serving size is also doubled so the serving potion is consistent.

    - Half: the function will go through and halve the amount of each of the ingredients.
      The change for this is also echoed through the directions. For example, if the recipe
      called for 4 cups of flour, it will halve it to 2 cups of flour in the ingredient list 
      and also change instances of 4 cups in the direction to 2 cups. This function will also 
      change all of the cooking utensils such as pots, pans, skillets etc. to a small size. If
      the size was already small before-hand, then it is not modified. It will decrease the
      size of baking-pans if it is referenced in terms of dimensions (change 18x13 to 9x13).
      The serving size is also halved so the serving potion is consistent.

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
