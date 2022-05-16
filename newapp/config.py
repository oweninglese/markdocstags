import os
app = {}

app['db'] = 'docs.db'
app['SECRET_KEY'] = os.environ.get("MDKEY", "")
app['base_dir'] = 'os.path.abspath(os.path.dirname(__file__))'
app['debug'] = 'True'
app['TAGSFILE'] = 'tags.csv'
app['TopicsDir'] = "./docs/tags/"
app['ArticlesDir'] = "./docs/"
app['TAGS'] = ''
app['schema'] = 'schema.sql'
