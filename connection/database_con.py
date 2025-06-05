from mysql.connector import connect, Error
import os
import utils.utils as ut

def execute_request(operation, params, fetch = False) :
    result = None
    try :
        with connect(
            host=ut.config['paths']['DB_HOST'],
            user=ut.config['paths']['DB_USER'],
            password=ut.config['paths']["DB_PASSWORD"],
            database=ut.config['paths']['DB_NAME']
        ) as connection:
            with connection.cursor() as cur:
                cur.execute(operation, params)
                if fetch :
                    result = cur.fetchall()
            connection.commit()
    except Error as e:
        print(e)
    return result


def add_user(telegram_id, telegram_name) :
    execute_request(f"INSERT INTO users (telegram_id, telegram_user_name)"
                            f" VALUES (%s, %s)", (telegram_id, telegram_name))
    user_id = get_full_info(telegram_id)[-1][0]
    execute_request(f"INSERT INTO selected_users (user_id, selected_user_id)"
                            f" VALUES (%s, %s)", (user_id, 1))

def update_user_name(telegram_id, new_user_name) :
    execute_request(f'UPDATE users SET user_name = %s WHERE telegram_id = %s', params=(new_user_name, telegram_id))
def update_user_photo(telegram_id, photo):
    execute_request(
        "UPDATE users SET photo = %s WHERE telegram_id = %s",
        (photo, telegram_id)
    )


def update_user_description(telegram_id, description):
    execute_request(
        "UPDATE users SET description = %s WHERE telegram_id = %s",
        (description, telegram_id)
    )


def get_genres():
    return execute_request("SELECT * FROM genres", (), fetch=True)

def update_genre(telegram_id, genre_id):
    execute_request(
        "UPDATE users SET genre = %s WHERE telegram_id = %s",
        (genre_id, telegram_id)
    )


def update_genre_like(telegram_id, genre_like_id):
    execute_request(
        "UPDATE users SET genre_like = %s WHERE telegram_id = %s",
        (genre_like_id, telegram_id)
    )

def update_age(telegram_id, age):
    execute_request(
        "UPDATE users SET age = %s WHERE telegram_id = %s",
        (age, telegram_id)
    )

def update_country(telegram_id, country):
    execute_request(
        "UPDATE users SET country = %s WHERE telegram_id = %s",
        (country, telegram_id)
    )


def get_full_info(telegram_id):
    return execute_request("""
        SELECT 
            u.ID, u.telegram_id, u.telegram_user_name, u.user_name,
            g1.genre AS genre, g2.genre AS genre_like,
            u.description, u.photo, u.age, u.country
        FROM users u
        LEFT JOIN genres g1 ON u.genre = g1.ID
        LEFT JOIN genres g2 ON u.genre_like = g2.ID
        WHERE u.telegram_id = %s
    """, (telegram_id,), fetch=True)

def get_full_info_with_user_id(user_id):
    return execute_request("""
        SELECT 
            u.ID, u.telegram_id, u.telegram_user_name, u.user_name,
            g1.genre AS genre, g2.genre AS genre_like,
            u.description, u.photo, u.age, u.country
        FROM users u
        LEFT JOIN genres g1 ON u.genre = g1.ID
        LEFT JOIN genres g2 ON u.genre_like = g2.ID
        WHERE u.ID = %s
    """, (user_id,), fetch=True)

def set_selected_user_request(user_id, next_user_id) :
    execute_request('UPDATE selected_users SET selected_user_id = %s WHERE user_id = %s',
                    (next_user_id, user_id))

def get_profile_of_selected_user(telegram_id) :
    return  execute_request("SELECT * FROM users "
        "WHERE ID IN (SELECT selected_user_id FROM selected_users "
        "WHERE user_id IN (SELECT ID FROM users WHERE telegram_id =%s))", (telegram_id,), fetch=True)

#compare genres
def is_user_suitable(user, to_user):
    return user[-1][5] == to_user[-1][4]
def get_next_profile(telegram_id):
    users = execute_request("SELECT * FROM users", (), fetch=True)
    if not users:
        return None

    user_request_list = execute_request(
        "SELECT * FROM users WHERE telegram_id = %s",
        (telegram_id,),
        fetch=True
    )
    if not user_request_list or len(user_request_list) == 0:
        return None
    user_request = user_request_list[0]

    selected_user_list = get_profile_of_selected_user(telegram_id)
    current_selected_id = selected_user_list[0][0] if selected_user_list else 0

    user_count = len(users)
    counter = 0
    for i, user in enumerate(users):
        if user[0] == current_selected_id:
            counter = i + 1
            break

    start_index = counter
    looped = False

    while True:
        if counter >= user_count:
            if looped:
                return None
            counter = 0
            looped = True

        user = users[counter]
        if user[1] == telegram_id:
            counter += 1
            continue

        if user_request[5] == user[4]:  # genre_like == genre
            set_selected_user_request(user_request[0], user[0])
            return get_full_info_with_user_id(user[0])

        counter += 1
        if counter == start_index and looped:
            break
    return None

def request_user_like(telegram_id, is_like) :
    user = get_full_info(telegram_id)
    selected_user = get_full_info(get_profile_of_selected_user(telegram_id)[0][1])
    if not is_like :
        execute_request("DELETE FROM like_request WHERE user_id = %s AND like_user_id = %s",
                        (user[0][0], selected_user[0][0]))
    else :
        execute_request("INSERT INTO like_request (user_id, like_user_id) VALUES (%s, %s)",
                        (user[0][0], selected_user[0][0]))
    return {'user' : user, 'liked_user' : selected_user}

def delete_request_likes(telegram_id) :
    user = get_full_info(telegram_id)
    execute_request("DELETE FROM like_request WHERE like_user_id = %s",
                        (user[0][0],))


def create_session(from_user_id, to_user_id):
    with connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")

    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO sessions (from_user_id, to_user_id) VALUES (%s, %s)",
                (from_user_id, to_user_id)
            )
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            session_id = result[0] if result else None
            conn.commit()
            return session_id

def get_reacted_users(telegram_id) :
    user_id = get_full_info(telegram_id)[0][0]
    return execute_request("SELECT * FROM users WHERE ID IN (SELECT user_id FROM like_request WHERE like_user_id = %s)",
                           (user_id,), fetch=True)

def stop_session(from_user_id) :
    pass

def react_to_like(user_id, liked_user, is_like) :
    if is_like :
        pass
    execute_request("DELETE FROM like_request WHERE user_id = %s AND like_user_id = %s",
                    (liked_user, user_id))

def get_session(from_user_id):
    return execute_request(""
                           "SELECT * FROM sessions WHERE from_user_id = %s", (from_user_id,), fetch=True)

def remove_all_session_with(user_id) :
    execute_request("DELETE FROM sessions WHERE from_user_id = %s", (user_id,))