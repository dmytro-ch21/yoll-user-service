import logging


def configure_logging(
    app,
    log_level=logging.DEBUG,
    log_format="%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
):
    app.logger.setLevel(log_level)
    if not app.logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
