from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from file_read_backwards import FileReadBackwards

# Create your views here.


class BanLog(LoginRequiredMixin, TemplateView):
    template_name = "logs/ban_log.html"

    def get_context_data(self, *args, **kwargs):
        context = context = super(BanLog, self).get_context_data(
            *args, **kwargs)

        context['day_log'] = []
        with FileReadBackwards("/var/log/fail2ban.log") as file:
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
                    day_log = line.split()
                    if (day_log[5] == "[dovecot]" or day_log[5] == "[postfix]") and (day_log[6] == "Ban" or day_log[6] == "Unban"):
                        context['day_log'] += [day_log]

        return context
