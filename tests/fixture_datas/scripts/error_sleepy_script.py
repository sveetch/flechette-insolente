#!/home/emencia/Projects/Apps/flechette-insolente/.venv/bin/python

if __name__ == "__main__":
    import time

    from dartsass.logger import init_logger

    SLEEPY_TIME = 5

    print("Starting sample with sleeping operation during {}s".format(SLEEPY_TIME))

    logger = init_logger(
        "flechette-insolente", 5, printout=True
    )

    logger.debug("Une ligne de debug 👷.")
    logger.info("Une ligne d'info.")

    print("A line between logs")

    logger.warning("🚨 Une ligne de warning.")
    logger.critical("Une ligne de critique.")

    time.sleep(SLEEPY_TIME)
