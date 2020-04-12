from app_base import *

from search.conjunctive_query import ConjunctiveQueryProcessor
from search.event_query import EventQueryProcessor
from basic_auth import get_logged_in_user


@api.route('/projects/<project_name>/search/<type>')
class Search(Resource):
    @requires_auth
    def get(self, project_name, type):
        if project_name not in data:
            user = get_logged_in_user()
            return project_name_not_found(project_name, user)
        logger.error('API Request received for %s' % (project_name))

        es = ES(config['es']['sample_url'])
        myargs = request.args
        if type == 'conjunctive':
            query = ConjunctiveQueryProcessor(project_name,
                                              data[project_name]['master_config']['fields'],
                                              data[project_name]['master_config']['root_name'], es, myargs=myargs)
            return query.process()
        elif type == 'event':
            query = EventQueryProcessor(project_name,
                                        data[project_name]['master_config']['fields'],
                                        data[project_name]['master_config']['root_name'], es, myargs=myargs)
            return query.process_event_query()
        elif type == 'time_series':

            query = EventQueryProcessor(project_name,
                                        data[project_name]['master_config']['fields'],
                                        data[project_name]['master_config']['root_name'], es, myargs=myargs)
            return query.process_ts_query()
        else:
            return rest.not_found('invalid search type')
