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
            match restriction:
                case "vegetarian":
                    indexToRemove = vegetarian
                case "pescatarian":
                    indexToRemove = pescatarian
                case "gluten-free":
                    indexToRemove = glutenFree
                case _:
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
            if (float(thisRecipe[4]) > requiredFat + 15 or float(thisRecipe[4]) < requiredFat - 15) and not removed:
                recipes.remove(thisRecipe)
                removed = True
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

        match self.user.activityLevel:
            case 'sedentary':
                activityMultiplier = 1.2
            case 'lightly active':
                activityMultiplier = 1.375
            case 'moderately active':
                activityMultiplier = 1.55
            case 'very active':
                activityMultiplier = 1.725
            case 'extremely active':
                activityMultiplier = 1.9

        TDEE = BMR * activityMultiplier

        match self.user.goal:
            case 'gain weight':
                TDEE += 300
            case 'lose weight':
                TDEE *= .8
            case 'maintain weight':
                TDEE = TDEE

        requiredCalories = TDEE * (4 / 12)

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
