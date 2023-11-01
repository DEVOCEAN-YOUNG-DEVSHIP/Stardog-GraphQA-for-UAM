from typing import Any, Dict, List, Optional

# from langchain.graphs.graph_document import GraphDocument
from langchain.graphs.graph_store import GraphStore
from langchain.utils import get_from_env

# node_properties_query = """
# CALL apoc.meta.data()
# YIELD label, other, elementType, type, property
# WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
# WITH label AS nodeLabels, collect({property:property, type:type}) AS properties
# RETURN {labels: nodeLabels, properties: properties} AS output

# """

# rel_properties_query = """
# CALL apoc.meta.data()
# YIELD label, other, elementType, type, property
# WHERE NOT type = "RELATIONSHIP" AND elementType = "relationship"
# WITH label AS nodeLabels, collect({property:property, type:type}) AS properties
# RETURN {type: nodeLabels, properties: properties} AS output
# """

# rel_query = """
# CALL apoc.meta.data()
# YIELD label, other, elementType, type, property
# WHERE type = "RELATIONSHIP" AND elementType = "node"
# UNWIND other AS other_node
# RETURN {start: label, type: property, end: toString(other_node)} AS output
# """


class StardogGraph(GraphStore):
    """Neo4j wrapper for graph operations.

    *Security note*: Make sure that the database connection uses credentials
        that are narrowly-scoped to only include necessary permissions.
        Failure to do so may result in data corruption or loss, since the calling
        code may attempt commands that would result in deletion, mutation
        of data if appropriately prompted or reading sensitive data if such
        data is present in the database.
        The best way to guard against such negative outcomes is to (as appropriate)
        limit the permissions granted to the credentials used with this tool.

        See https://python.langchain.com/docs/security for more information.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
    ) -> None:
        """Create a new Neo4j graph wrapper instance."""
        try:
            import stardog
        except ImportError:
            raise ValueError(
                "Could not import stardog python package. "
                "Please install it with `pip install pystardog`."
            )
            
        endpoint = get_from_env("url", "STARDOG_ENDPOINT", endpoint)
        username = get_from_env("username", "STARDOG_USERNAME", username)
        password = get_from_env("password", "STARDOG_PASSWORD", password)
        database = get_from_env("database", "STARDOG_DATABASE", database)
        
        conn_details = {
            "endpoint": endpoint,
            "username": username,
            "password": password,
        }
        
        # self._admin = stardog.Admin(**conn_details)
        self.conn = stardog.Connection(database, **conn_details)
        
    def query(self, sparql_query):
        """Query Stardog database."""
        from stardog.exceptions import StardogException
        try:
            results = self.conn.select(sparql_query)
            return results
        except StardogException as e:
            raise ValueError(f"Generated Stardog Statement is not valid\n{e}")
    # def query(self, query: str, params: dict = {}) -> List[Dict[str, Any]]:
    #     """Query Neo4j database."""
    #     from neo4j.exceptions import CypherSyntaxError

    #     with self._driver.session(database=self._database) as session:
    #         try:
    #             data = session.run(query, params)
    #             return [r.data() for r in data]
    #         except CypherSyntaxError as e:
    #             raise ValueError(f"Generated Cypher Statement is not valid\n{e}")
        

    #     self._driver = stardog.GraphDatabase.driver(url, auth=(username, password))
    #     self._database = database
    #     self.schema: str = ""
    #     self.structured_schema: Dict[str, Any] = {}
    #     # Verify connection
    #     try:
    #         self._driver.verify_connectivity()
    #     except neo4j.exceptions.ServiceUnavailable:
    #         raise ValueError(
    #             "Could not connect to Neo4j database. "
    #             "Please ensure that the url is correct"
    #         )
    #     except neo4j.exceptions.AuthError:
    #         raise ValueError(
    #             "Could not connect to Neo4j database. "
    #             "Please ensure that the username and password are correct"
    #         )
    #     # Set schema
    #     try:
    #         self.refresh_schema()
    #     except neo4j.exceptions.ClientError:
    #         raise ValueError(
    #             "Could not use APOC procedures. "
    #             "Please ensure the APOC plugin is installed in Neo4j and that "
    #             "'apoc.meta.data()' is allowed in Neo4j configuration "
    #         )

    # @property
    # def get_schema(self) -> str:
    #     """Returns the schema of the Graph"""
    #     return self.schema

    # @property
    # def get_structured_schema(self) -> Dict[str, Any]:
    #     """Returns the structured schema of the Graph"""
    #     return self.structured_schema

    # def query(self, query: str, params: dict = {}) -> List[Dict[str, Any]]:
    #     """Query Neo4j database."""
    #     from neo4j.exceptions import CypherSyntaxError

    #     with self._driver.session(database=self._database) as session:
    #         try:
    #             data = session.run(query, params)
    #             return [r.data() for r in data]
    #         except CypherSyntaxError as e:
    #             raise ValueError(f"Generated Cypher Statement is not valid\n{e}")