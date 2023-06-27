from surprise import Dataset, SVD, Reader
from .models_for import RatingStorage
import numpy as np
import pandas as pd
from random import randint

def getting_rating_data():      
    rating_storage = RatingStorage.objects.all()
    list_of_data = []
    for rs in rating_storage:
        list_of_data.append([rs.id_connector.name, rs.unique_user, rs.rating_storage])
    np_name = []
    np_user = []
    np_rating = []
    for ls in list_of_data:
        name, user_data ,rating_data = ls
        np_name.append(name)
        np_user.append(user_data)
        np_rating.append(rating_data)
    np_name = np.array(np_name)
    np_user = np.array(np_user)
    np_rating = np.array(np_rating)
    return np_name, np_user ,np_rating        



def recommendation_func(request):
    reader = Reader()
    dataframe = pd.read_csv("dataset_rec.csv")
    dataset = Dataset.load_from_df(dataframe, reader)
    machine = SVD()
    machine.fit(dataset.build_full_trainset())
    random_data = randint(0, len(dataframe) - 1)
    prediction = machine.predict(request, random_data)
    return prediction.est

