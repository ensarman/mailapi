from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date

# Create your views here.


class BanLog(LoginRequiredMixin, TemplateView):
    template_name = "logs/ban_log.html"

    def get_context_data(self, *args, **kwargs):
        context = context = super(BanLog, self).get_context_data(
            *args, **kwargs)

        context['day_log'] = []
        with open("/var/log/fail2ban.log", "r") as file:
            for line in file:
                log_date_string = line.split(" ")[0]
                log_date = {
                    'year': int(log_date_string.split("-")[0]),
                    'month': int(log_date_string.split("-")[1]),
                    'day': int(log_date_string.split("-")[2]),
                }
                line_date = date(
                    log_date['year'],
                    log_date['month'],
                    log_date['day']
                )
                if line_date == date.today():
                    context['day_log'] += [line.split()]
        return context
