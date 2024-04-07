import neo4j

class Neo4jClient:
    
    @staticmethod
    def createClient():
        uri = "neo4j://localhost:7687"
        userName = "neo4j"
        password = "12345678"
        
        driver = neo4j.GraphDatabase.driver(uri, auth= (userName, password))
        
        return driver
    
    
    