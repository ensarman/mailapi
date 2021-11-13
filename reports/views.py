from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from sys_users.models import Company
from virtual.models import Domain

import csv
# Create your views here.


class AccountsReport(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        domain_id = self.kwargs.get('domain_id')
        if domain_id:

            request_user = self.request.user
            companies = request_user.domainadmin.company.all()
            request_domain = Domain.objects.get(id=domain_id)

            # validar que el dominio sea del usuario
            for company in companies:
                if request_domain not in company.domain.all():
                    raise Http404

            if self.kwargs.get('format') == 'csv':
                # creando el csv
                response = HttpResponse(
                    content_type='text/csv',
                    headers={
                        'Content-Disposition': 'attachment; filename="report.csv"'
                    },
                )
                writer = csv.writer(response)
                writer.writerow(
                    ['User', 'Domain', 'Quota Assigned', 'Quota Used', 'Quota %'])
                users = request_domain.user_set.all()
                for user in users:
                    writer.writerow(
                        [
                            user.email,
                            user.domain,
                            user.quota_gb(),
                            user.quota_used_gb,
                            user.quota_percent
                        ]
                    )

            return response
        else:
            raise Http404
