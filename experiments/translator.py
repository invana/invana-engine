from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal

connection = DriverRemoteConnection("ws://localhost:8182/gremlin", "g")
g = traversal().withRemote(connection)


class GremlinQueryTranslator:
    allowed_predicates_list = ['within', 'without', 'inside', 'outside', 'between', 'eq', 'neq',
                               'lt', 'lte', 'gt', 'gte', 'startingWith', 'containing', 'endingWith',
                               'notStartingWith', 'notContaining', 'notEndingWith']
    filter_key_starting_words_list = ['has']
    pagination_key_starting_words_list = ["pagination"]

    """
    USAGE: example usage.
    
    gremlin_query = GremlinQueryTranslator()
    gremlin_query = query_translator.process_search_kwargs(
            has__label__within=["Person", "Planet"],
            pagination__range=[0, 10],
        )
    
    has__id=1021
    has__id__within=[200752, 82032, 4320],
    has__label__within=["Person", "Planet"]
    has__label__without=["Person", "Planet"]
    has__label="Person"
    has__age__lte=25
    has__age__lt=25
    has__age__gte=25
    has__age__gt=25
    has__age__inside=(10, 20)
    has__age__outside=(10, 20)
    has__age__between=(10, 20)
    has__label__eq="Person"
    has__label__neq="Person"
    
    has__name__startingWith="Per"
    has__name__endingWith="son"
    has__name__containing="erson"
    has__name__notStartingWith="son"
    has__name__notEndingWith="son"
    has__name__notContaining="son"

    pagination__limit=10
    pagination__range=[0, 10]
    
    Refer https://tinkerpop.apache.org/docs/3.5.0/reference/#a-note-on-predicates for more details on usage.
    """

    def extract_filters_and_pagination_kwargs(self, **kwargs):
        filter_kwargs = {}
        pagination_kwargs = {}
        for kwarg_key, value in kwargs.items():
            for starting_keyword in self.filter_key_starting_words_list:
                if kwarg_key.startswith(starting_keyword):
                    filter_kwargs[kwarg_key] = value
            for starting_keyword in self.pagination_key_starting_words_list:
                if kwarg_key.startswith(starting_keyword):
                    pagination_kwargs[kwarg_key] = value
        return {"filter_kwargs": filter_kwargs, "pagination_kwargs": pagination_kwargs}

    def process_search_kwargs(self, **kwargs):
        query_string = "g.V()"
        cleaned_kwargs = self.extract_filters_and_pagination_kwargs(**kwargs)
        for kwarg_key, value in cleaned_kwargs['filter_kwargs'].items():
            kwargs__list = kwarg_key.split("__")
            if kwargs__list.__len__() >= 2:
                if kwargs__list.__len__() == 2:
                    query_string += ".{0}({1}, {2})".format(kwargs__list[0], kwargs__list[1], self.check_if_str(value))
                else:
                    if kwargs__list[2] not in self.allowed_predicates_list:
                        raise Exception("{} not allowed in kwargs. Only {} are allowed".format(
                            kwargs__list[2], self.allowed_predicates_list))
                    query_string += ".{0}({1}, {2}({3}))".format(kwargs__list[0], kwargs__list[1],
                                                                 kwargs__list[2],
                                                                 self.check_if_str(value))
        for kwarg_key, value in cleaned_kwargs['pagination_kwargs'].items():
            kwargs__list = kwarg_key.split("__")
            if kwargs__list.__len__() == 2:
                if type(value) in [list, tuple]:
                    query_string += ".{0}{1}".format(kwargs__list[1], tuple(value))
                else:
                    query_string += ".{0}({1})".format(kwargs__list[1], value)
            else:
                raise Exception("{} not allowed in kwargs. Only {} are allowed".format(
                    kwargs__list[2], self.allowed_predicates_list))
        query_string += ".toList()"
        return query_string

    @staticmethod
    def check_if_str(s):
        if type(s) is str:
            return "'{}'".format(s)
        return s


query_translator = GremlinQueryTranslator()

gremlin_query = query_translator.process_search_kwargs(
    has__label__neq="Person",
    pagination__range=[0, 5],
)

print("query__", gremlin_query)
result = connection._client.submit(gremlin_query).all().result()

print("=====result: ", result)
print("=====result: ", list(set([res.label for res in result])))
connection.close()
