import ConfigParser

conf_variables = ConfigParser.ConfigParser()
conf_variables.add_section('config')
conf_variables.add_section('phpipam')
conf_variables.add_section('test variables')
conf_variables.set('config', 'url', raw_input('url'))
conf_variables.set('phpipam', 'username', raw_input('username'))
conf_variables.set('phpipam', 'password', raw_input('password'))
conf_variables.set('test variables', 'single result', raw_input('phpipam keyword which should only pull up one result'))
conf_variables.set('test variables', 'no result', raw_input('phpipam keyword which should not find any results'))
conf_variables.set('test variables', 'many results', raw_input('phpipam keyword which should find many results'))
conf_variables.set('test variables', 'search result', raw_input('phpipam keyword which should find atleast one result '
                                                                'in the search page'))
conf_variables.set('test variables', 'device result', raw_input('phpipam keyword which should find atleast one result '
                                                                'in the device page'))
with open('variables.cfg', 'w') as f:
    conf_variables.write(f)

