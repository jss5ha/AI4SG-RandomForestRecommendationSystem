from sklearn.ensemble import RandomForestRegressor
import numpy as np
import os
import pickle


class RecommendationSystem():
    def __init__(self, userId, recipesDataFrame):
        self.recipeNames = recipesDataFrame[0].values.tolist()
        recipesDataFrame.drop(0, inplace=True, axis=1)
        self.vectorizedRecipes = recipesDataFrame.to_numpy()
        self.numberOfRecipes = self.vectorizedRecipes.shape[0]
        self.modelPath = f"user_models/{userId}.pickle"
        self.setModelAndRatings()
        self.recommendedRecipesIdxSoFar = set()
        self.recentRecommendedRecipesIdx = []

    def setModelAndRatings(self):
        if os.path.isfile(self.modelPath):
            self.model = pickle.load(open(self.modelPath, "rb"))
            self.ratings = self.model.predict(self.vectorizedRecipes)
        else:
            self.model = RandomForestRegressor(n_estimators=10, max_depth=3)
            self.ratings = [0.5] * self.numberOfRecipes
            self.model.fit(self.vectorizedRecipes, self.ratings)

    def retrainModel(self, updatedRatings):
        count = 0
        for item in self.recentRecommendedRecipesIdx:
            self.ratings[item] = updatedRatings[count]
            count += 1
        self.model.fit(self.vectorizedRecipes, self.ratings)

    def getRecommendations(self, recommendSameRecipes=False):
        recipeRatingPredictions = self.model.predict(self.vectorizedRecipes)
        sortedRecipesIdx = np.array(recipeRatingPredictions).argsort()
        newRecommendedRecipesIdx = []

        if recommendSameRecipes == True:
            newRecommendedRecipesIdx = sortedRecipesIdx[-min(
                3, sortedRecipesIdx.shape[0]):]
        else:
            for i in range(sortedRecipesIdx.shape[0]):
                if sortedRecipesIdx[sortedRecipesIdx.shape[0]-1-i] not in self.recommendedRecipesIdxSoFar:
                    newRecommendedRecipesIdx.append(
                        sortedRecipesIdx[sortedRecipesIdx.shape[0]-1-i])
                    if len(newRecommendedRecipesIdx) == 3:
                        break

        self.recommendedRecipesIdxSoFar.update(newRecommendedRecipesIdx)

        self.recentRecommendedRecipesIdx = newRecommendedRecipesIdx
        return np.array(self.recipeNames)[newRecommendedRecipesIdx]

    def save(self):
        pickle.dump(self.model, open(self.modelPath, "wb"))
