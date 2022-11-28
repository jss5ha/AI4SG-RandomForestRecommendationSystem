import pandas as pd

df = pd.read_csv('data/epi_r.csv')

# removing unwanted features
to_drop = ['#cakeweek', '#wasteless', '22-minute meals', '3-ingredient recipes', '30 days of groceries', 'alabama', 'alaska', 'alcoholic', 'anniversary', 'anthony bourdain', 'arizona', 'atlanta', 'australia', 'back to school', 'backyard bbq', 'bastille day', 'beverly hills', 'birthday', 'blender', 'boil', 'bon appétit', 'bon app��tit', 'boston', 'brandy', 'buffet', 'bulgaria', 'california', 'cambridge', 'canada', 'chicago', 'chile', 'colorado', 'columbus', 'connecticut', 'cuba', 'dallas', 'date', 'denver', 'digestif', 'diwali', 'dominican republic', 'dorie greenspan', 'edible gift', 'egypt', 'emeril lagasse', 'engagement party', 'england', 'entertaining', 'epi + ushg', 'epi loves the microwave', 'fall', 'family reunion', 'flaming hot summer', 'florida', 'fourth of july', 'france',
           'friendsgiving', 'georgia', 'germany', 'graduation', 'haiti', 'halloween', 'hanukkah', 'hawaii', 'healdsburg', 'hollywood', 'houston', 'idaho', 'illinois', 'indiana', 'iowa', 'ireland', 'israel', 'italy', 'jamaica', 'japan', 'jerusalem artichoke', 'kansas', 'kansas city', 'kentucky', 'kentucky derby', 'kitchen olympics', 'labor day', 'las vegas', 'london', 'louisiana', 'louisville', 'maryland', 'massachusetts', 'mexico', 'miami', 'michigan', 'minneapolis', 'minnesota', 'mississippi', 'missouri', 'nancy silverton', 'nebraska', 'new hampshire', 'new jersey', 'new mexico', 'new orleans', 'new york', 'north carolina', 'ohio', 'oklahoma', 'oktoberfest', 'oregon', 'oscars', 'party', 'pasadena', 'pennsylvania', 'persian new year', 'peru', 'philippines', 'pittsburgh', 'portland', 'providence']

df.drop(to_drop, inplace=True, axis=1)
df = df[df['calories'].notna()]
df = df[df['protein'].notna()]
df = df[df['fat'].notna()]
df = df[df['sodium'].notna()]

df = df.drop_duplicates(subset=["title"])

df.to_csv("data/recipes.csv", encoding='utf-8', index=False)
