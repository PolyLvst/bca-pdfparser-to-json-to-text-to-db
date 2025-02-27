import yaml

class Configurer:
    def __init__(self):
        self.config_path = "./config.yaml"
        self.__configs = {}
        self.__load_config()
    
    def __load_config(self):
        with open(self.config_path, "r") as file:
            self.__configs = yaml.safe_load(file)
    
    def get_db_string(self):
        db_key = self.__configs.get("db")
        username = db_key.get("username")
        password = db_key.get("password")
        host = db_key.get("host")
        database = db_key.get("database")
        port = db_key.get("port")
        db_string = f"mssql+pyodbc://{username}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
        return db_string

    def get_db_table(self):
        db_key = self.__configs.get("db")
        table = db_key.get("table")
        return table