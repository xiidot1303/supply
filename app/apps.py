from django.apps import AppConfig
import os

class app(AppConfig):
    name = 'app'
    def ready(self):
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE')
        if run_once is not None:
            return
        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True'
        from scheduled_job import updater
        updater.start()
