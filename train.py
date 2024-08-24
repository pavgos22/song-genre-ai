import pandas as pd
from bayes import Bayes
import pickle

database = pd.read_csv("csv/training_database_v36.csv")
data = Bayes(database)
data.serialize_dictionaries('data/compressed_data.json.gz')
with open("instance.pickle", "wb") as file:
    pickle.dump(data, file)
