from user import User
from knowledgeBasedFilter import KnowledgeBasedFilter
from recommendationSystem import RecommendationSystem
import pandas as pd
import pickle
import os


def getUser():
    userId = input("Please enter user id: ").lower()
    user = User(userId)
    return user


def getFilteredRecipes():
    recipes = pd.read_csv('data/recipes.csv').values.tolist()
    knowledgeBasedFilter = KnowledgeBasedFilter(user)
    filteredRecipes = knowledgeBasedFilter.getFilteredRecipes(recipes)
    filteredRecipesDataFrame = pd.DataFrame(filteredRecipes)
    return filteredRecipesDataFrame


def showRecommendations(userId):
    recommendSameRecipes = True
    recommendedRecipes = []
    allRatings = []
    dayCount = 1
    print("\nYou will be given recommendations for 24 days.")
    while dayCount <= 24:
        while True:
            recommendedRecipes = recommendationSystem.getRecommendations(
                recommendSameRecipes)

            print(
                f"\nSuccess - We've got your recipe recommendations for day {dayCount}!")
            for idx, recipe in enumerate(recommendedRecipes):
                print(f"({idx+1}) {recipe}")

            if input("\nWould you like to proceed with these recipes? [y/n] ").lower() == "y":
                break
            else:
                recommendSameRecipes = False

        # ask user to rate
        print("\nHope you enjoy your meals for today :)\n")
        ratings = []

        for idx, recipe in enumerate(recommendedRecipes):
            rating = input(
                f"Please rate today's recipe - {recipe} (min = 0, max = 5): ")
            while not str(rating).isnumeric() or int(rating) < 0 or int(rating) > 5:
                print("Invalid rating")
                rating = input(
                    f"Please rate today's recipe - {recipe} (min = 0, max = 5): ")
            ratings.append(int(rating) / 5)

        allRatings.extend(ratings)

        # update model
        recommendationSystem.retrainModel(ratings)

        if dayCount % 3 == 0:
            print(
                "\nPlease take the survey: https://virginia.az1.qualtrics.com/jfe/form/SV_9oi2R7WEZb6tF9c")

        dayCount += 1

    allRatingsPath = f"user_recipe_ratings/{userId}.pickle"
    pickle.dump(allRatings, open(allRatingsPath, "wb"))


def getUserSatisfactionRatings(userId):
    overallRatingsPath = f"user_satisfaction_ratings/{userId}.pickle"
    if os.path.isfile(overallRatingsPath):
        satisfactionScores = pickle.load(
            open(overallRatingsPath, "rb"))
    else:
        satisfactionScores = []
    satisfactionScores.append(int(
        input("\nPlease rate today's recommendation in general (min = 0, max = 100): ")))
    pickle.dump(satisfactionScores, open(overallRatingsPath, "wb"))


if __name__ == "__main__":
    user = getUser()
    print("\n[USER STATS]")
    print(user, "\n")

    filteredRecipesDataFrame = getFilteredRecipes()
    print(f"Total available recipes: {filteredRecipesDataFrame.shape[0]}")

    recommendationSystem = RecommendationSystem(
        user.userId, filteredRecipesDataFrame)

    showRecommendations(user.userId)
    recommendationSystem.save()
    # collect user's overall satisfaction level
    getUserSatisfactionRatings(user.userId)
