from django.contrib import admin
from .models import *


admin.site.register(StockModel)
admin.site.register(StockPortfolioModel)
admin.site.register(DiaryPostModel)
admin.site.register(HistoryModel)