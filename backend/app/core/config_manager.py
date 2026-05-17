CLIENT_CONFIGS = {
    'cda_standard': {
        'active_sources': ['runt', 'simit', 'procuraduria', 'registraduria'],
        'priority': 'high',
        'webhook': 'https://api.cda.com/callback'
    },
    'seguros_bogota_master': {
        'active_sources': ['runt', 'simit', 'procuraduria', 'bdme', 'policia', 'sisben', 'libreta_militar', 'contraloria'],
        'priority': 'critical',
        'webhook': 'https://compliance.cloud/notify'
    }
}

def get_active_connectors(client_id):
    config = CLIENT_CONFIGS.get(client_id, CLIENT_CONFIGS['cda_standard'])
    return config['active_sources']
