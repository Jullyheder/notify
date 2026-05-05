from django.contrib import admin
from django.urls import path
from webhooks.views import WebhooksOrderView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/webhooks/order/', WebhooksOrderView.as_view(), name='webhooks-order'),
]
