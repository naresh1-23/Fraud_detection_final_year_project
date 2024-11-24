import numpy as np
import pandas as pd
from datetime import datetime
from django.db.models import Q
import pytz
from app.apps import AppConfig
from app.models import Product, UserStatistics, Bidding, BiddingWinner
from model.LogisticRegression import LogisticRegression


class ProductService:

    @staticmethod
    def get_product(*args, **kwargs):
        try:
            return Product.objects.get(*args, **kwargs)
        except Product.DoesNotExist:
            return None

    @staticmethod
    def filter_product(*args, **kwargs):
        return Product.objects.filter(*args, **kwargs)

    @staticmethod
    def add_product(name, description, starting_price, date, time, picture, user):
        if name == "" or description == "" or starting_price == "" or date == "" or time == "" or picture == "":
            return False, "All fields are required", None
        product = Product.objects.create(
            name=name, description=description, starting_price=starting_price, bidding_ending_date=date,
            bidding_ending_time=time, picture=picture, seller=user)
        return True, "Product successfully addded", product

    @staticmethod
    def update_user_stats_item_listed(user):
        user_stats = UserStatistics.objects.filter(user=user).first()
        products = ProductService().filter_product(seller=user).values_list('starting_price', flat=True)
        prices = {"prices": products}
        df = pd.DataFrame(prices)
        median_price = df["prices"].median()
        if not user_stats:
            user_stats_create = UserStatistics.objects.create(
                user=user, total_item_listed=1, total_item_sold=0, median_auction_price=median_price)
            user_stats_create.save()
            print("created user stats")
        else:
            user_stats.total_item_listed += 1
            user_stats.median_auction_price = median_price
            user_stats.save()
            print("Updated user stats")

    @staticmethod
    def predict_fraud(user):
        user_stats = UserStatistics.objects.get(user=user)
        model = LogisticRegression(
            weights=np.array([-0.01716929, -0.09296037, 0.02588775, 0.04282618]),
            bias=-0.0031132521959794145)
        prediction = model.predict([[user_stats.total_item_listed, user_stats.total_item_sold,
                                   user_stats.median_auction_price, user_stats.total_item_returned]])
        print(prediction)
        print(user_stats.total_item_listed, user_stats.total_item_sold)
        return "Might be fraud" if prediction[0] == 1 else "This user is verified"

    @staticmethod
    def assign_winner():
        time_zone = pytz.timezone("Asia/Kathmandu")
        products = ProductService().filter_product(Q(bidding_ending_date__lt=datetime.now(time_zone), assigned_winner=False) | Q(
            bidding_ending_date=datetime.now(time_zone).date(), bidding_ending_time__lte=datetime.now(time_zone).time()), assigned_winner=False)
        for product in products:
            winner = Bidding.objects.filter(product=product, price=product.starting_price).first()
            if winner:
                bid_winner = BiddingWinner.objects.create(
                    bidding=winner, final_price=winner.price, winning_date=product.bidding_ending_date)
                bid_winner.save()
                product.assigned_winner = True
                product.save()
                print(f"Winner of {product.name} is {winner.bidder.email}")
