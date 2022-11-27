from user import User
from knowledgeBasedFilter import KnowledgeBasedFilter
from recommendationSystem import RecommendationSystem
import pandas as pd


def getMealType():
    mealType = input(
        'What kind of meal are you looking for? (breakfast, lunch, dinner) ').lower()
    while mealType not in ['breakfast', 'lunch', 'dinner']:
        print("Invalid Meal Type")
        mealType = input(
            'What kind of meal are you looking for? (breakfast, lunch, dinner) ').lower()
    return mealType


if __name__ == "__main__":
    usersDataFrame = pd.read_csv("data/user_data.csv")
    recipes = pd.read_csv('data/recipes.csv').values.tolist()

    userId = input("Please enter user id: ").lower()
    user = User(userId)
    print(user)

    mealType = getMealType()

    knowledgeBasedFilter = KnowledgeBasedFilter(user, mealType)
    filteredRecipes = knowledgeBasedFilter.getFilteredRecipes(recipes)

    recommendationSystem = RecommendationSystem()
    recommendationSystem.getRecommendations(user.userId, filteredRecipes)
