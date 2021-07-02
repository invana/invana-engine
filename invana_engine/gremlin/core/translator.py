"""

"""
from invana_engine.gremlin.core.exceptions import InvalidQueryArguments


class GremlinQueryTranslator:
    allowed_predicates_list = ['within', 'without', 'inside', 'outside', 'between', 'eq', 'neq',
                               'lt', 'lte', 'gt', 'gte', 'startingWith', 'containing', 'endingWith',
                               'notStartingWith', 'notContaining', 'notEndingWith']
    filter_key_starting_words_list = ['has']
    pagination_key_starting_words_list = ["pagination"]

    """
    USAGE: example usage.

    gremlin_query = GremlinQueryTranslator()
    c = query_translator.process_search_kwargs(
            has__label__within=["Person", "Planet"],
            pagination__range=[0, 10],
        ) # g.V().has(label, neq('Person')).range(0, 5)

    
    
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

    @staticmethod
    def validate_search_kwargs(**search_kwargs):
        pass  # TODO - security | add this, or sometimes, it might delete entire graph data if no has__ data is sent
        valid_search_kwargs = False
        for k, v in search_kwargs.items():
            if k.startswith("has__") or k.startswith("pagination__"):
                valid_search_kwargs = True
                break
        if valid_search_kwargs is False:
            raise InvalidQueryArguments(
                "Either has__** or pagination__** search kwargs should be used with filter many type queries")

    def separate_filters_and_pagination_kwargs(self, **search_kwargs):
        filter_kwargs = {}
        pagination_kwargs = {}
        for kwarg_key, value in search_kwargs.items():
            for starting_keyword in self.filter_key_starting_words_list:
                if kwarg_key.startswith(starting_keyword):
                    filter_kwargs[kwarg_key] = value
            for starting_keyword in self.pagination_key_starting_words_list:
                if kwarg_key.startswith(starting_keyword):
                    pagination_kwargs[kwarg_key] = value
        return {"filter_kwargs": filter_kwargs, "pagination_kwargs": pagination_kwargs}

    def process_search_kwargs(self, element_type=None, **search_kwargs):
        if element_type not in ["V", "E"]:
            raise Exception("invalid element_type provided, valid values are : 'V', 'E'", )
        query_string = "g.{element_type}()".format(element_type=element_type)
        cleaned_kwargs = self.separate_filters_and_pagination_kwargs(**search_kwargs)
        for kwarg_key, value in cleaned_kwargs['filter_kwargs'].items():
            kwargs__list = kwarg_key.split("__")
            if kwargs__list.__len__() >= 2:
                if kwargs__list.__len__() == 2:
                    query_string += ".{0}({1}, {2})".format(kwargs__list[0],
                                                            # self.check_if_str(
                                                            kwargs__list[1]
                                                            # )
                                                            ,
                                                            self.check_if_str(value))
                else:
                    if kwargs__list[2] not in self.allowed_predicates_list:
                        raise Exception("{} not allowed in search_kwargs. Only {} are allowed".format(
                            kwargs__list[2], self.allowed_predicates_list))
                    query_string += ".{0}({1}, {2}({3}))".format(kwargs__list[0],
                                                                 kwargs__list[1],
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
                raise Exception("{} not allowed in search_kwargs. Only {} are allowed".format(
                    kwargs__list[2], self.allowed_predicates_list))
        return query_string

    def generate_gremlin_query_for_properties(self, **property_kwargs):
        """

        :param property_kwargs: key, value pairs for properties
        :return:
        """
        query_string = ""
        for k, v in property_kwargs.items():
            query_string += ".property({k},{v})".format(k=self.check_if_str(k), v=self.check_if_str(v))
        return query_string

    @staticmethod
    def check_if_str(s):
        if type(s) is str:
            return '"{}"'.format(s)
        return s
