from Utility_Module.Postgres import Postgres

class DatabaseConnectionSetter:
    
    @staticmethod 
    def create_database_url():
        databaseConnector: Postgres.Postgres = Postgres.Postgres.get_postgres_settings()
        connection = f"postgresql+psycopg2://{databaseConnector.user}:{databaseConnector.password}@{databaseConnector.host}:{databaseConnector.port}/{databaseConnector.database}"
        return connection   
        
        