from django.contrib import admin
from .models import *


admin.site.register(StockModel)
admin.site.register(StockPortfolioModel)
admin.site.register(UniqUserStockModel)
admin.site.register(DiaryPostModel)
