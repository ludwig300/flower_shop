# Generated by Django 4.2.4 on 2023-08-23 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowershop_bot', '0007_remove_bouquet_quiz_steps_delete_quizstep'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=36, null=True),
        ),
    ]