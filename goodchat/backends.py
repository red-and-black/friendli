from logging import getLogger

from django.core.mail.backends.filebased import EmailBackend as FBEmailBackend
from django.core.mail.backends.smtp import EmailBackend as SmtpEmailBackend


class LoggingFileBasedEmailBackend(FBEmailBackend):
    """A wrapper around `filebased.EmailBackend` that logs every email."""

    def __init__(self, *args, **kwargs):
        super(LoggingFileBasedEmailBackend, self).__init__(*args, **kwargs)
        self.logger = getLogger('django.mail')

    def write_message(self, message):
        super(LoggingFileBasedEmailBackend, self).write_message(message)

        # Write the log entry.
        log_entry = 'To: %s | Subject: \'%s\' | Status: Sent' % (
            '; '.join(message.recipients()),
            message.subject,
        )
        self.logger.info(log_entry)


class LoggingSmtpEmailBackend(SmtpEmailBackend):
    """A wrapper around `smtp.EmailBackend` that logs every email."""

    def __init__(self, *args, **kwargs):
        super(LoggingSmtpEmailBackend, self).__init__(*args, **kwargs)
        self.logger = getLogger('django.mail')

    def _send(self, email_message):
        sent = super(LoggingSmtpEmailBackend, self)._send(email_message)

        # Write the log entry.
        log_entry = 'To: %s | Subject: \'%s\'' % (
            '; '.join(email_message.recipients()),
            email_message.subject,
        )
        if sent:
            log_entry += ' | Status: Sent'
            self.logger.info(log_entry)
        else:
            log_entry += ' | Status: Failed to send'
            self.logger.warn(log_entry)

        return sent
