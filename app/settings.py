from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env.str('SECRET_KEY', '')
GOOGLE_API_KEY = env.str('GOOGLE_API_KEY', '')
DATABASE_URL = env.str('DATABASE_URL', 'sqlite://db.sqlite3')
