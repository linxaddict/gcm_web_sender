from django.shortcuts import render
from gcm import GCM
from gcm_sender.models import Shopper, NotificationNewOrderAvailable, NotificationShopperFound, \
    NotificationShopperVerified


def index(request):
    return render(request, 'gcm_sender/index.html')


def create_notification(notification_type):
    if notification_type == 'push_new_order':
        return NotificationNewOrderAvailable(1)
    elif notification_type == 'push_shopper_found':
        shopper = Shopper(1, 'shopper_name', 'shopper_surname', 'http://photo.com/1')
        return NotificationShopperFound('2015-10-25T22:34:51+00:00', shopper)
    elif notification_type == 'push_shopper_verified':
        return NotificationShopperVerified()

    return None


def send_gcm_push(request):
    r = request

    if 'api_token' not in r.POST:
        return render(request, 'gcm_sender/index.html', {'error_message': 'api token missing'})

    if 'device_token' not in r.POST:
        return render(request, 'gcm_sender/index.html', {'error_message': 'device token missing'})

    if 'push' not in r.POST:
        return render(request, 'gcm_sender/index.html', {'error_message': 'notification type missing'})

    try:
        client = GCM(r.POST['api_token'])
        notification = create_notification(r.POST['push'])
        if notification is None:
            return render(request, 'gcm_sender/index.html', {'error_message': 'unable to sent the notification'})

        response = client.json_request(registration_ids=[r.POST['device_token']],
                                       data=notification.as_dict())
        if 'success' not in response:
            return render(request, 'gcm_sender/index.html', {'error_message': 'unable to sent the notification'})

        return render(request, 'gcm_sender/index.html', {'success': True})
    except Exception as err:
        return render(request, 'gcm_sender/index.html', {'error_message': 'unable to sent the notification'})
