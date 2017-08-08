from django.db import connection, transaction
from django.utils.decorators import ContextDecorator


class count_queries(ContextDecorator):
    def __enter__(self):
        self.start_len = len(connection.queries)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            return
        self.end_len = len(connection.queries)
        count = self.end_len - self.start_len
        print('{} quer{} executed'.format(
            count,
            'y' if count == 1 else 'ies',
        ))


class Rollback(ContextDecorator):
    def __enter__(self):
        self.atomic = transaction.atomic()
        self.atomic.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        transaction.set_rollback(True)
        self.atomic.__exit__(None, None, None)


def rollback(func=None):
    if func:
        return Rollback()(func)
    return Rollback()
