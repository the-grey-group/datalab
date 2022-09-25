from flask_pymongo import PyMongo
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

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


def _get_active_mongo_client(timeoutMS: int = 100) -> MongoClient:
    """Returns a `MongoClient` for the configured `MONGO_URI`,
    raising a `RuntimeError` if not available.
    Parameters:
        timeoutMS: Value to use for the MongoDB timeouts (connect and server select)
            in milliseconds
    Returns:
        The active MongoClient, already connected.
    """
    from pydatalab.config import CONFIG
    from pydatalab.logger import LOGGER

    try:
        return MongoClient(
            CONFIG.MONGO_URI,
            connectTimeoutMS=timeoutMS,
            serverSelectionTimeoutMS=timeoutMS,
            connect=True,
        )
    except ServerSelectionTimeoutError as exc:
        LOGGER.critical(f"Unable to connect to MongoDB at {CONFIG.MONGO_URI}")
        raise RuntimeError from exc


__all__ = ("flask_mongo", "check_mongo_connection", "_get_active_mongo_client")
