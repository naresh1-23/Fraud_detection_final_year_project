import pandas as pd
from django.apps import AppConfig
from model.LogisticRegression import LogisticRegression


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
