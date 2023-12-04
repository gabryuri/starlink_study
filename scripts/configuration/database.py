import os

def load_required_env(env_name: str) -> str:
    """
    Loads a required environment variable.
    Throws exception in case necessary variables are missing
    """
    if env_name not in os.environ or os.environ[env_name] == "":
        raise DatabaseConfigurationHelper.NecessaryParameterMissing(env_name)
    return os.environ[env_name]


class DatabaseConfigurationHelper:
    class NecessaryParameterMissing(Exception):
        def __init__(self, parameter):
            self.message = f"Configuration fetch failed. Necessary environment variable {parameter} is not set."
            super().__init__(self.message)

    def __init__(self, logger) -> None:
        """
        A helper class for fetching and constructing database configuration details from environment variables.

        This class reads database configuration parameters such as username, password, host, port, and database name
        from the environment variables and provides an assembled database URI.

        Attributes:
            logger (Logger): A logging object used to log messages.

        Raises:
            NecessaryParameterMissing: If a required environment variable is missing or empty.

        Example:
            logger = logging.getLogger()
            config_helper = DatabaseConfigurationHelper(logger)
            db_uri = config_helper.database_uri
        """
        self.logger = logger
        self.fetch_configurations()

    def fetch_configurations(self) -> None:
        """
        Fetches the required database configuration parameters from environment variables.
        """
        self.logger.info("Fetching configurations from environment variables.")
        self.__db_username = load_required_env("POSTGRES_USER")
        self.__db_password = load_required_env("POSTGRES_PASSWORD")
        self.__db_port = load_required_env("POSTGRES_PORT")
        self.__db_name = load_required_env("POSTGRES_DB")
        self.__db_host = load_required_env("POSTGRES_HOST")

    @property
    def database_uri(self) -> str:
        """
        Database URI to be used in SQLAlchemy.
        """
        return f"postgresql+psycopg2://{self.__db_username}:{self.__db_password}@{self.__db_host}:{self.__db_port}/{self.__db_name}"
