import line_591_notifications.models as models
from line_591_notifications.celery import app
import line_591_notifications.utils as utils

@app.task
def send_notification():  
    notifications = models.Notification.objects.all()
    for notification in notifications:
        token = notification.token
        rent_url = notification.rent_url
        if not token or not rent_url:
            continue
        res = utils.notify(token, rent_url)
        if res.status_code == 401:
            notification.delete()
        elif res.status_code == 200:
            print(f"Notification sent to {notification.user.id}")
