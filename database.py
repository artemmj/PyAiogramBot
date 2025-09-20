from sqlalchemy import BigInteger, Integer, String

from settings import pg_manager


async def create_table_users(table_name='users_reg'):
    async with pg_manager:
        columns = [
            {'name': 'user_id',       'type': BigInteger, "options": {"primary_key": True, "autoincrement": False}},
            {'name': 'gender',        'type': String},
            {'name': 'age',           'type': Integer},
            {'name': 'full_name',     'type': String},
            {'name': 'user_login',    'type': String},
            {'name': 'photo',         'type': String},
            {'name': 'about',         'type': String},
            {'name': 'date_reg',      'type': String},
            {'name': 'refer_id',      'type': Integer},
            {'name': 'count_refer',   'type': Integer},
        ]
        await pg_manager.create_table(table_name=table_name, columns=columns)


async def get_all_users(table_name='users_reg', count=False):
    async with pg_manager:
        all_users = await pg_manager.select_data(table_name=table_name)
        if count:
            return len(all_users)
        return all_users


async def get_user_data(user_id: int, table_name='users_reg'):
    async with pg_manager:
        return await pg_manager.select_data(
            table_name=table_name,
            where_dict={'user_id': user_id},
            one_dict=True,
        )


# async def insert_user(user_data: dict, table_name='users_reg'):
#     async with pg_manager:
#         await pg_manager.insert_data_with_update(
#             table_name=table_name,
#             records_data=user_data,
#             conflict_column='user_id',
#         )


async def insert_user(user_data: dict, table_name='users_reg'):
    async with pg_manager:
        await pg_manager.insert_data_with_update(
            table_name=table_name,
            records_data=user_data,
            conflict_column='user_id',
        )
        if user_data.get('refer_id'):
            refer_info = await pg_manager.select_data(
                table_name=table_name,
                where_dict={'user_id': user_data.get('refer_id')},
                one_dict=True,
                columns=['user_id', 'count_refer'],
            )
            await pg_manager.update_data(
                table_name=table_name,
                where_dict={'user_id': refer_info.get('user_id')},
                update_dict={'count_refer': refer_info.get('count_refer') + 1},
            )
