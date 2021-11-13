from django.urls import path
from .views import AccountsReport

urlpatterns = [
    path('accounts_report', view=AccountsReport.as_view(), name="accounts_report"),
    path('accounts_report/<int:domain_id>/<str:format>',
         view=AccountsReport.as_view(),
         name="accounts_report")

]
