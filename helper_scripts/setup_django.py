"""File that sets up the django environment. Must be called at the beginning of any django script"""
import os
import django
env_config = os.environ.get('ENV_CONFIG', 'development')
print(f"Setting up django with {env_config} settings")
if env_config == "development":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uwccsystem.settings.development")
elif env_config == "ci":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uwccsystem.settings.ci")
elif env_config == "staging":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "excsystem.settings.staging")
elif env_config == "prod2":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "excsystem.settings.prod2")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uwccsystem.settings.production")

django.setup()
