from os import getenv
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.formats import number_format
from rest_framework import (
    views, response, status
)
from webhooks.models import Webhook
from services.callmebot import CallMeBot
from webhooks.messages import outflow_message


class WebhooksOrderView(views.APIView):

    def post(self, request):
        data = request.data
        __event_type = data.get('event_type')
        data.pop('event_type', None)

        Webhook.objects.create(
            event_type=__event_type,
            event=json.dumps(data, ensure_ascii=False)
        )

        quantity = data.get('quantity')
        product_selling_price = data.get('product_selling_price')
        product_cost_price = data.get('product_cost_price')
        __total_value_selling = product_selling_price * quantity
        __total_value_cost = product_cost_price * quantity
        __profit_value = __total_value_selling - __total_value_cost

        data['total_value_selling'] = number_format(
            __total_value_selling, decimal_pos=2, force_grouping=True
        )
        data['total_value_cost'] = number_format(
            __total_value_cost, decimal_pos=2, force_grouping=True
        )
        data['profit_value'] = number_format(
            __profit_value, decimal_pos=2, force_grouping=True
        )

        __message = outflow_message.format(
            data.get('product'),
            quantity,
            data.get('total_value_selling'),
            data.get('profit_value'),
            data.get('timestamp')
        )

        call_me_bot = CallMeBot()
        call_me_bot.send_message(message=__message)

        send_mail(
            subject='Uma nova saída foi registrada no (SGE)',
            message='',
            from_email=f'SGE <{getenv("EMAIL_HOST_USER")}>',
            recipient_list=[getenv('EMAIL_ADMIN_RECEIVER')],
            html_message=render_to_string('outflow.html', context=data),
            fail_silently=False,
        )

        return response.Response(
            data=data,
            status=status.HTTP_200_OK
        )
