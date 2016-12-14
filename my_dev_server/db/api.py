from my_dev_server.db import base


def add_values_to_table(table, dict_of_values):
    db = base.Connect()
    insert = table.insert()
    #clause = db.metadata.tables.slams.insert().values(name='Wimbledon', country='United Kingdom')
    db.connection.execute(insert, [dict_of_values])
