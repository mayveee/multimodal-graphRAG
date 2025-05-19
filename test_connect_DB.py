from neo4j import GraphDatabase
import certifi

uri = "neo4j+ssc://11891092.databases.neo4j.io"
auth = ("neo4j", "tLP_I6Zd36gLpVpUz8jtHSyCHYvJfzMBRI7VekMTbfQ")

with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
            result = session.run("CREATE (img:Image {image_id: 'img1234'})", {})
            summary = result.consume()
            print(result, summary.counters.nodes_created)