import pandas as pd
from django.apps import AppConfig
from model.LogisticRegression import LogisticRegression


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    model_instance = None
    model_loaded = False

    def ready(self):
        if not AppConfig.model_loaded:
            data = pd.read_csv('data/train_dataset.csv')  # Replace with actual data source
            X = data[['SellerAuctionCount', 'SellerAuctionSaleCount']].values  # Adjust features
            y = data['is_fraud'].values  # Target variable

            # Create and train the model
            model = LogisticRegression(learning_rate=0.01, num_iterations=1000)
            model.fit(X, y)
            AppConfig.model_instance = model
            AppConfig.model_loaded = True  # Store the trained model
