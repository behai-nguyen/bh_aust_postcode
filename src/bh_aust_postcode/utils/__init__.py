"""
Some generic helper functions.
"""

from flask import current_app as app

def print_log(logger: object, msg: str, cateogry: str):
    """Print to stdout and log to file a message. 

    :param object logger: the actual logger instance.
    :param str msg: the message to print and to log.
    :param str cateogry: the logging cateogry -- info, debug, error, exception.
    """

    print(msg)
    method = getattr(logger, cateogry, None)
    method(msg)

def format_sql_statement(sql: str) -> str:
    """Complete a SQL statement with schema name and table name.

    :param str sql: SQL statement with postional format {0} and {1}.

    :return: complete SQL statement.
    :rtype: str.
    """

    schema_name = app.config['SCHEMA_NAME']
    postcode_table_name = app.config['POSTCODE_TABLE_NAME']
    
    return sql.format(schema_name, postcode_table_name)