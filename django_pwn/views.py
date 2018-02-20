# -*- coding: utf-8 -*-

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.permissions import BasePermission

from udo.utils import get_ip

from .exceptions import PWNAPIError
from .settings import pwn_settings
from models import PWNOrder


ORDER_APPROVED = 'approved'
ORDER_REJECTED = 'rejected'
ORDER_RESULTED = 'resulted'


class OnlyPWNPermission(BasePermission):
    """
        Authorize PWN by the server IP address
    """
    def has_permission(self, request, view):
        ip = get_ip(request)
        if ip != pwn_settings.PWN_IP:
            return False
        else:
            return True


class NotifyView(APIView):
    """
        Process PWN result notification

        More info at:
        https://api-docs-labs-module.pwnhealth.com/v3.2.0/docs/notifications-system-overview
    """
    # permission_classes = [OnlyPWNPermission]

    def get(self, request, format=None):
        pwn_customer_id = request.GET.get('id')
        result = request.GET.get('result', None)
        # result_complete = request.GET.get('result_complete', None)
        try:
            pwn_order = PWNOrder.objects.get(pwn_customer_id=pwn_customer_id)
        except:
            raise PWNAPIError("Wrong id!")

        if result:
            pwn_order.fetch_results()
        return HttpResponse('')
