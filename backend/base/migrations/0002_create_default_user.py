from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_default_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='user').exists():
        User.objects.create(
            username='user',
            email='admin@example.com',
            password=make_password('1234'),
            is_staff=True,
            is_superuser=True
        )

def reverse_default_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='user').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('base', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_default_user, reverse_default_user),
    ]