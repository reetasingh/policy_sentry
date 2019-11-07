import click
import pprint
import json
from policy_sentry.shared.query import query_condition_table, query_condition_table_by_name, query_arn_table, \
    query_arn_table_by_name, query_action_table, query_action_table_by_name
from policy_sentry.shared.database import connect_db
from pathlib import Path

HOME = str(Path.home())
CONFIG_DIRECTORY = '/.policy_sentry/'
DATABASE_FILE_NAME = 'aws.sqlite3'
database_file_path = HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME

@click.command(
    short_help="Allow users to query the action, arn, and condition tables from command line."
)
@click.option(
    '--table',
    type=click.Choice(['action', 'arn', 'condition']),
    required=True,
    help='The table to query. Accepted values are action, arn, or condition.'
)
@click.option(
    '--service',
    type=str,
    required=True,
    help="Filter according to AWS service."
)
@click.option(
    '--name',
    type=str,
    required=False,
    help='Name of the action, arn type, or condition key. Optional.'
)
# TODO: Ask Matty about how to handle Click context
#  so we can have different options for filtering based on which table the user selects
def query(table, service, name):
    """Allow users to query the action tables, arn tables, and condition keys tables from command line."""
    db_session = connect_db(database_file_path)
    if table == 'condition':
        if name is None:
            condition_results = query_condition_table(db_session, service)
            for item in condition_results:
                print(item)
        else:
            output = query_condition_table_by_name(db_session, service, name)
            print(json.dumps(output, indent=4))
    elif table == 'arn':
        if name is None:
            raw_arns = query_arn_table(db_session, service)
            for item in raw_arns:
                print(item)
        else:
            output = query_arn_table_by_name(db_session, service, name)
            print(json.dumps(output, indent=4))
    elif table == 'action':
        if name is None:
            action_list = query_action_table(db_session, service)
            for item in action_list:
                print(item)
        else:
            output = query_action_table_by_name(db_session, service, name)
            print(json.dumps(output, indent=4))
    else:
        print("Table name not valid.")
