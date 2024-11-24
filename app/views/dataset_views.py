import pandas as pd
import numpy as np
from django.core.paginator import Paginator
from django.shortcuts import render

from model.LogisticRegression import LogisticRegression


def data_listing(request):
    df = pd.read_csv('data/train_dataset.csv')
    csv_data = df.to_dict(orient='records')

    # Paginate the data
    paginator = Paginator(csv_data, 500)  # Show 50 rows per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, "model_checking/data_listing.html", context)


def predict_model(request):
    model = LogisticRegression(
        weights=np.array([-0.01716929, -0.09296037, 0.02588775, 0.04282618]),
        bias=-0.0031132521959794145)
    if request.method == "POST":
        median_price = float(request.POST["median_price"])
        sales_count = int(request.POST["sales_count"])
        item_listed = int(request.POST["item_listed"])
        return_count = int(request.POST["return_count"])
        prediction = model.predict([[item_listed, sales_count, median_price, return_count]])
        result = "Might be fraud" if prediction else "Might not be fraud"
        return render(request, "model_checking/predict_model.html", {"result": result})
    return render(request, "model_checking/predict_model.html")
