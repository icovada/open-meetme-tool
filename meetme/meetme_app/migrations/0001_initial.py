# Generated by Django 4.1.3 on 2022-11-12 22:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField()),
                ('address', models.TextField()),
                ('meeting_duration_mins', models.PositiveIntegerField()),
                ('meeting_time_slots', models.PositiveIntegerField()),
                ('meeting_concurrencies', models.PositiveIntegerField()),
                ('registered_users', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=30)),
                ('event_participations', models.ManyToManyField(to='meetme_app.event')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MeetingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('acknowledge_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('ACK', 'Accepted'), ('NAK', 'Rejected')], max_length=6, null=True)),
                ('fkevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetme_app.event')),
                ('invitee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invites_received', to=settings.AUTH_USER_MODEL)),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations_sent', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_sent_invitations', 'Can view sent invitations'), ('view_received_invitations', 'Can view received invitations'), ('send_invitation', 'Can send invitation'), ('accept_invitation', 'Can accept invitation')),
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_slot', models.PositiveIntegerField()),
                ('concurrency', models.PositiveIntegerField()),
                ('booked_meeting', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='meetme_app.meetingrequest')),
                ('fkevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetme_app.event')),
            ],
        ),
        migrations.AddConstraint(
            model_name='meetingrequest',
            constraint=models.UniqueConstraint(fields=('fkevent', 'inviter', 'invitee'), name='one_invite_per_pair_per_event'),
        ),
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.UniqueConstraint(fields=('fkevent', 'time_slot', 'concurrency'), name='one_slot_per_room_per_event'),
        ),
    ]
