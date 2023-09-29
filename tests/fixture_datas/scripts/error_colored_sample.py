#!/home/emencia/Projects/Apps/flechette-insolente/.venv/bin/python

if __name__ == "__main__":
    import click

    from dartsass.logger import init_logger

    print("Starting sample with click.Abort()")

    logger = init_logger(
        "flechette-insolente", 5, printout=True
    )

    logger.debug("Une ligne de debug 👷.")
    logger.info("Une ligne d'info.")

    print("A line between logs")

    logger.warning("🚨 Une ligne de warning.")
    logger.critical("Une ligne de critique.")

    raise click.Abort()
