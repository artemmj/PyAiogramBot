from sqlalchemy import Integer, String

from settings import pg_manager


async def create_table_users(table_name='users_reg'):
    async with pg_manager:
        columns = [
            {'name': 'user_id',    'type': Integer, "options": {"primary_key": True, "autoincrement": False}},
            {'name': 'gender',     'type': String},
            {'name': 'age',        'type': Integer},
            {'name': 'full_name',  'type': String},
            {'name': 'user_login', 'type': String},
            {'name': 'photo',      'type': String},
            {'name': 'about',      'type': String},
            {'name': 'date_reg',   'type': String},
        ]
        await pg_manager.create_table(table_name=table_name, columns=columns)


async def get_user_data(user_id: int, table_name='users_reg'):
    async with pg_manager:
        user_info = await pg_manager.select_data(table_name=table_name, where_dict={'user_id': user_id}, one_dict=True)
        if user_info:
            return user_info
        return None


async def insert_user(user_data: dict, table_name='users_reg'):
    async with pg_manager:
        await pg_manager.insert_data_with_update(table_name=table_name, records_data=user_data, conflict_column='user_id')
