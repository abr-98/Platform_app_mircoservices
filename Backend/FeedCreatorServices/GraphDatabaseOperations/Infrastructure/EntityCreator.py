from FeedCreatorServices.GraphDatabaseOperations.Neo4jClient import Neo4jClient

class EntityCreator:
    
    def __init__(self):
        self.driver = Neo4jClient.createClient()
        
    def CreateEntityExcutor(self, datatype, name):
        with self.driver.session() as session:
            session.write_transaction(self.__Create_command, datatype,name)
            
    def CreateRelationshipExcutor(self, datatype1, datatype2, node1_name, node2_name, relation):
        with self.driver.session() as session:
            session.write_transaction(self.__Relation_creator_command,datatype1, datatype2, node1_name, node2_name, relation)

        
    
    def __Create_command(self, tx, datatype, name):
        command = "CREATE (n: {datatype}  {id : $name})".replace("{datatype}",datatype)
        tx.run(command, name=name)
        
    def __Relation_creator_command(self, tx, type1, type2, node1_name, node2_name, rel_type):
        query = """MATCH (n1: {type1} {id :  $node1_name}),(n2: {type2} {id :  $node2_name}) 
        CREATE (n1)-[r: {rel_type}]-> (n2)""".replace("{type1}",type1).replace("{type2}", type2).replace("{rel_type}", rel_type)
        
        tx.run(query, node1_name=node1_name, node2_name=node2_name)



