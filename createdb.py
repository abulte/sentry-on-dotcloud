import MySQLdb
import psycopg2

from sentry_conf import DATABASES

def create_dbs():
    print("create_dbs: let's go.")
    print("create_dbs: got settings.")
    for name, db in DATABASES.iteritems():
        host = db['HOST']
        user = db['USER']
        password = db['PASSWORD']
        port = db['PORT']
        db_name = db['NAME']
        db_type = db['ENGINE']
        # see if it is mysql
        if db_type.endswith('mysql'):
            print 'creating database %s on %s' % (db_name, host)
            db = MySQLdb.connect(user=user,
                                passwd=password,
                                host=host,
                                port=port)
            cur = db.cursor()
            print("Check if database is already there.")
            cur.execute("""SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
                         WHERE SCHEMA_NAME = %s""", (db_name,))
            results = cur.fetchone()
            if not results:
                print("Database %s doesn't exist, lets create it." % db_name)
                sql = """CREATE DATABASE IF NOT EXISTS %s """ % (db_name,)
                print("> %s" % sql)
                cur.execute(sql)
                print(".....")
            else:
                print("database already exists, moving on to next step.")
        # see if it is postgresql
        elif db_type.endswith('postgresql_psycopg2'):
            print 'creating database %s on %s' % (db_name, host)
            con = psycopg2.connect(host=host, user=user, password=password, port=port, database='postgres')
            con.set_isolation_level(0)
            cur = con.cursor()
            try:
                cur.execute('CREATE DATABASE %s' % db_name)
            except psycopg2.ProgrammingError as detail:
                print detail
                print 'moving right along...'
        else:
            print("ERROR: {0} is not supported by this script, you will need to create your database by hand.".format(db_type))


if __name__ == '__main__':
    print("create_dbs start")
    create_dbs()
    print("create_dbs all done")
