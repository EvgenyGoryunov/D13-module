from django.apps import AppConfig
import redis


class McdonaldsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mcdonalds'


red = redis.Redis(
    host='redis-16974.c258.us-east-1-4.ec2.cloud.redislabs.com',
    port=16974,
    password='SLltAfLjaeIah58aXZBP6rICl6g60J2N'
)

