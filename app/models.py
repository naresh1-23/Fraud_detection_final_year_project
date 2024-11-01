from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    AUCTIONEER = "Auctioneer"
    BIDDER = "Bidder"
    USER_ROLES = (
        (AUCTIONEER,  AUCTIONEER),
        (BIDDER, BIDDER)
    )

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=USER_ROLES, default=BIDDER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    starting_price = models.PositiveIntegerField()
    bidding_ending_date = models.DateField(default=timezone.now)
    bidding_ending_time = models.TimeField(default=timezone.now)
    picture = models.FileField(upload_to='product/', null=True, blank=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="seller")
    is_sold = models.BooleanField(default=False)
    assigned_winner = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} {self.seller.email}"


class Bidding(BaseModel):
    price = models.PositiveIntegerField()
    bidder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bidder")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")

    def __str__(self) -> str:
        return f"{self.bidder.email} bids {self.product.name} with price {self.price}"


class BiddingWinner(BaseModel):
    bidding = models.ForeignKey(Bidding, on_delete=models.CASCADE)
    final_price = models.PositiveIntegerField()
    winning_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Winner: {self.bidding.bidder.email} won {self.bidding.product.name}"


class UserStatistics(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="statistics")
    total_item_listed = models.PositiveIntegerField(default=0)
    total_item_sold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} - Listed: {self.total_item_listed}, Sold: {self.total_item_sold}"
