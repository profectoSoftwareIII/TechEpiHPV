import psycopg2
import psycopg2.extras


def DataBaseConnection():
    conn = None
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="hpv_safe",
            user="root",
            password="1234")

        return conn
    except psycopg2.OperationalError as err:
        print(err)
        conn.close()


def run_query(query='', data=any):
    conn = DataBaseConnection()
    cursor = conn.cursor()
    print(query, data)
    cursor.execute(query, data)

    columns = list(cursor.description)

    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()
    else:
        conn.commit()
        data = None

    results = []
    for row in data:
        row_dict = {}
        for i, col in enumerate(columns):
            row_dict[col.name] = row[i]
        results.append(row_dict)

    cursor.close()
    conn.close()

    return results
