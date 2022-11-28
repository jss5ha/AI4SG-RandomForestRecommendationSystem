class KnowledgeBasedFilter:
    def __init__(self, user, mealType=None):
        self.user = user
        self.mealType = mealType

    def filterByDietaryRestrictions(self, recipes):
        """Function for Removing Recipes Based on Dietary Restrictions and Returning an Updated List"""
        vegetarian = 524
        pescatarian = 354
        glutenFree = 542
        for restriction in self.user.dietaryRestrictions:
            if restriction == "vegetarian":
                indexToRemove = vegetarian
            elif restriction == "pescatarian":
                indexToRemove = pescatarian
            elif restriction == "gluten-free":
                indexToRemove = glutenFree
            else:
                raise Exception("Invalid User Dietary Restriction")
            index = 0
            while index != len(recipes):
                if recipes[index][indexToRemove] != 1:
                    recipes.remove(recipes[index])
                else:
                    index += 1
        return recipes

    def filterByNutrients(self, recipes, requiredCalories, requiredProtein, requiredFat):
        """Function for Removing Recipes Based on Calories, Protein, and Fat Content and Returning an Updated List"""
        index = 0
        while index < len(recipes):
            thisRecipe = recipes[index]
            removed = False
            if float(thisRecipe[2]) > requiredCalories + 100 or float(thisRecipe[2]) < requiredCalories - 100:
                recipes.remove(thisRecipe)
                removed = True
            if (float(thisRecipe[3]) > requiredProtein + 15 or float(thisRecipe[3]) < requiredProtein - 15) and not removed:
                recipes.remove(thisRecipe)
                removed = True
            # if (float(thisRecipe[4]) > requiredFat + 15 or float(thisRecipe[4]) < requiredFat - 15) and not removed:
            #     recipes.remove(thisRecipe)
            #     removed = True
            if not removed:
                index += 1
        return recipes

    def getRequiredCalories(self):
        """Calculates Calories Needed for this Meal and Returns it"""
        if self.user.gender == 'female':
            BMR = 655 + (9.6 * int(self.user.weight)) + (
                1.8 * int(self.user.height)) - (4.7 * int(self.user.age))
        else:
            BMR = 66 + (13.7 * int(self.user.weight)) + (
                5 * int(self.user.height)) - (6.8 * int(self.user.age))

        if self.user.activityLevel == 'sedentary':
            activityMultiplier = 1.2
        elif self.user.activityLevel == 'lightly active':
            activityMultiplier = 1.375
        elif self.user.activityLevel == 'moderately active':
            activityMultiplier = 1.55
        elif self.user.activityLevel == 'very active':
            activityMultiplier = 1.725
        elif self.user.activityLevel == 'extremely active':
            activityMultiplier = 1.9

        TDEE = BMR * activityMultiplier

        if self.user.goal == 'gain weight':
            TDEE += 300
        elif self.user.goal == 'lose weight':
            TDEE *= .8
        elif self.user.goal == 'maintain weight':
            TDEE = TDEE

        requiredCalories = TDEE * (1 / 3)

        return requiredCalories

    def getRequiredProtein(self):
        """Calculates Amount of Protein Needed for Day and Returns that Value/3"""
        requiredProtein = .8 * int(self.user.weight) / 3
        return requiredProtein

    def getRequiredFat(self, requiredCalories):
        """Calculates Amount of Fat Needed for Day and Returns that Value/3"""
        requiredFat = (requiredCalories * .35) / 27
        return requiredFat

    def getFilteredRecipes(self, recipes):
        requiredCalories = self.getRequiredCalories()
        requiredProtein = self.getRequiredProtein()
        requiredFat = self.getRequiredFat(requiredCalories)
        recipes = self.filterByDietaryRestrictions(recipes)
        recipes = self.filterByNutrients(
            recipes, requiredCalories, requiredProtein, requiredFat)
        return recipes
