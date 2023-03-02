import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from joblib import Parallel, delayed
import spacy

try:
    nlp = spacy.load('en_core_web_lg')
except OSError:
    spacy.cli.download('en_core_web_lg')
    nlp = spacy.load('en_core_web_lg')

coffee = pd.read_csv('data/coffee_final.csv')

def similarity(coffee1, notes):
    sentence_1 = nlp(notes)
    sentence_2 = nlp(coffee1)
    return sentence_1.similarity(sentence_2)

def show_recommender_2(coffee, notes, no_rec):
    similarityValue = Parallel(n_jobs=-1,
                               backend="threading")(delayed(similarity)(coffee1, notes) for coffee1 in coffee['desc'])
    coffee['Similarity'] = similarityValue
    return coffee.sort_values(by='Similarity', ascending=False).loc[:, ['name', 'roaster', 'roaster_country',
                                                                        'origin_country', 'aroma', 'acid', 'body',
                                                                        'flavor', 'aftertaste', 'desc_1', 'desc_2',
                                                                        'desc_3']].head(no_rec)

def knn_recommender(coffee, taste_input):
    df = coffee.copy()
    taste_feature = df.loc[:,['aroma', 'acid', 'body', 'flavor', 'aftertaste']]
    neighbour_taste = NearestNeighbors(n_jobs=-1)
    neighbour_taste.fit(taste_feature)
    taste_index = neighbour_taste.kneighbors(taste_input, 50, return_distance=False)
    select_taste_index = np.reshape(taste_index,-1)
    return df.iloc[select_taste_index,:]

def main_recommender(notes, taste_input, origin=None, no_rec=3, coffee=coffee):
    df = coffee.copy()
    if origin:
        df = df[df['origin'].str.contains(origin, na=False)]
    coffee_filtered = knn_recommender(df, taste_input)
    final_recommender = show_recommender_2(coffee_filtered, notes, no_rec=no_rec)
    return final_recommender

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(main_recommender('juicy sweet bright fruity', [[5,2,8,5,9]]))



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
