from app.models import Product


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
