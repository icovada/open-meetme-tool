# Generated by Django 4.1.3 on 2022-11-09 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetme_app', '0003_create_default_user_groups'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meetingrequest',
            options={'permissions': (('view_sent_invitations', 'Can view sent invitations'), ('view_received_invitations', 'Can view received invitations'), ('send_invitation', 'Can end invitation'), ('accept_invitation', 'Can accept invitation'))},
        ),
        migrations.RenameField(
            model_name='meetingrequest',
            old_name='accepted_date',
            new_name='acknowledge_date',
        ),
        migrations.AddField(
            model_name='meetingrequest',
            name='status',
            field=models.CharField(choices=[('ACK', 'Accepted'), ('NAK', 'Rejected')], max_length=6, null=True),
        ),
    ]
