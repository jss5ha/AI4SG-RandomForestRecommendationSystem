from user import User
from knowledgeBasedFilter import KnowledgeBasedFilter
from recommendationSystem import RecommendationSystem
import pandas as pd
import pickle
import os


def getMealType():
    mealType = input(
        'What kind of meal are you looking for? (breakfast, lunch, dinner) ').lower()
    while mealType not in ['breakfast', 'lunch', 'dinner']:
        print("Invalid Meal Type")
        mealType = input(
            'What kind of meal are you looking for? (breakfast, lunch, dinner) ').lower()
    return mealType


def getUser():
    userId = input("Please enter user id: ").lower()
    user = User(userId)
    return user


def getFilteredRecipes():
    recipes = pd.read_csv('data/recipes.csv').values.tolist()
    mealType = getMealType()
    knowledgeBasedFilter = KnowledgeBasedFilter(user, mealType)
    filteredRecipes = knowledgeBasedFilter.getFilteredRecipes(recipes)
    filteredRecipesDataFrame = pd.DataFrame(filteredRecipes)
    return filteredRecipesDataFrame


def showRecommendations():
    k = int(input("\nHow many recipes do you want? "))
    samePreference = input(
        "\nDo you want to try some different recipes? [yes / no] ")
    recommendSameRecipes = False if samePreference == "yes" else True

    recommendedRecipes = recommendationSystem.getKRecommendations(
        k, recommendSameRecipes)

    print("\nSuccess - We've got your recipe recommendations!")
    for idx, recipe in enumerate(recommendedRecipes):
        print(f"({idx+1}) {recipe}")

    # ask user to rate
    print("\nHope you enjoy your meals for today :)\n")
    ratings = []

    for idx, recipe in enumerate(recommendedRecipes):
        ratings.append(
            int(input(f"Please rate today's recipe - {recipe} (min = 0, max = 5): ")) / 5)

    # update model
    recommendationSystem.retrainModel(ratings)


def getUserSatisfactionRatings(userId):
    overallRatingsPath = f"user_satisfaction_ratings/{userId}.pickle"
    if os.path.isfile(overallRatingsPath):
        satisfactionScores = pickle.load(
            open(overallRatingsPath, "rb"))
    else:
        satisfactionScores = []
    satisfactionScores.append(int(
        input("Please rate today's recommendation in general (min = 0, max = 100): ")))
    pickle.dump(satisfactionScores, open(overallRatingsPath, "wb"))


if __name__ == "__main__":
    user = getUser()
    print("\n[USER STATS]")
    print(user, "\n")

    filteredRecipesDataFrame = getFilteredRecipes()
    print(f"Total available recipes: {filteredRecipesDataFrame.shape[0]}")

    recommendationSystem = RecommendationSystem(
        user.userId, filteredRecipesDataFrame)

    while True:
        showRecommendations()
        exitLoop = False if input(
            "\nWould you like to continue [yes/no] ").lower() == "yes" else True
        if exitLoop:
            recommendationSystem.save()
            # collect user's overall satisfaction level
            getUserSatisfactionRatings(user.userId)
            break
