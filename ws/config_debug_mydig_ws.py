import logging
import os
import base64

print('config_debug_mydig_ws.py is here')

config = {
    # if it's True, two daemon threads (one by flask, one by flask spawn) in mydig
    # will overwrite the same status file, which will cause a conflict
    'debug': False,
    'server': {
        'host': '0.0.0.0',
        'port': 9879,
    },
    'repo': {
        'local_path': '{}'.format(os.getenv('DIG_PROJECTS_DIR_PATH', '/shared_data/projects')),
        'git': {
            'enable_sync': False,
            'remote_url': 'https://github.com/<user_name>/<repo_name>.git',
        }
    },
    'logging': {
        'name': 'mydig-webservice.log',  # name of logger
        'file_path': None,
        'format': '%(asctime)s [%(levelname)s] %(message)s',
        'level': logging.INFO,
        'werkzeug': logging.WARNING
    },
    'es': {
        'sample_url': 'http://{}:{}/es/'.format(os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_DOCKER', '12497')),
        'full_url': 'http://{}:{}/es/'.format(os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_DOCKER', '12497')),
    },
    'etk': {
        'path': '/app/etk',
        'conda_path': '/app/miniconda/bin/',
        'daemon': {
            'host': 'localhost',
            'port': 12121
        },
        # 'number_of_processes': 8
    },
    'etl': {
        'url': 'http://{}:{}/dig_etl_engine/'.format(os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_DOCKER', '12497')),
        'number_of_workers': int(os.getenv('NUM_ETK_PROCESSES', '4')),
        'timeout': 20
    },
    'kafka': {
        'servers': ['{}:9092'.format(os.getenv('DOMAIN', 'localhost'))]
    },
    'sandpaper': {
        'url': "http://{}:{}".format(os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_SANDPIPER', '9876')),
        'ws_url': 'http://{}:{}/internal'.format(os.getenv('HOST_ON_DOCKER_DOMAIN', 'host.docker.internal'), os.getenv('PORT_BACKEND', '9879')),  # This is how Sandpaper sees the backend
        'es_url': 'http://elasticsearch:9200',  # This is how Sandpaper sees Elasticsearch
    },
    'users': {
        'admin': '123'  # basic YWRtaW46MTIz
    },
    'frontend': {
        'host': '0.0.0.0',
        'port': 9880,
        'debug': True,
        'frontend_url': 'http://{}:{}/'.format(
            os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_FRONTEND', '9880')), 
        'backend_url': 'http://{}:{}/'.format(
            os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_BACKEND', '9879')),
        'landmark_url': 'http://{}:{}/landmark/'.format(
            os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_DOCKER', '12497')),  # add slash at the end
        'digui_url': 'http://{}:{}/dig-ui/search.html'.format(
            os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_DOCKER', '12497')),
        'kibana_url': 'http://{}:{}/kibana/'.format(
            os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_DOCKER', '12497')),
        'spacy_ui_url': 'http://{}:{}/mydig/spacy_ui/'.format(
            os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_DOCKER', '12497')),
        'spacy_backend_sever_name_base64': base64.b64encode('{}:{}/mydig'.format(
            os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_DOCKER', '12497')).encode('utf-8')),
        'spacy_backend_auth_base64': base64.b64encode('{}:{}'.format(
            os.getenv('DIG_AUTH_USER', 'admin'), os.getenv('DIG_AUTH_PASSWORD', '123')).encode('utf-8'))
    },
    'landmark': {
        'create': 'http://landmark-rest:5000/project/create_from_dig/{project_name}',
        'export': 'http://landmark-rest:5000/project/export/{project_name}',
        'import': 'http://landmark-rest:5000/project/import/{project_name}'
    },
    'ache': {
        'enable': len(os.getenv('ADDON_ACHE', '')) != 0,
        'kafka_topic': 'ache',
        'group_id': 'mydig',
        'upload': {
            'endpoint': 'http://{}:{}/projects/{{project_name}}/data?sync=true&log=false'.format(os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_BACKEND', '9879')),
            'file_name': 'ache',  # file name in data folder
            # send to endpoint when get more than max_size or max_wait_time
            # 'max_size': 10, # 10 docs
            # 'max_wait_time': 10 * 1000, # 10s, float('inf')
        }
    },
    'rss_feed_crawler': {
        'enable': len(os.getenv('ADDON_RSS_FEED_CRAWLER', '')) != 0,
        'kafka_topic': 'rss',
        'group_id': 'mydig',
        'upload': {
            'endpoint': 'http://{}:{}/projects/{{project_name}}/data?sync=true&log=false'.format(os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_BACKEND', '9879')),
            'file_name': 'rss'
        }
    },
    'external_crawler': {
        'kafka_topic': 'crawler',
        'group_id': 'mydig',
        'upload': {
            'endpoint': 'http://{}:{}/projects/{{project_name}}/data?sync=true&log=false'.format(os.getenv('DOMAIN', 'localhost'), os.getenv('PORT_BACKEND', '9879')),
            'file_name': 'crawler'
        },
        'default_project': os.getenv('DEFAULT_EXTERNAL_CRAWLER_PROJECT', 'crawler')
    },
    'data_pushing_worker_backoff_time': 5,
    'status_memory_dump_backoff_time': 5,
    'catalog_memory_dump_backoff_time': 5,
    'project_name_blacklist': ('logs', 'dig-logs', 'dig-states', 'dig-profiles', '.kibana', 'crawler'),
    'database_url': 'sqlite:///app.db',
    'default_glossary_dicts_path': '/shared_data/dig3-resources/builtin_resources',
    'default_glossaries_path': '/shared_data/dig3-resources/glossaries',
    'default_spacy_rules_path': '/shared_data/dig3-resources/custom_spacy_rules'
}
