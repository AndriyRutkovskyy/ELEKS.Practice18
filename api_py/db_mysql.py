import MySQLdb


class Database(object):

    __instance = None
    __host = None
    __user = None
    __password = None
    __database = None
    __session = None
    __connection = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Database, cls).__new__(cls)
        return cls.__instance
    # End def __new__

    def __init__(self, host='localhost', user='root', password='', database=''):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
    # End def __init__

    def __open(self):
        try:
            cnx = MySQLdb.connect(self.__host, self.__user, self.__password, self.__database)
            self.__connection = cnx
            self.__session = cnx.cursor()
        except MySQLdb.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
    # End def __open

    def __close(self):
        self.__session.close()
        self.__connection.close()
    # End def __close

    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(["%s"]*len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()
        self.__close()

        return self.__session.lastrowid
    # End def insert

    def select(self, table, where=None, join=None, *args, **kwargs):
        # result = None
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += "`"+key+"`"
            if i < l:
                query += ","
        # End for keys

        query += 'FROM %s' % table

        if join:
            query += " JOIN %s" % join
        # End if join

        if where:
            query += " WHERE %s" % where
        # End if where

        self.__open()
        self.__session.execute(query, values)

        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            query_res = [item for item in self.__session.fetchall()]
        else:
            query_res = [item[0] for item in self.__session.fetchall()]

        result = []

        columns = [desc[0] for desc in self.__session.description]

        for row in query_res:
            row = dict(zip(columns, row))
            result.append(row)

        self.__close()

        return result
    # End def select

    def delete(self, table, where=None, *args):
        query = "DELETE FROM %s" % table
        if where:
            query += ' WHERE %s' % where

        values = tuple(args)

        try:
            self.__open()
            self.__session.execute(query, values)
            self.__connection.commit()

            delete_rows = self.__session.rowcount
            self.__close()

            return delete_rows
        #

        except MySQLdb.Error as e:
            return "Error %d: %s" % (e.args[0], e.args[1])
    # End def delete
# End def __close
