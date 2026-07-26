import pymysql

pymysql.install_as_MySQLdb()

import django.db.backends.mysql.base
from django.db.backends.mysql.features import DatabaseFeatures

django.db.backends.mysql.base.DatabaseWrapper.check_database_version_supported = lambda self: None

DatabaseFeatures.can_return_columns_from_insert = False
DatabaseFeatures.can_return_rows_from_bulk_insert = False