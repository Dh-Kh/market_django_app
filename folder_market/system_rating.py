from surprise import Dataset, SVD, Reader
import pandas as pd
from random import randint

def recommendation_func(request):
    reader = Reader()
    dataframe = pd.read_csv("dataset_rec.csv")
    dataset = Dataset.load_from_df(dataframe, reader)
    machine = SVD()
    machine.fit(dataset.build_full_trainset())
    random_data = randint(0, len(dataframe) - 1)
    prediction = machine.predict(request, random_data)
    return prediction.est

