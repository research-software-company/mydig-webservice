import copy
import default_resources


def get(name):
    return copy.deepcopy(eval(name))

project = {
    'master_config': {}, # master_config
    'entities': {}, # 'kg-id': entity
    'field_annotations': {},
    'data': {} # tlds -> meta data
}

master_config = {
    'configuration': copy.deepcopy(default_resources.default_configuration) \
        if hasattr(default_resources, 'default_configuration') else {},
    'table_attributes': {},
    'glossaries': copy.deepcopy(default_resources.default_glossaries) \
        if hasattr(default_resources, 'default_glossaries') else {},
    'glossary_dicts': copy.deepcopy(default_resources.default_glossary_dicts) \
        if hasattr(default_resources, 'default_glossary_dicts') else {},
    'root_name': 'ads',
    'sources': [],
    'fields': copy.deepcopy(default_resources.default_fields) \
        if hasattr(default_resources, 'default_fields') else {},
    'tags': copy.deepcopy(default_resources.default_tags) \
        if hasattr(default_resources, 'default_tags') else {},
    'index': {
        'sample': '',
        'full': '',
        'version': 0
    },
    'image_prefix': ''
}

# field_annotations = {
#     kg_id: {
#         field_name: {
#             key: {
#                 'human_annotation': 0/1
#             }
#         }
#     },
# }


# entities = {
#     entity_name: {
#         kg_id: {
#             tag_name: {
#                 'human_annotation': 0/1
#             }
#         }
#     }
# }

# table_attribute = {
#     'name': 'attribute_name_1',
#     'field_name': '',
#     'value': [],
#     'info': {}
# }

# entity = {
# }
#
# tag = {
#     'name': 'name',
#     'description': '',
#     'screen_label': 'show on the screen',
#     'include_in_menu': False,
#     'positive_class_precision': 0.0,
#     'negative_class_precision': 0.0
# }

# field = {
#     'name': 'same as the key',
#     'screen_label': 'show on the screen',
#     'screen_label_plural': 'screen label plural',
#     'description': 'whatever',
#     'type': 'enum(string | location | username | date | email | hyphenated | phone | image)',
#     'show_in_search': True,
#     'show_in_facets': True,
#     'show_as_link': 'enum(text | entity)',
#     'show_in_result': 'enum(header | detail | no | title | description)',
#     'color': 'enum(...)',
#     'icon': 'enum(...)',
#     'search_importance': 1, # (integer range in [1, 10])
#     'use_in_network_search': True
#     'group_name': string optional,
#     'combine_fields': boolean, optional
#     'glossaries': [], optional,
#     'rule_extractor_enabled': boolean,
#     'number_of_rules': integer,
#     'predefined_extractor': 'enum (social_media | review_id | city | posting_date | phone | email | address |
#      country | TLD | none)',
#     'rule_extraction_target': enum('title_only', 'description_only', 'title_and_description'),
#     'case_sensitive': boolean
# }