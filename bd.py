import sqlite3
import csv
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

class DatabaseManager:
    """
    Комплексная система управления базой данных интернет-магазина
    с поддержкой транзакций, импорта/экспорта и оптимизации
    """
    
    def __init__(self, db_path: str = "ecommerce.db"):
        self.db_path = db_path
        self.setup_logging()
        self.init_database()
    
    def setup_logging(self):
        """Настройка логирования операций"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('database_operations.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def init_database(self):
        """Инициализация структуры базы данных"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
               
                ### БЛОК Python
                # import - использование библиотеки 
                # from import - использование конкретной библиотеки
                # class DatabaseManager: -  Создает шаблон (класс) для управления базой данных. Этот класс - "главный управляющий" базой данных. Он знает КАК работать с БД
                
                # def __init__(self, db_path: str = "ecommerce.db"): - Объявляет конструктор класса с параметрами.
                # # __init__ - специальное имя для конструктора в Python
                # # self - ссылка на сам объект (всегда первый параметр)
                # # db_path: str - параметр с указанием типа (строка)
                # # = "ecommerce.db" - значение по умолчанию
                # self.db_path = db_path - Что делает: Сохраняет путь к базе данных внутри объекта.
                # self.setup_logging() - Что делает: Вызывает метод для настройки системы логирования.
                # self.init_database() - Что делает: Вызывает метод для инициализации базы данных.
                # def setup_logging(self): - Что делает: Объявляет метод для настройки системы логирования. Вызывается автоматически в конструкторе __init__ .
                # logging.basicConfig(...) - Что делает: Настраивает основную конфигурацию логирования. Настраивает логирование для всего класса.
                # level=logging.INFO - с него будут записываться: INFO: "Создана категория: Электроника". WARNING: "Категория уже существует". ERROR: "Ошибка подключения к БД"
                # format='%(asctime)s - %(levelname)s - %(message)s' - %(asctime)s  - время события. %(levelname)s - уровень.  %(message)s   - сообщение  
                # # Результат лога: "2024-01-15 14:30:25 - INFO - Создана категория: Электроника"
                # handlers=[...] - Куда записывать логи 
                # # handlers=[ 
                # # logging.FileHandler('database_operations.log'),  # 📁 В файл
                # # logging.StreamHandler()                          # 💻 В консоль
                # # ]
                # logging.FileHandler('database_operations.log')
                # # Записывает логи в файл 'database_operations.log'
                # # Результат: создается файл с историей всех операций
                # logging.StreamHandler()
                # # Выводит логи в консоль (терминал)
                # # Результат: видите операции в реальном времени при запуске программы
                # self.logger = logging.getLogger(__name__) - Что делает: Создает объект логгера для использования в классе. 
                # # self.logger - сохраняет логгер как свойство класса
                # # __name__ - автоматическое имя модуля (файла)
                # def init_database(self): - Объявляет метод для инициализации базы данных.
                # try: - Что делает: Начало блока обработки исключений. 
                # # Без try/except - программа упадет при ошибке
                # # create_table()  # ❌ Если ошибка - программа завершится
                # with self.get_connection() as conn: - Что делает: Создает и автоматически управляет соединением с базой данных.(грубо говоря оптимизирует код)
                # self.get_connection(): - Возвращает соединение с базой данных.(conn - это активное соединение с SQLite базой данных.)
                # cursor = conn.cursor() - Что делает: Создает курсор для выполнения SQL команд. 
                # get_connection(): - Получение соединения с БД с поддержкой транзакций
                # # sqlite3.connect(self.db_path) - создает/открывает файл БД 
                # # row_factory = sqlite3.Row - позволяет обращаться к колонкам по имени
                # (Возвращает готовое соединение)
                
                ### БЛОК SQL
                # PRAGMA foreign_keys = ON; -  ЦЕЛЬ: Включение проверки целостности внешних ключей.  Без этой настройки SQLite игнорирует все FOREIGN KEY ограничения.
                # PRAGMA journal_mode = WAL; - ЦЕЛЬ: Включение современного режима журналирования. Улучшает производительность и надежность БД. Читатели не блокируют писателей и наоборот.
                #.executescript() - Метод выполнения скрипта. Выполняет несколько SQL команд одновременно. Все команды выполняются как одна транзакция.
                # cursor - Курсор базы данных. Это "указатель" для выполнения команд в БД. Как пульт управления для работы с базой данных. 
                # CREATE TABLE IF NOT EXISTS categories -Создает новую таблицу с именем "categories", но только если она еще не существует.
                # category_id INTEGER PRIMARY KEY AUTOINCREMENT - Что делает: Создает главный идентификатор категории. category_id - имя столбца. INTEGER - тип данных (целые числа). PRIMARY KEY - основной ключ таблицы. AUTOINCREMENT - автоматическая нумерация.
                # name TEXT NOT NULL UNIQUE - Что делает: Создает поле для названия категории с строгими ограничениями. name - название категории. TEXT - текстовый тип данных. NOT NULL - обязательное поле (не может быть пустым). UNIQUE - уникальное значение (не может повторяться).
                # description TEXT - Что делает: Создает поле для описания категории. TEXT - текстовый тип данных. Нет ограничений - может быть NULL, пустым, повторяться. 
                # created_at DATETIME DEFAULT CURRENT_TIMESTAMP - Что делает: Автоматически записывает дату и время создания категории. created_at - имя столбца для времени создания. DATETIME - тип данных (дата и время). DEFAULT CURRENT_TIMESTAMP - значение по умолчанию = текущее время.
                # PRIMARY KEY - гарантирует уникальность идентификаторов.
                # NOT NULL - предотвращает категории без названия.
                # UNIQUE - исключает дубликаты названий.
                # AUTOINCREMENT - не нужно генерировать ID вручную.
                # DEFAULT CURRENT_TIMESTAMP - автоматическое логирование.
                # IF NOT EXISTS - устойчивость к повторным запускам.
                # PRIMARY KEY создает индекс для быстрого поиска.
                # FOREIGN KEY -  Это "крючок", который соединяет записи в разных таблицах и не позволяет создать "висячие" ссылки.
                #
                #
                #
                #
                #
                #
                #
                #
                #
                #
                #

               
              
                ### Создание таблиц
                cursor.executescript("""
                    PRAGMA foreign_keys = ON;
                    PRAGMA journal_mode = WAL;
                    
                    CREATE TABLE IF NOT EXISTS categories (
                        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        description TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                    
                    CREATE TABLE IF NOT EXISTS products (
                        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        price DECIMAL(10,2) NOT NULL CHECK(price >= 0),
                        stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK(stock_quantity >= 0),
                        category_id INTEGER,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL
                    );
                    
                    CREATE TABLE IF NOT EXISTS customers (
                        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        phone TEXT,
                        registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                    
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_id INTEGER NOT NULL,
                        order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        total_amount DECIMAL(10,2) DEFAULT 0,
                        status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
                    );
                    
                    CREATE TABLE IF NOT EXISTS order_items (
                        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL CHECK(quantity > 0),
                        unit_price DECIMAL(10,2) NOT NULL,
                        subtotal DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) VIRTUAL,
                        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT
                    );
                """)
                
                # Создание индексов
                cursor.executescript("""
                    CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
                    CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);
                    CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
                    CREATE INDEX IF NOT EXISTS idx_orders_customer_date ON orders(customer_id, order_date);
                    CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
                    CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
                    CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id);
                """)
                
                conn.commit()
                self.logger.info("База данных инициализирована успешно")
                
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка инициализации БД: {e}")
            raise
    
    def get_connection(self):
        """Получение соединения с БД с поддержкой транзакций"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
        return conn

    # === CRUD OPERATIONS ===
    
    def create_category(self, name: str, description: str = "") -> int:
        """CREATE: Добавление новой категории"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO categories (name, description) VALUES (?, ?)",
                    (name, description)
                )
                category_id = cursor.lastrowid
                conn.commit()
                self.logger.info(f"Создана категория: {name} (ID: {category_id})")
                return category_id
        except sqlite3.IntegrityError:
            self.logger.error(f"Категория с именем '{name}' уже существует")
            raise
    
    def create_product(self, product_data: Dict[str, Any]) -> int:
        """CREATE: Добавление нового продукта"""
        required_fields = ['name', 'price', 'category_id']
        if not all(field in product_data for field in required_fields):
            raise ValueError(f"Отсутствуют обязательные поля: {required_fields}")
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO products (name, description, price, stock_quantity, category_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    product_data['name'],
                    product_data.get('description', ''),
                    product_data['price'],
                    product_data.get('stock_quantity', 0),
                    product_data['category_id']
                ))
                product_id = cursor.lastrowid
                conn.commit()
                self.logger.info(f"Создан продукт: {product_data['name']} (ID: {product_id})")
                return product_id
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка создания продукта: {e}")
            raise
    
    def batch_create_products(self, products: List[Dict[str, Any]]) -> bool:
        """CREATE: Пакетное добавление продуктов в транзакции"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                for product in products:
                    cursor.execute("""
                        INSERT INTO products (name, description, price, stock_quantity, category_id)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        product['name'],
                        product.get('description', ''),
                        product['price'],
                        product.get('stock_quantity', 0),
                        product['category_id']
                    ))
                conn.commit()
                self.logger.info(f"Пакетно добавлено {len(products)} продуктов")
                return True
        except sqlite3.Error as e:
            conn.rollback()
            self.logger.error(f"Ошибка пакетного добавления: {e}")
            return False
    
    def get_products(self, filters: Dict[str, Any] = None, 
                    page: int = 1, per_page: int = 10) -> List[Dict]:
        """READ: Получение продуктов с фильтрацией и пагинацией"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Базовый запрос
                query = """
                    SELECT p.*, c.name as category_name
                    FROM products p
                    LEFT JOIN categories c ON p.category_id = c.category_id
                    WHERE 1=1
                """
                params = []
                
                # Применение фильтров
                if filters:
                    if 'category_id' in filters:
                        query += " AND p.category_id = ?"
                        params.append(filters['category_id'])
                    if 'min_price' in filters:
                        query += " AND p.price >= ?"
                        params.append(filters['min_price'])
                    if 'max_price' in filters:
                        query += " AND p.price <= ?"
                        params.append(filters['max_price'])
                    if 'search' in filters:
                        query += " AND (p.name LIKE ? OR p.description LIKE ?)"
                        params.extend([f"%{filters['search']}%", f"%{filters['search']}%"])
                
                # Сортировка и пагинация
                query += " ORDER BY p.created_at DESC"
                query += " LIMIT ? OFFSET ?"
                params.extend([per_page, (page - 1) * per_page])
                
                cursor.execute(query, params)
                products = [dict(row) for row in cursor.fetchall()]
                
                self.logger.info(f"Получено {len(products)} продуктов (страница {page})")
                return products
                
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка получения продуктов: {e}")
            return []
    
    def update_product(self, product_id: int, update_data: Dict[str, Any]) -> bool:
        """UPDATE: Обновление данных продукта"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Проверка существования продукта
                cursor.execute("SELECT 1 FROM products WHERE product_id = ?", (product_id,))
                if not cursor.fetchone():
                    self.logger.warning(f"Продукт с ID {product_id} не найден")
                    return False
                
                # Формирование запроса обновления
                set_clause = []
                params = []
                for field, value in update_data.items():
                    if field in ['name', 'description', 'price', 'stock_quantity', 'category_id']:
                        set_clause.append(f"{field} = ?")
                        params.append(value)
                
                if not set_clause:
                    self.logger.warning("Нет полей для обновления")
                    return False
                
                params.append(product_id)
                query = f"UPDATE products SET {', '.join(set_clause)} WHERE product_id = ?"
                
                cursor.execute(query, params)
                conn.commit()
                
                self.logger.info(f"Обновлен продукт ID {product_id}")
                return True
                
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка обновления продукта: {e}")
            return False
    
    def bulk_update_prices(self, category_id: int, increase_percent: float) -> bool:
        """UPDATE: Массовое обновление цен по категории"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE products 
                    SET price = ROUND(price * (1 + ? / 100), 2)
                    WHERE category_id = ?
                """, (increase_percent, category_id))
                
                affected_rows = cursor.rowcount
                conn.commit()
                
                self.logger.info(f"Обновлены цены для {affected_rows} продуктов в категории {category_id}")
                return True
                
        except sqlite3.Error as e:
            conn.rollback()
            self.logger.error(f"Ошибка массового обновления цен: {e}")
            return False
    
    def delete_product(self, product_id: int) -> bool:
        """DELETE: Удаление продукта с проверкой ограничений"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Проверка наличия продукта в заказах
                cursor.execute("""
                    SELECT COUNT(*) as order_count 
                    FROM order_items 
                    WHERE product_id = ?
                """, (product_id,))
                result = cursor.fetchone()
                
                if result['order_count'] > 0:
                    self.logger.warning(f"Невозможно удалить продукт ID {product_id} - есть связанные заказы")
                    return False
                
                cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
                conn.commit()
                
                self.logger.info(f"Удален продукт ID {product_id}")
                return True
                
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка удаления продукта: {e}")
            return False
    
    def truncate_table(self, table_name: str) -> bool:
        """DELETE: Очистка таблицы с сохранением структуры"""
        allowed_tables = ['products', 'categories', 'customers', 'orders', 'order_items']
        if table_name not in allowed_tables:
            self.logger.error(f"Недопустимое имя таблицы для очистки: {table_name}")
            return False
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {table_name}")
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = ?", (table_name,))
                conn.commit()
                
                self.logger.info(f"Очищена таблица {table_name}")
                return True
                
        except sqlite3.Error as e:
            conn.rollback()
            self.logger.error(f"Ошибка очистки таблицы: {e}")
            return False

    # === COMPLEX QUERIES ===
    
    def get_sales_report(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Сложный запрос: отчет по продажам с GROUP BY и агрегатными функциями"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT 
                        c.name as category_name,
                        COUNT(oi.order_item_id) as items_sold,
                        SUM(oi.quantity) as total_quantity,
                        SUM(oi.subtotal) as total_revenue,
                        AVG(oi.unit_price) as avg_price,
                        MAX(oi.unit_price) as max_price,
                        MIN(oi.unit_price) as min_price
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.product_id
                    JOIN categories c ON p.category_id = c.category_id
                    JOIN orders o ON oi.order_id = o.order_id
                    WHERE o.status != 'cancelled'
                """
                params = []
                
                if start_date:
                    query += " AND o.order_date >= ?"
                    params.append(start_date)
                if end_date:
                    query += " AND o.order_date <= ?"
                    params.append(end_date)
                
                query += " GROUP BY c.category_id, c.name ORDER BY total_revenue DESC"
                
                cursor.execute(query, params)
                report = [dict(row) for row in cursor.fetchall()]
                
                self.logger.info(f"Сформирован отчет по продажам: {len(report)} категорий")
                return report
                
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка формирования отчета: {e}")
            return []
    
    def get_customer_orders(self, customer_id: int) -> List[Dict]:
        """Сложный запрос: заказы клиента с JOIN и подзапросами"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT 
                        o.order_id,
                        o.order_date,
                        o.status,
                        o.total_amount,
                        (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.order_id) as item_count,
                        GROUP_CONCAT(p.name, ', ') as product_names
                    FROM orders o
                    LEFT JOIN order_items oi ON o.order_id = oi.order_id
                    LEFT JOIN products p ON oi.product_id = p.product_id
                    WHERE o.customer_id = ?
                    GROUP BY o.order_id
                    ORDER BY o.order_date DESC
                """
                
                cursor.execute(query, (customer_id,))
                orders = [dict(row) for row in cursor.fetchall()]
                
                self.logger.info(f"Получено {len(orders)} заказов для клиента {customer_id}")
                return orders
                
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка получения заказов клиента: {e}")
            return []
    
    def get_popular_products(self, limit: int = 5) -> List[Dict]:
        """Сложный запрос: популярные продукты с использованием подзапросов"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    WITH product_sales AS (
                        SELECT 
                            p.product_id,
                            p.name,
                            p.price,
                            c.name as category_name,
                            SUM(oi.quantity) as total_sold,
                            SUM(oi.subtotal) as total_revenue
                        FROM products p
                        LEFT JOIN order_items oi ON p.product_id = oi.product_id
                        LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status != 'cancelled'
                        LEFT JOIN categories c ON p.category_id = c.category_id
                        GROUP BY p.product_id
                    )
                    SELECT * FROM product_sales
                    ORDER BY total_sold DESC, total_revenue DESC
                    LIMIT ?
                """
                
                cursor.execute(query, (limit,))
                products = [dict(row) for row in cursor.fetchall()]
                
                self.logger.info(f"Получено {len(products)} популярных продуктов")
                return products
                
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка получения популярных продуктов: {e}")
            return []

    # === DATA IMPORT/EXPORT ===
    
    def import_csv_to_table(self, csv_file: str, table_name: str, 
                          mapping: Dict[str, str] = None) -> bool:
        """Импорт данных из CSV с валидацией и преобразованием"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                with open(csv_file, 'r', encoding='utf-8') as file:
                    csv_reader = csv.DictReader(file)
                    
                    for row_num, row in enumerate(csv_reader, 1):
                        try:
                            # Преобразование данных
                            if mapping:
                                mapped_data = {}
                                for csv_field, db_field in mapping.items():
                                    if csv_field in row:
                                        mapped_data[db_field] = row[csv_field]
                            else:
                                mapped_data = row
                            
                            # Валидация и вставка
                            placeholders = ', '.join(['?' for _ in mapped_data])
                            columns = ', '.join(mapped_data.keys())
                            values = list(mapped_data.values())
                            
                            cursor.execute(
                                f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
                                values
                            )
                            
                        except (ValueError, sqlite3.Error) as e:
                            self.logger.warning(f"Пропуск строки {row_num}: {e}")
                            continue
                
                conn.commit()
                self.logger.info(f"Импорт CSV в таблицу {table_name} завершен")
                return True
                
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Ошибка импорта CSV: {e}")
            return False
    
    def import_json_to_table(self, json_file: str, table_name: str) -> bool:
        """Импорт данных из JSON с парсингом сложных структур"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                with open(json_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                    if isinstance(data, list):
                        for item in data:
                            self._insert_json_item(cursor, table_name, item)
                    elif isinstance(data, dict):
                        self._insert_json_item(cursor, table_name, data)
                
                conn.commit()
                self.logger.info(f"Импорт JSON в таблицу {table_name} завершен")
                return True
                
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Ошибка импорта JSON: {e}")
            return False
    
    def _insert_json_item(self, cursor, table_name: str, item: Dict):
        """Вспомогательный метод для вставки элемента JSON"""
        try:
            # Преобразование JSON-структур
            flattened_item = {}
            for key, value in item.items():
                if isinstance(value, (dict, list)):
                    flattened_item[key] = json.dumps(value, ensure_ascii=False)
                else:
                    flattened_item[key] = value
            
            placeholders = ', '.join(['?' for _ in flattened_item])
            columns = ', '.join(flattened_item.keys())
            values = list(flattened_item.values())
            
            cursor.execute(
                f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
                values
            )
            
        except sqlite3.Error as e:
            self.logger.warning(f"Ошибка вставки элемента JSON: {e}")
            raise
    
    def export_table_to_csv(self, table_name: str, output_file: str, 
                          delimiter: str = ',') -> bool:
        """Экспорт таблицы в CSV с настраиваемым разделителем"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                if not rows:
                    self.logger.warning(f"Таблица {table_name} пуста")
                    return False
                
                with open(output_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=delimiter)
                    
                    # Заголовки
                    writer.writerow([description[0] for description in cursor.description])
                    
                    # Данные
                    for row in rows:
                        writer.writerow(row)
                
                self.logger.info(f"Экспорт таблицы {table_name} в {output_file} завершен")
                return True
                
        except Exception as e:
            self.logger.error(f"Ошибка экспорта в CSV: {e}")
            return False
    
    def export_query_to_json(self, query: str, output_file: str, 
                           params: tuple = None) -> bool:
        """Экспорт результатов запроса в JSON с иерархической структурой"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                rows = [dict(row) for row in cursor.fetchall()]
                
                with open(output_file, 'w', encoding='utf-8') as file:
                    json.dump(rows, file, ensure_ascii=False, indent=2, 
                             default=str)  # Для обработки datetime
                
                self.logger.info(f"Экспорт запроса в {output_file} завершен")
                return True
                
        except Exception as e:
            self.logger.error(f"Ошибка экспорта в JSON: {e}")
            return False

    # === DATABASE MAINTENANCE ===
    
    def optimize_database(self):
        """Оптимизация базы данных: перестройка индексов и анализ"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("ANALYZE")
                cursor.execute("VACUUM")
                self.logger.info("Оптимизация базы данных завершена")
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка оптимизации БД: {e}")
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Статистика базы данных для мониторинга производительности"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Размер БД
                cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
                stats['database_size'] = cursor.fetchone()[0]
                
                # Количество записей в таблицах
                tables = ['products', 'categories', 'customers', 'orders', 'order_items']
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    stats[f'{table}_count'] = cursor.fetchone()[0]
                
                # Использование индексов
                cursor.execute("""
                    SELECT name, sql FROM sqlite_master 
                    WHERE type = 'index' AND name NOT LIKE 'sqlite_%'
                """)
                stats['indexes'] = [dict(row) for row in cursor.fetchall()]
                
                self.logger.info("Статистика БД собрана")
                return stats
                
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка сбора статистики: {e}")
            return {}

# === ДЕМОНСТРАЦИЯ РАБОТЫ СИСТЕМЫ ===

def demonstrate_system():
    """Демонстрация работы всей системы"""
    
    # Инициализация
    db = DatabaseManager("demo_ecommerce.db")
    
    print("=== ДЕМОНСТРАЦИЯ СИСТЕМЫ УПРАВЛЕНИЯ БАЗОЙ ДАННЫХ ===\n")
    
    # 1. Создание тестовых данных
    print("1. СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ")
    
    # Категории
    electronics_id = db.create_category("Электроника", "Техника и гаджеты")
    books_id = db.create_category("Книги", "Художественная и учебная литература")
    
    # Продукты
    products_data = [
        {'name': 'iPhone 13', 'price': 799.99, 'stock_quantity': 10, 'category_id': electronics_id},
        {'name': 'Samsung Galaxy', 'price': 699.99, 'stock_quantity': 15, 'category_id': electronics_id},
        {'name': 'Война и мир', 'price': 25.50, 'stock_quantity': 50, 'category_id': books_id},
        {'name': 'Преступление и наказание', 'price': 20.00, 'stock_quantity': 30, 'category_id': books_id},
    ]
    db.batch_create_products(products_data)
    
    print("✓ Тестовые данные созданы\n")
    
    # 2. Демонстрация CRUD операций
    print("2. CRUD ОПЕРАЦИИ")
    
    # Чтение с фильтрацией
    electronic_products = db.get_products({'category_id': electronics_id})
    print(f"✓ Электронные продукты: {len(electronic_products)} шт.")
    
    # Обновление
    db.update_product(1, {'price': 749.99, 'stock_quantity': 8})
    print("✓ Цена iPhone обновлена")
    
    # Массовое обновление
    db.bulk_update_prices(books_id, 10)  # +10% к ценам книг
    print("✓ Цены на книги увеличены на 10%")
    
    # 3. Сложные запросы
    print("\n3. СЛОЖНЫЕ ЗАПРОСЫ")
    
    # Отчет по продажам
    sales_report = db.get_sales_report()
    print("✓ Отчет по продажам сформирован")
    
    # Популярные продукты
    popular = db.get_popular_products(3)
    print(f"✓ Топ-3 популярных продукта: {[p['name'] for p in popular]}")
    
    # 4. Импорт/экспорт
    print("\n4. ИМПОРТ/ЭКСПОРТ ДАННЫХ")
    
    # Экспорт в CSV
    db.export_table_to_csv('products', 'products_export.csv')
    print("✓ Продукты экспортированы в CSV")
    
    # Экспорт в JSON
    db.export_query_to_json(
        "SELECT * FROM products WHERE price > 100",
        'expensive_products.json'
    )
    print("✓ Дорогие продукты экспортированы в JSON")
    
    # 5. Оптимизация и статистика
    print("\n5. ОПТИМИЗАЦИЯ И МОНИТОРИНГ")
    
    db.optimize_database()
    print("✓ База данных оптимизирована")
    
    stats = db.get_database_stats()
    print(f"✓ Статистика собрана: {stats['products_count']} продуктов, {stats['categories_count']} категорий")
    
    print("\n=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===")

if __name__ == "__main__":
    def demonstrate_system():
        """Демонстрация работы всей системы без ошибок при повторных запусках"""
    
    # Инициализация
    db = DatabaseManager("demo_ecommerce.db")
    
    print("=== ДЕМОНСТРАЦИЯ СИСТЕМЫ УПРАВЛЕНИЯ БАЗОЙ ДАННЫХ ===\n")
    
    # 1. Создание тестовых данных с проверкой существования
    print("1. СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ")
    
    # Сначала очистим старые данные для чистой демонстрации
    db.truncate_table('order_items')
    db.truncate_table('orders')
    db.truncate_table('products')
    db.truncate_table('categories')
    db.truncate_table('customers')
    
    # Категории - создаем с проверкой
    try:
        electronics_id = db.create_category("Электроника", "Техника и гаджеты")
        print("✓ Создана категория: Электроника")
    except sqlite3.IntegrityError:
        # Если категория уже существует, получаем её ID
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category_id FROM categories WHERE name = ?", ("Электроника",))
            electronics_id = cursor.fetchone()[0]
        print("✓ Используем существующую категорию: Электроника")
    
    try:
        books_id = db.create_category("Книги", "Художественная и учебная литература")
        print("✓ Создана категория: Книги")
    except sqlite3.IntegrityError:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category_id FROM categories WHERE name = ?", ("Книги",))
            books_id = cursor.fetchone()[0]
        print("✓ Используем существующую категорию: Книги")
    
    # Продукты
    products_data = [
        {'name': 'iPhone 13', 'price': 799.99, 'stock_quantity': 10, 'category_id': electronics_id},
        {'name': 'Samsung Galaxy', 'price': 699.99, 'stock_quantity': 15, 'category_id': electronics_id},
        {'name': 'Война и мир', 'price': 25.50, 'stock_quantity': 50, 'category_id': books_id},
        {'name': 'Преступление и наказание', 'price': 20.00, 'stock_quantity': 30, 'category_id': books_id},
    ]
    
    # Удаляем старые продукты перед добавлением новых
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products")
        conn.commit()
    
    db.batch_create_products(products_data)
    print("✓ Созданы тестовые продукты")
    
    # 2. Демонстрация CRUD операций
    print("\n2. CRUD ОПЕРАЦИИ")
    
    # Чтение с фильтрацией
    electronic_products = db.get_products({'category_id': electronics_id})
    print(f"✓ Электронные продукты: {len(electronic_products)} шт.")
    
    # Обновление
    if electronic_products:
        first_product_id = electronic_products[0]['product_id']
        db.update_product(first_product_id, {'price': 749.99, 'stock_quantity': 8})
        print("✓ Цена первого продукта обновлена")
    
    # Массовое обновление
    db.bulk_update_prices(books_id, 10)  # +10% к ценам книг
    print("✓ Цены на книги увеличены на 10%")
    
    # 3. Сложные запросы
    print("\n3. СЛОЖНЫЕ ЗАПРОСЫ")
    
    # Отчет по продажам (пустой, т.к. нет заказов)
    sales_report = db.get_sales_report()
    print(f"✓ Отчет по продажам сформирован: {len(sales_report)} категорий")
    
    # Популярные продукты
    popular = db.get_popular_products(3)
    print(f"✓ Топ-3 продуктов: {[p['name'] for p in popular]}")
    
    # 4. Импорт/экспорт
    print("\n4. ИМПОРТ/ЭКСПОРТ ДАННЫХ")
    
    # Экспорт в CSV
    try:
        db.export_table_to_csv('products', 'products_export.csv')
        print("✓ Продукты экспортированы в CSV")
    except Exception as e:
        print(f"⚠ Ошибка экспорта в CSV: {e}")
    
    # Экспорт в JSON
    try:
        db.export_query_to_json(
            "SELECT * FROM products WHERE price > 100",
            'expensive_products.json'
        )
        print("✓ Дорогие продукты экспортированы в JSON")
    except Exception as e:
        print(f"⚠ Ошибка экспорта в JSON: {e}")
    
    # 5. Оптимизация и статистика
    print("\n5. ОПТИМИЗАЦИЯ И МОНИТОРИНГ")
    
    try:
        db.optimize_database()
        print("✓ База данных оптимизирована")
    except Exception as e:
        print(f"⚠ Ошибка оптимизации: {e}")
    
    stats = db.get_database_stats()
    print(f"✓ Статистика собрана: {stats.get('products_count', 0)} продуктов, {stats.get('categories_count', 0)} категорий")
    
    print("\n=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО ===")
    
    