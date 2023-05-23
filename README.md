# market_django_app
## Project Overview
This is the Django Market project, which allows users to start trading as salesmen or search for desired items as anonymous users. The app includes a rating system for salesmen, where users can evaluate their experience. Additionally, the project features categories of products that can be scaled as needed. Users have the option to add items to their basket and remove them. Moreover, users have a personal cabinet if they wish to become a salesman, which includes statistical data.

Furthermore, the project offers the ability to search for desired items using the Levenshtein string matching algorithm. This algorithm allows the program to check the product's category based on the installed dataframe. Users can also add their own dataframes to scale the categories of products.

Finally, the project incorporates a recommendation system using the Surprise library. Users can customize the recommendation system according to their preferences.
## Installation
```
pip install git+https://github.com/Dh-Kh/market_django_app.git
```
P.S. For the app to work properly, you need to set up an .env file and define your own sensitive data, such as email credentials and secret keys. if you want to dockerize a program the application has a dockerfile.

