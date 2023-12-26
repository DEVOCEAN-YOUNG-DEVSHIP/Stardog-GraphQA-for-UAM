from typing import Any, Dict, List, Optional

from langchain.graphs.graph_store import GraphStore
from langchain.utils import get_from_env

# 임시
# 추후 stardog 라이브러리를 이용하여 가져오도록 수정
schema = """
<tag:stardog:designer:UAM_DEVOCEAN:model:AREA> a <http://www.w3.org/2002/07/owl#Class> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "AREA" ;
  <tag:stardog:designer:colorId> "sd-qb-green" .
<tag:stardog:designer:UAM_DEVOCEAN:model:TIME> a <http://www.w3.org/2002/07/owl#Class> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "TIME" ;
  <tag:stardog:designer:colorId> "sd-qb-yellow-green" .
<tag:stardog:designer:UAM_DEVOCEAN:model:UAM> a <http://www.w3.org/2002/07/owl#Class> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "UAM" ;
  <tag:stardog:designer:colorId> "sd-qb-red" .
<tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPAD> a <http://www.w3.org/2002/07/owl#Class> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "VERTIPAD" ;
  <tag:stardog:designer:colorId> "sd-qb-orange" .
<tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPORT> a <http://www.w3.org/2002/07/owl#Class> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "VERTIPORT" ;
  <tag:stardog:designer:colorId> "sd-qb-gold" .
<tag:stardog:designer:UAM_DEVOCEAN:model:waypoint> a <http://www.w3.org/2002/07/owl#Class> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "WAYPOINT" ;
  <tag:stardog:designer:colorId> "sd-qb-light-orange" .

<tag:stardog:designer:UAM_DEVOCEAN:model:between> a <http://www.w3.org/2002/07/owl#ObjectProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "between" ;
  <https://schema.org/domainIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:waypoint> ;
  <https://schema.org/rangeIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPORT> .
<tag:stardog:designer:UAM_DEVOCEAN:model:in> a <http://www.w3.org/2002/07/owl#ObjectProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "in" ;
  <https://schema.org/domainIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPAD> ;
  <https://schema.org/rangeIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPORT> .
<tag:stardog:designer:UAM_DEVOCEAN:model:in_area> a <http://www.w3.org/2002/07/owl#ObjectProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "in area" ;
  <https://schema.org/domainIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPORT>, <tag:stardog:designer:UAM_DEVOCEAN:model:waypoint> ;
  <https://schema.org/rangeIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:AREA> .
<tag:stardog:designer:UAM_DEVOCEAN:model:on_time> a <http://www.w3.org/2002/07/owl#ObjectProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "on time" ;
  <https://schema.org/domainIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:AREA>, <tag:stardog:designer:UAM_DEVOCEAN:model:UAM>, <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPAD>, <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPORT>, <tag:stardog:designer:UAM_DEVOCEAN:model:waypoint> ;
  <https://schema.org/rangeIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:TIME> .
<tag:stardog:designer:UAM_DEVOCEAN:model:on_vertipad> a <http://www.w3.org/2002/07/owl#ObjectProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "on vertipad" ;
  <https://schema.org/domainIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:UAM> ;
  <https://schema.org/rangeIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPAD> .
<tag:stardog:designer:UAM_DEVOCEAN:model:on_waypoint> a <http://www.w3.org/2002/07/owl#ObjectProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "on waypoint" ;
  <https://schema.org/domainIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:UAM> ;
  <https://schema.org/rangeIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:waypoint> .

<tag:stardog:designer:UAM_DEVOCEAN:model:area_id> a <http://www.w3.org/2002/07/owl#DatatypeProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "area_id" ;
  <https://schema.org/domainIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:AREA>, <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPORT>, <tag:stardog:designer:UAM_DEVOCEAN:model:waypoint> ;
  <https://schema.org/rangeIncludes> <http://www.w3.org/2001/XMLSchema#string> .
<tag:stardog:designer:UAM_DEVOCEAN:model:availability> a <http://www.w3.org/2002/07/owl#DatatypeProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "availability" ;
  <https://schema.org/domainIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:AREA> ;
  <https://schema.org/rangeIncludes> <http://www.w3.org/2001/XMLSchema#boolean> .
<tag:stardog:designer:UAM_DEVOCEAN:model:num_of_avail_vertipad> a <http://www.w3.org/2002/07/owl#DatatypeProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "num_of_avail_vertipad" ;
  <https://schema.org/rangeIncludes> <http://www.w3.org/2001/XMLSchema#integer> .
<tag:stardog:designer:UAM_DEVOCEAN:model:time> a <http://www.w3.org/2002/07/owl#DatatypeProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "time" ;
  <https://schema.org/domainIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:AREA>, <tag:stardog:designer:UAM_DEVOCEAN:model:TIME>, <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPAD>, <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPORT>, <tag:stardog:designer:UAM_DEVOCEAN:model:waypoint> ;
  <https://schema.org/rangeIncludes> <http://www.w3.org/2001/XMLSchema#time> .
<tag:stardog:designer:UAM_DEVOCEAN:model:uam_id> a <http://www.w3.org/2002/07/owl#DatatypeProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "uam_id" ;
  <https://schema.org/domainIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:UAM>, <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPAD>, <tag:stardog:designer:UAM_DEVOCEAN:model:waypoint> ;
  <https://schema.org/rangeIncludes> <http://www.w3.org/2001/XMLSchema#string> .
<tag:stardog:designer:UAM_DEVOCEAN:model:uam_type> a <http://www.w3.org/2002/07/owl#DatatypeProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "uam_type" ;
  <https://schema.org/rangeIncludes> <http://www.w3.org/2001/XMLSchema#string> .
<tag:stardog:designer:UAM_DEVOCEAN:model:vertipad_id> a <http://www.w3.org/2002/07/owl#DatatypeProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "vertipad_id" ;
  <https://schema.org/domainIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:UAM>, <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPAD> ;
  <https://schema.org/rangeIncludes> <http://www.w3.org/2001/XMLSchema#string> .
<tag:stardog:designer:UAM_DEVOCEAN:model:vertiport_id> a <http://www.w3.org/2002/07/owl#DatatypeProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "vertiport_id" ;
  <https://schema.org/domainIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:UAM>, <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPAD>, <tag:stardog:designer:UAM_DEVOCEAN:model:VERTIPORT> ;
  <https://schema.org/rangeIncludes> <http://www.w3.org/2001/XMLSchema#string> .
<tag:stardog:designer:UAM_DEVOCEAN:model:waypoint_id> a <http://www.w3.org/2002/07/owl#DatatypeProperty> ;
  <http://www.w3.org/2000/01/rdf-schema#label> "waypoint_id" ;
  <https://schema.org/domainIncludes> <tag:stardog:designer:UAM_DEVOCEAN:model:UAM>, <tag:stardog:designer:UAM_DEVOCEAN:model:waypoint> ;
  <https://schema.org/rangeIncludes> <http://www.w3.org/2001/XMLSchema#string> .
"""


class StardogGraph(GraphStore):
    """Stardog wrapper for graph operations.

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
        """Create a new Stardog graph wrapper instance."""
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
        
        self.conn = stardog.Connection(database, **conn_details)
        self.schema = schema
        
    def query(self, sparql_query):
        """Query Stardog database."""
        from stardog.exceptions import StardogException
        try:
            results = self.conn.select(sparql_query)
            return results
        except StardogException as e:
            raise ValueError(f"Generated Stardog Statement is not valid\n{e}")

    @property
    def get_schema(self) -> str:
        """Returns the schema of the Graph"""
        return self.schema