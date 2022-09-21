from flask_pymongo import PyMongo

flask_mongo = PyMongo()


def check_mongo_connection():
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure

    from pydatalab.config import CONFIG
    from pydatalab.logger import LOGGER

    try:
        cli = MongoClient(
            CONFIG.MONGO_URI, connectTimeoutMS=100, serverSelectionTimeoutMS=100, connect=True
        )
        cli.list_database_names()
    except ConnectionFailure as exc:
        LOGGER.critical(f"Unable to connect to MongoDB at {CONFIG.MONGO_URI}")
        raise RuntimeError from exc

    return True


__all__ = ("flask_mongo", "check_mongo_connection")
