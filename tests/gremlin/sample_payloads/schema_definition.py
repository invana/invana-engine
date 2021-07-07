


planet_schema = """

planet = mgmt.makeVertexLabel('Planet').make()
name = mgmt.makePropertyKey('name').dataType(String.class).cardinality(Cardinality.SET).make()
birthDate = mgmt.makePropertyKey('birthDate').dataType(Long.class).cardinality(Cardinality.SINGLE).make()
mgmt.addProperties(person, name, birthDate)
mgmt.commit()


"""
