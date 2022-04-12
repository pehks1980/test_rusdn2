from datetime import date
import aiomysql
import os.path
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.locks
import tornado.options
import tornado.web

from tornado.escape import json_decode
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("db_host", default="192.168.1.204", help="mysql database host")
define("db_port", default=3306, help="mysql database port")
define("db_database", default="task2", help="mysql database name")
define("db_user", default="task2user", help="mysql database user")
define("db_password", default="task2passwd", help="mysql task2user password")

"""
execute_ddl - exec DDL schema.sql for this app
"""


async def execute_ddl(pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 42;")
            #print(cur.description)
            print("connected to mysql ok.")
            # (r,) = await cur.fetchone()
            # assert r == 42
            with open("schema.sql") as f:
                schema = f.read()
                await cur.execute(schema)
                vals = ("aaa", "bbb")
                await cur.execute("INSERT INTO task2values (valkey, val) VALUES (%s, %s);", vals)



class NoResultError(Exception):
    pass


"""
App - application class has routes, some settings, and connection to db pool (aiomysql)
"""


class Application(tornado.web.Application):
    def __init__(self, db):
        self.db = db
        handlers = [
            (r"/", HomeHandler),
            (r"/values", ValuesHandler),
            (r"/values/([^/]+)", ValuesHandler),
        ]
        settings = dict(
            title="Tornado Async Server",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
        )
        super().__init__(handlers, **settings)


"""
BaseHandler - subclass has some api to interact to sql db side
"""


class BaseHandler(tornado.web.RequestHandler):
    """
    execute a query (direct)
    """

    async def execute(self, stmt, *args):
        async with self.application.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(stmt, args)

    async def query(self, stmt, *args):
        """
        make a query and get some results as list of dicts for each row
        """
        async with self.application.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(stmt, args)
        # make answer as list of dicts for each row
        lines = []
        for row in await cur.fetchall():
            # print(row)
            obj = {}
            for val, desc in zip(row, cur.description):
                obj[desc[0]] = val
            lines.append(obj)
        return lines

    async def queryone(self, stmt, *args):
        """
        Query for exactly one result.
        """
        results = await self.query(stmt, *args)
        if len(results) == 0:
            # raise NoResultError()
            return None
            # raise ValueError("Expected result, got nothing")
        elif len(results) > 1:
            raise ValueError("Expected 1 result, got %d" % len(results))
        return results[0]


class HomeHandler(BaseHandler):
    """
    Get Home /
    """

    async def get(self):
        response = {'message': "Hello world",
                    'release_date': date.today().isoformat()}
        self.write(response)


class ValuesHandler(BaseHandler):
    """
    Get /values/{id}
    """

    async def get(self, value_id):
        value = await self.queryone("SELECT * FROM task2values WHERE id = %s", value_id)
        self.set_header("Content-Type", "application/json")
        if not value:
            response = {
                'message': 'value not found'
            }
        else:
            response = {
                f"{value['valkey']}": value['val'],
            }
        self.write(response)

    """
    POST /values
    """

    async def post(self):
        data = json_decode(self.request.body)
        vals = list(data.items())
        vals = vals[0]
        await self.execute("INSERT INTO task2values (valkey, val) VALUES (%s, %s);", vals[0], vals[1])
        self.set_header("Content-Type", "application/json")
        response = {}
        self.write("OK")
        self.write(response)


"""
main loop - setups server, creates conn pool to mysql db
"""


async def main():
    tornado.options.parse_command_line()
    # Create the global connection pool.
    print(f"connecting to mysql server {options.db_host}:{options.db_port}...")
    async with aiomysql.create_pool(
            host=options.db_host,
            port=options.db_port,
            user=options.db_user,
            password=options.db_password,
            db=options.db_database,
            autocommit=True,
    ) as db:
        await execute_ddl(db)
        app = Application(db)
        app.listen(options.port)
        print(f"server started at 127.0.0.1:{options.port}")
        shutdown_event = tornado.locks.Event()
        await shutdown_event.wait()
        db.close()
        await db.wait_closed()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    tornado.ioloop.IOLoop.current().run_sync(main)
