from django.core.management.base import BaseCommand


from growers.utils import sms_queue

class Command(BaseCommand):
    help = 'Checking and processing sms queue'

    def handle(self, *args, **options):
        self.stdout.write('Sending sms messages...')
        err = sms_queue()
        if err:
            self.stdout.write('Error: ' + err)
        else:
            self.stdout.write('Finished sending messages...')




