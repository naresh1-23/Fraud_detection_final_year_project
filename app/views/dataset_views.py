import pandas as pd
from django.core.paginator import Paginator
from django.shortcuts import render


def data_listing(request):
    df = pd.read_csv('data/train_dataset.csv')
    csv_data = df.to_dict(orient='records')

    # Paginate the data
    paginator = Paginator(csv_data, 500)  # Show 50 rows per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, "model_checking/data_listing.html", context)
