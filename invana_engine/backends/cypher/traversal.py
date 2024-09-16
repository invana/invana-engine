



class Neo4jTraversal:
    """This module takes traversal config and fetches the data from 
    all the traversals. Anything that is not Properties is a traversal .

    A) Get Properties 
    "Properties": {
      "screen_name": true,
      "last_name": true,
      "first_name": true
    }


    B) Four types of traveral definitions are supported 
    1. Traversal defined in `relationship_fields` of Node (Actor.relationship_fields)
        Ex: in the following case, `movies` is a traversal, but the relationships 
        of movies should be figured using the Actor.relationship_fields data. 
    2. Generic direction traversal ex: `oute` or `ine`.
        this case should follow `oute` by the target node , incase of `ine` source node.
        "oute": {
            "Movie": {
                "Id": true,
                "Label": true,
                "Properties": {
                "published_date": true,
                "title": true
                }
            }
        }
    3. Directed relationship. ex: `oute__ACTED_IN`
        this case is same as (2) - but relation is also specified 
        "oute__ACTED_IN": {
            "Movie": {
                "Id": true,
                "Label": true,
                "Properties": {
                "title": true,
                "published_date": true
                }
            }
        }

    4. Directed relationship to Node. ex: oute__ACTED_IN__ShortMovie
    "oute__ACTED_IN__ShortMovie": {
      "ShortMovie": {
        "Id": true,
        "Label": true,
        "Properties": {
          "published_date": true,
          "title": true
        }
      }
    }
 
    """
    

    def get_traversed_data(self, traversal_config):
      """This 

      Args:
          traversal_config (_type_): contains both the description of 
          1. filters(and, or, not, property filter) and 
          2. traversals (oute, oute__ACTED_IN, etc)  
      """

      return 