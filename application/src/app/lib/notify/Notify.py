"""Manage notification channels (such as email) with users"""

import os
from datetime import datetime

from sparkpost import SparkPost

from app.models.Notification import Notification


class Notify:
    """Open a notification channel with a user"""

    CHANNEL_EMAIL = 1

    def __init__(self, env='development', db=None, force_email=None):
        self.env = env
        self.db = db
        self.force_email = force_email

    def send(self, user, channel, template=None, **kwargs):
        """Sends a notification to a user

        :param user: The user to notify
        :type user: User
        :param channel: The communication channel to use
        :type channel: int
        :param template: The name of the template to use when communicating
        :type template: string
        :param kwargs: Key:value pairs for template substitution
        :return: True if channel accepted notification, otherwise false
        :rtype: bool
        """

        # prep results
        notification_id = None
        accepted = 0
        rejected = 0
        service = None

        # use email channel
        if self.CHANNEL_EMAIL == channel:
            response = self._email(
                self.force_email if self.force_email else user.email, template,
                **kwargs)

            # parse results
            notification_id = response['notification_id']
            accepted = response['accepted']
            rejected = response['rejected']
            service = response['service']

        # no other channels at the moment
        else:
            pass

        # save notification to log if database object present
        if self.db:
            notification = Notification(
                user_id=user.id,
                channel=channel,
                template=template,
                service=service,
                notification_id=notification_id,
                accepted=accepted,
                rejected=rejected,
                sent_at=datetime.now(),
                status=Notification.STATUS_ENABLED,
                status_changed_at=datetime.now()
            )
            self.db.session.add(notification)
            self.db.session.commit()

        # return True if at least one notification sent
        return accepted >= 1

    def _email(self, email, template=None, **kwargs):
        """Sends an email via Sparkpost API

        :param email: A single email address to send to
        :type email: str
        :param template: The name of the template to use when communicating
        :type template: string
        :param kwargs: Key:value pairs for template substitution
        :return: A dictionary of values from the communication channel
        :rtype: dict
        """

        # prep output
        output = {
            'notification_id': None,
            'accepted': 0,
            'rejected': 0,
            'service': None
        }

        # send if in prod mode or forced
        if (os.environ.get('SPARKPOST_API_KEY') and
                (self.env == 'production' or self.force_email)):

            # send email via SparkPost
            sp = SparkPost()
            response = sp.transmissions.send(
                recipients=[email],
                template=template,
                substitution_data=kwargs
            )

            # parse response for output
            if response and isinstance(response, dict):
                if 'id' in response:
                    output['notification_id'] = response['id']
                if 'total_accepted_recipients' in response:
                    output['accepted'] = response['total_accepted_recipients']
                if 'total_rejected_recipients' in response:
                    output['rejected'] = response['total_rejected_recipients']
                output['service'] = "SparkPost"

        return output
