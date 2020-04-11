import json
import random
import time
from datetime import datetime

import requests
from secret import edamam_app_id, edamam_app_key


class RecipePicker:
    def __init__(self):
        pass

    def key_ingredients_req(self):
        """Request key ingredients from user"""

        q = input("Enter keywords for the desired recipe (e.g. chicken, mushroom): ")
        return ("q=" + q)

    def calorie_req(self):
        """Request calorie range from user"""

        is_calorie = input("Do you want to add a calorie range? (y or n): ")
        if (is_calorie == "y"):
            calories = input("Enter calorie range (e.g 500-700): ")
            return ("&calories=" + calories)
        else:
            return("")

    def random_recipe_index(self):
        """Generates a random number for the recipe"""

        r_from = random.randint(0, 99)
        r_to = r_from + 1
        return ("&from=" + str(r_from) + "&to=" + str(r_to))

    def health_dict(self, choice):
        """Dictionary containing health requirements"""

        option = {
            0: "vegan",
            1: "vegetarian",
            2: "sugar-conscious",
            3: "peanut-free",
            4: "tree-nut-free",
            5: "alcohol-free",
        }

        return option.get(choice, "")

    def diet_dict(self, choice):
        """Dictionary containing dietary requirements"""

        option = {
            0: "balanced",
            1: "high-protein",
            2: "low-fat",
            3: "low-carb",
        }

        return option.get(choice, "")

    def health_req(self):
        """Request health filters from the user"""

        print("Health options:")
        print("0. vegan  1. vegetarian  2. sugar-conscious  3. peanut-free  4. tree-nut-free  5. alcohol-free  6. none")
        health_option = int(input("Please enter a health option from above (e.g. enter 0 for vegan): "))
        health = ""

        if health_option != 6:
            health = "&health=" + self.health_dict(health_option)
            while (health_option != 6):
                health_option = int(input("If you would like to select any other health options from above, enter their respective number: "))
                if health_option != 6:
                    health = health + "&health=" + self.health_dict(health_option)

            return health
        else:
            return health

    def diet_req(self):
        """Request dietary filters from the user"""

        print("Diet options:")
        print("0. balanced  1. high protein  2. low-fat  3. low-carb  4. none")
        diet_option = int(input("Please enter a dietary options from above (e.g. enter 1 for high protein): "))
        diet = ""

        if diet_option != 4:
            diet = "&diet=" + self.diet_dict(diet_option)
            while (diet_option != 4):
                diet_option = int(input("If you would like to select any other dietary options from above, enter their respective number: "))
                if diet_option != 4:
                    diet = diet + "&health=" + self.diet_dict(diet_option)

            return diet
        else:
            return diet

    def user_input(self):
        """asks for users input regarding recipe"""

        # builds GET request
        query = "https://api.edamam.com/search?&" + self.key_ingredients_req() + self.random_recipe_index() + self.calorie_req() + "&app_id=" + edamam_app_id + "&app_key=" + edamam_app_key + self.health_req() + self.diet_req()
        return query

    def pick_recipe(self):
        # form api request here

        response = requests.get(self.user_input())
        # number of recipes
        count = response.json()['count']
        recipe_name = (response.json()['hits'][0])['recipe']['label']
        ingredient_list = (response.json()['hits'][0])['recipe']['ingredientLines']
        recipe_url = (response.json()['hits'][0])['recipe']['url']

        if (count > 0):
            print("\nRecipe:")
            print("recipe name: " + recipe_name + "\n")
            print("ingredient list:")
            for i in ingredient_list:
                print("\t" + i)

            print("\nrecipe website: " + recipe_url)
        else:
            print("no recipes available")

        #uncomment to print entire json response
        #print(json.dumps(response.json(), sort_keys=True, indent=4))

if __name__ == '__main__':
    random.seed(datetime.now())
    rs = RecipePicker()
    rs.pick_recipe()
