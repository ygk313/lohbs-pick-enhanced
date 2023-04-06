from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'delete user which is_active is false'

    def handle(self, *args, **options):

        users = User.objects.all()

        for user in users:
            if user.is_active is False:
                tmp = user.username
                user.delete()
                print(tmp," 가 삭제되었습니다.")

# crontab(분,시,일,월,요일) - 0 0 * * * python manage.py user_delete_command