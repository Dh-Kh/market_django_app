import pandas as pd
from folder_market.models_for import RatingStorage
import numpy as np


class UserMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.counter = 0
        
    def __call__(self, request):
        self.counter += 1
        if self.counter >= 100000:
              
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
            dataframe = pd.DataFrame()
            dataframe["user"] = np_user
            dataframe["name"] = np_name
            dataframe["rating"] = np_rating
            dataframe.to_csv("dataset_rec.csv", index=False)
            self.counter = 0
            
            
        response = self.get_response(request)
        return response

