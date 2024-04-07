from FeedCreatorServices.GraphDatabaseOperations.Neo4jClient import Neo4jClient


class CollaborativeQueryCreator:
    
    def __init__(self):
        self.driver = Neo4jClient.createClient()
        
    def fetch_top_interest(self, tx, user):
        
        query = """
        MATCH (u: User {id: $user})-[:Likes]->(p:Post)-[:Of]->(i:Interest)
        RETURN i.id AS interest
        """
        
        result = tx.run(query, user=user)
        interests = [record["interest"] for record in result]
        print(interests)
        return interests

    def fetch_top_user_connection(self, tx, user):
        query ="""
        MATCH (u1: User {id: $user})-[:Likes]->(p:Post)<-[:From]-(u:User)<-[:Connection]-(u1: User {id: $user})
        RETURN u.id AS userId
        """
        result = tx.run(query, user=user)
        connection = [record["userId"] for record in result]
        print(connection)
        return connection
        
    def fetch_network_content(self, tx, user):
        query ="""
        MATCH (u: User {id: $user})-[:Has]->(i: Interest)
        MATCH (u)-[:Connection]->()-[:From]->(p:Post)-[:Of]->(i)
        RETURN p.id AS postId         
        """
        
        result = tx.run(query, user=user)
        post = [record["postId"] for record in result]
        print(post)
        return post
    
    def fetch_suggested_post(self, tx, user):
        query = """
        MATCH (u: User {id: $user})-[:Has]->(i: Interest)
        MATCH (i)<-[:Of]-(p:Post)<-[l:Likes]-()
        with p, count(l) as likes
        ORDER BY likes DESC
        RETURN p.id as postId
        """
        result = tx.run(query, user=user)
        posts = [record["postId"] for record in result]
        print(posts)
        return posts
    
    def fetch_suggested_users(self, tx, user, interest):
        query = """
        MATCH (u: User {id: $user}) -[:Connection]->()-[:Connection]->(u1: User)-[f:From]->()
        MATCH (u1: User) -[:Has]-> (i : Interest {id: $interest})
        with u1, count(f) as activity
        ORDER BY activity DESC
        RETURN u1.id as userId
        """
        result = tx.run(query, interest=interest, user=user)
        user = [record["userId"] for record in result]
        print(user)
        return user
    
    def FetchTopInterestExcutor(self, name):
        with self.driver.session() as session:
            session.write_transaction(self.fetch_top_interest,name)
            
    def FetchTopConnectionExcutor(self, name):
        with self.driver.session() as session:
            session.write_transaction(self.fetch_top_user_connection,name)
            
    def FetchContentExecutor(self, interest, name):
        with self.driver.session() as session:
            session.write_transaction(self.fetch_network_content,interest, name)
            
            
    def FetchSuggestedPosts(self, interest):
        with self.driver.session() as session:
            session.write_transaction(self.fetch_suggested_post,interest)
            
    def FetchSuggestedUsers(self, users, interest):
        with self.driver.session() as session:
            session.write_transaction(self.fetch_suggested_users, users, interest)