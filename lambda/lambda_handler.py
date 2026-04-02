import os
from apig_wsgi import make_lambda_handler
from app import app

prefix = os.environ.get("URL_PREFIX", "").rstrip("/")

if prefix:
    class StripPrefix:
        def __init__(self, wsgi_app, prefix):
            self.wsgi_app = wsgi_app
            self.prefix = prefix

        def __call__(self, environ, start_response):
            path = environ.get("PATH_INFO", "")
            if path.startswith(self.prefix):
                environ["PATH_INFO"] = path[len(self.prefix):] or "/"
                environ["SCRIPT_NAME"] = self.prefix
            return self.wsgi_app(environ, start_response)

    application = StripPrefix(app, prefix)
else:
    application = app

handler = make_lambda_handler(application, binary_support=True)
