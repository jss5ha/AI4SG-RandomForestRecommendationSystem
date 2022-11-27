from sklearn.ensemble import RandomForestRegressor
import numpy as np


class RecommendationSystem():
    def __init__(self, rs, names):
        self.rs = rs
        self.names = names
        self.userRatings = [0.5] * rs.shape[0]
        self.rec_ed = []
        self.model.fit(self.rs, self.userRatings)

    def createModel(self):
        self.model = RandomForestRegressor(n_estimators=10, max_depth=3)
        self.userRatings = [0.5] * rs.shape[0]
        self.model.fit(self.rs, self.userRatings)

    def retrainModel(self, updatedRatings):
        count = 0
        for item in self.rec_idx_this_round:
            self.userRatings[item] = updatedRatings[count]
            count += 1
        self.model.fit(self.rs, self.userRatings)

    def rec(self, k, same=0):
        results = self.model.predict(self.rs)
        rec_rs = np.array(results).argsort()
        rec_idx = []

        if same == 1:
            rec_idx = rec_rs[-k:]
        else:
            for i in range(rec_rs.shape[0]):
                if rec_rs[rec_rs.shape[0]-1-i] not in self.rec_ed:
                    rec_idx.append(rec_rs[rec_rs.shape[0]-1-i])
                    self.rec_ed.append(rec_rs[rec_rs.shape[0]-1-i])
                if len(rec_idx) == k:
                    break

        self.rec_idx_this_round = rec_idx
        return np.array(self.names)[rec_idx]


def getRecommendations(userId, recipes):
    print(recipes)
    # names = df['title'].values.tolist()  # first column of the df
    # df.drop('title', inplace=True, axis=1)
    # rec_model = RecommendationSystem(rs, names)
    # while True:
    #     print("Then how many recipes do you want today?")
    #     the_k = int(input())
    #     rec_prediction = rec_model.rec(the_k, same)

    #     print("Success - We've got your recipe recommendations for today!")

    #     for i in range(the_k):
    #         print("Recipe " + str(i + 1) + ":")
    #         print(str(rec_prediction[i]))

    #     # ask user to rate
    #     print("Hope you enjoy your meals for today :)\n")
    #     print("Waiting for you to complete you meal...")
    #     print("How do you like the recommendations for today?")
    #     ratings = []

    #     for i in range(the_k):
    #         print("Please rate today's recipe " + str(i + 1) + " - " +
    #               str(rec_prediction[i]) + " (min = 0, max = 5):")
    #         ratings.append(float(int(input()) / 5))

    #     # update database
    #     rec_model.preference_update(ratings)

    #     # collect users' satisfaction level
    #     print("Please rate today's recommendation in general (min = 0, max = 100):")
    #     satis.append(input())
