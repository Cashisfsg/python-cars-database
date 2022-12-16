import sqlite3
from data import get_brand, get_model, get_year, get_price

# =======================Имя файла=================================
DB = 'cars.db'
# ==============Количество записей в таблице=======================
AMOUNT_OF_RECORDS = 100


def ensure_connection(sqlite_query):
    def query(*args, **kwargs):
        try:
            print('Connection to database')
            with sqlite3.connect(DB, timeout=20) as sqlite_connection:
                print('Connection to SQLite database successfully established')
                response = sqlite_query(connection=sqlite_connection, *args, **kwargs)
            return response
        except Exception as ex:
            print(f'Error while connecting to database: \'{ex}\'')
        finally:
            print('The SQLite connection is closed\n')
    return query


@ensure_connection
def init_db(connection):
    cursor = connection.cursor()

    cursor.execute('SELECT sqlite_version();')
    (version, ) = cursor.fetchone()
    print(f'SQLite Database version is: {version}')

    cursor.execute(f'DROP TABLE IF EXISTS cars;')
    cursor.execute(f'''
        CREATE TABLE cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT,
        model TEXT,
        year INTEGER,
        price FLOAT
    );
    ''')
    connection.commit()
    print('Database created and Successfully connected to SQLite')


@ensure_connection
def set_data(connection):
    cursor = connection.cursor()
    cursor.executemany('''
        INSERT INTO cars (brand, model, year, price)
        VALUES (?, ?, ?, ?);
    ''', ((get_brand(), get_model(), get_year(), get_price(), ) for _ in range(AMOUNT_OF_RECORDS)))
    connection.commit()
    print('Data successfully added into the database')


@ensure_connection
def select_all_ordered_by_price(connection):
    cursor = connection.cursor()
    response = cursor.execute('''
        SELECT brand, model, year, price
        FROM cars
        ORDER BY price;
    ''')
    print('Request completed successfully')
    return response


@ensure_connection
def select_all_by_price(connection, min: float = 100000, max: float = 120000):
    if min > max:
        raise ValueError('Incorrect data request')
    else:
        cursor = connection.cursor()
        response = cursor.execute(f'''
            SELECT brand, model, year, price
            FROM cars
            WHERE price BETWEEN {min} AND {max}
            ORDER BY price DESC;
        ''')
        print('Request completed successfully')
        return response


@ensure_connection
def select_all_by_brand(connection, brand: str = ''):
    cursor = connection.cursor()
    response = cursor.execute(f'''
        SELECT brand, model, year, price
        FROM cars
        WHERE brand = \'{brand}\'
        ORDER BY year DESC, price;
    ''')
    print('Request completed successfully')
    return response


@ensure_connection
def select_all_by_brand_and_year(connection, brand: str = '', year: int = 2000):
    cursor = connection.cursor()
    response = cursor.execute(f'''
        SELECT brand, model, year, price FROM (
            SELECT * FROM cars
            WHERE brand = \'{brand}\'
        ) WHERE year = {year};
    ''')
    print('Request completed successfully')
    return response


@ensure_connection
def select_amount_cars_by_brand(connection, brand: str = ''):
    cursor = connection.cursor()
    response = cursor.execute(f'''
        SELECT brand, COUNT(brand), SUM(price) 
        FROM cars
        WHERE brand = \'{brand}\';
    ''')
    print('Request completed successfully')
    return response


@ensure_connection
def update_car_price(connection, brand: str = '', model: str = '', year: int = 2000, price: float = 50000):
    cursor = connection.cursor()
    cursor.execute(f'''
        UPDATE cars
        SET price = {price}
        WHERE brand = \'{brand}\' AND model = \'{model}\' AND year = {year};
    ''')
    print('Data successfully updated')


@ensure_connection
def delete_car_from_table(connection, brand: str = '', model: str = ''):
    cursor = connection.cursor()
    cursor.execute(f'''
        DELETE FROM cars
        WHERE brand = \'{brand}\' AND model = \'{model}\';
    ''')
    print('Data successfully deleted from the table')


def main():
    init_db()
    set_data()
    print(*select_all_ordered_by_price(), sep='\n', end='\n\n')
    print(*select_all_by_price(min=50000, max=70000), sep='\n', end='\n\n')
    print(*select_all_by_brand(brand='Audi'), sep='\n', end='\n\n')
    print(*select_all_by_brand_and_year(brand='Audi', year=2022), sep='\n', end='\n\n')
    print(*select_amount_cars_by_brand(brand='Audi'), sep='\n', end='\n\n')
    update_car_price(brand='BMW', model='Rebecca NQ-37', year=1973, price=10000)
    delete_car_from_table(brand='Porsche', model='Jennifer YN-50')
    print(*select_all_ordered_by_price(), sep='\n', end='\n\n')


if __name__ == '__main__':
    main()


