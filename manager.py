import click

@click.group()
def cli():
    """Nothing but an entrypoint"""

@click.command()
def celery_beater():
    from celery.bin.beat import beat
    from hcloud.libs.celery.celery import celery as celery_app
    from hcloud.config import CELERY_LOGLEVEL, CELERY_LOG_FILE
    celery_beater = beat(app=celery_app)
    celery_beater.run(loglevel=CELERY_LOGLEVEL)


@click.command()
@click.option('-w', default=1, help='Number of workers')
def celery_worker(w):
    from celery.bin.worker import worker
    from hcloud.libs.celery.celery import celery as celery_app
    from hcloud.config import CELERY_LOGLEVEL, CELERY_LOG_FILE
    celery_worker = worker(app=celery_app)
    celery_worker.run(concurrency=w, loglevel=CELERY_LOGLEVEL, logfile=CELERY_LOG_FILE, hostname='w1@%%h')


cli.add_command(celery_beater)
cli.add_command(celery_worker)


if __name__ == '__main__':
    cli()

