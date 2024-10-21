from invana_engine.contribs.importers import JSONImporter
from invana_engine.graph import InvanaGraph
import os

invana = InvanaGraph()
invana.drop()
importer = JSONImporter(os.path.join(os.getcwd(), "sample-data/hello-world/"), invana)
importer.start()