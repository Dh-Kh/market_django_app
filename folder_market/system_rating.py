from surprise import Dataset, Reader
import pandas as pd
from surprise import SVD
from django.contrib.auth import get_user_model
from .models_for import Item_info, RatingStorage

all_users = get_user_model().objects.values("username")  
all_items = Item_info.objects.values("item_id")
all_rating = RatingStorage.objects.values("rating_storage")


def recommendation_func(request):
    rating_data = {
        "item": [user["username"] for user in all_users].extend([]),
        "user": [[item["item_id"] for item in all_items]].extend([]),
        "rating": [rating["rating_storage"] for rating in all_rating],
    }
    pandas_rating = pd.DataFrame(rating_data)
    reader = Reader()
    data = Dataset.load_from_df(pandas_rating, reader)
    algo = SVD()
    algo.fit(data.build_full_trainset())
    
    pre_user = request
    pre_id = 1
    prediction = algo.predict(pre_user, pre_id)
    return prediction.est

