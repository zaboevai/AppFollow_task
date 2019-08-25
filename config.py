import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'news.db')
    SQLALCHEMY_DATABASE_URI = "postgres://ndfmuenfatvxmb:9fb40770e7922c4a3e73535d0658def58b9b9e8f646f84e492deeae55a071d61@ec2-54-247-96-169.eu-west-1.compute.amazonaws.com:5432/d7udk7olnqbhb6"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
