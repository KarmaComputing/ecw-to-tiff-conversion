import logging
import threading
from flask import current_app

log = logging.getLogger(__name__)


def background_task(f):
    def bg_f(*a, **kw):
        app = current_app._get_current_object()
        kw["app"] = app  # inject flask app for app context
        log.info(f"Starting background_taski with kw args: {kw}")
        threading.Thread(target=f, args=a, kwargs=kw).start()

    return bg_f
