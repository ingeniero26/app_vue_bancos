from distutils.debug import DEBUG


class DevelopmentConfig():
    DEBUG:True
    MYSQL_HOST='34.75.68.76'
    MYSQL_USER='jbatistav'
    MYSQL_PASSWORD='Hardware100.'
    MYSQL_DB='jbatistav'
    
config = {
    'development':DevelopmentConfig
}