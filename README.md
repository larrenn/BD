Система управления базой данных интернет-магазина на SQLite
https://img.shields.io/badge/Python-3.8+-blue.svg
https://img.shields.io/badge/SQLite-3.0+-green.svg
https://img.shields.io/badge/License-MIT-yellow.svg

Полнофункциональная система управления реляционной базой данных для интернет-магазина, реализующая все основные операции CRUD, сложные SQL-запросы, импорт/экспорт данных и оптимизацию производительности.

📋 Оглавление
Особенности

Архитектура БД

Быстрый старт

Установка

Использование

Документация API

Примеры запросов

Импорт/экспорт данных

Оптимизация

Структура проекта

Разработка

Лицензия

✨ Особенности
🗄️ Полный цикл работы с БД
Проектирование с соблюдением нормальных форм (1NF, 2NF, 3NF)

Сложные SQL-запросы с JOIN, GROUP BY, подзапросами

Транзакции для обеспечения целостности данных

Индексы для оптимизации производительности

🔄 CRUD операции
Create: Добавление одиночных и пакетных записей

Read: Фильтрация, сортировка, пагинация

Update: Модификация с проверкой ограничений

Delete: Каскадное удаление с сохранением структуры

📊 Импорт/экспорт
CSV: Загрузка и выгрузка с настраиваемыми разделителями

JSON: Парсинг сложных структур и иерархический экспорт

Валидация данных при передаче

⚡ Производительность
Индексация ключевых полей

Оптимизация запросов через EXPLAIN

Кэширование часто используемых данных

Мониторинг статистики БД

🗃️ Архитектура БД
Диаграмма базы данных
text
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  categories │    │   products  │    │  customers  │
│─────────────│    │─────────────│    │─────────────│
│ category_id │◄───│ category_id │    │ customer_id │
│ name        │    │ product_id  │    │ first_name  │
│ description │    │ name        │    │ last_name   │
│ created_at  │    │ description │    │ email       │
└─────────────┘    │ price       │    │ phone       │
                   │ stock_qty   │    │ reg_date    │
┌─────────────┐    │ created_at  │    └─────────────┘
│   orders    │    └─────────────┘           │
│─────────────│            │            ┌────┘
│ order_id    │    ┌─────────────┐      │
│ customer_id │┼───│ order_items │      │
│ order_date  │    │─────────────│      │
│ total_amt   │    │ order_id    │┼─────┘
│ status      │    │ product_id  │
└─────────────┘    │ quantity    │
                   │ unit_price  │
                   │ subtotal    │
                   └─────────────┘
Схема таблиц
Категории (categories)
sql
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
Продукты (products)
sql
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL CHECK(price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK(stock_quantity >= 0),
    category_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL
);
Клиенты (customers)
sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
Заказы (orders)
sql
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) DEFAULT 0,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);
Элементы заказа (order_items)
sql
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) VIRTUAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT
);
🚀 Быстрый старт
Минимальный пример
python
from database import DatabaseManager

# Создание базы данных
db = DatabaseManager("my_shop.db")

# Создание категории
category_id = db.create_category("Электроника", "Техника и гаджеты")

# Добавление продукта
product_data = {
    'name': 'iPhone 13',
    'price': 799.99,
    'stock_quantity': 10,
    'category_id': category_id
}
product_id = db.create_product(product_data)

# Получение продуктов
products = db.get_products({'category_id': category_id})
print(f"Найдено продуктов: {len(products)}")
📥 Установка
Требования
Python 3.8+

SQLite 3.0+

Установка зависимостей
bash
# Клонирование репозитория
git clone https://github.com/your-username/ecommerce-db-system.git
cd ecommerce-db-system

# Установка зависимостей
pip install -r requirements.txt
requirements.txt
txt
# Основные зависимости
sqlite3>=3.0.0
logging>=0.4.9.6

# Для расширенного функционала
pandas>=1.3.0
numpy>=1.21.0
💻 Использование
Инициализация системы
python
from database import DatabaseManager

# Создание экземпляра менеджера БД
db = DatabaseManager("ecommerce.db")

# Автоматическое создание таблиц и индексов
# Файл БД создается автоматически при первом запуске
Демонстрация всех возможностей
python
from database import demonstrate_system

# Запуск полной демонстрации системы
demonstrate_system()
📚 Документация API
Основные методы
create_category(name, description="")
Создает новую категорию продуктов.

Параметры:

name (str): Название категории (уникальное)

description (str): Описание категории

Возвращает:

int: ID созданной категории

Пример:

python
category_id = db.create_category(
    name="Книги",
    description="Художественная и учебная литература"
)
create_product(product_data)
Добавляет новый продукт в базу данных.

Параметры:

product_data (dict): Словарь с данными продукта

Структура product_data:

python
{
    'name': 'Название продукта',
    'description': 'Описание продукта',
    'price': 99.99,           # decimal
    'stock_quantity': 10,     # int
    'category_id': 1          # int
}
get_products(filters=None, page=1, per_page=10)
Получает список продуктов с фильтрацией и пагинацией.

Параметры:

filters (dict): Словарь фильтров

page (int): Номер страницы

per_page (int): Количество элементов на странице

Доступные фильтры:

python
filters = {
    'category_id': 1,         # Фильтр по категории
    'min_price': 50,          # Минимальная цена
    'max_price': 500,         # Максимальная цена
    'search': 'iphone'        # Поиск по названию и описанию
}
update_product(product_id, update_data)
Обновляет данные продукта.

Параметры:

product_id (int): ID продукта

update_data (dict): Поля для обновления

Пример:

python
db.update_product(1, {
    'price': 849.99,
    'stock_quantity': 15
})
delete_product(product_id)
Удаляет продукт с проверкой ограничений.

🔍 Примеры запросов
Сложные SQL-запросы
Отчет по продажам
python
# Получение отчета по продажам с группировкой
report = db.get_sales_report(
    start_date='2024-01-01',
    end_date='2024-12-31'
)
SQL запрос:

sql
SELECT 
    c.name as category_name,
    COUNT(oi.order_item_id) as items_sold,
    SUM(oi.quantity) as total_quantity,
    SUM(oi.subtotal) as total_revenue,
    AVG(oi.unit_price) as avg_price
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status != 'cancelled'
GROUP BY c.category_id, c.name
ORDER BY total_revenue DESC
Популярные продукты
python
# Топ-5 самых продаваемых продуктов
popular = db.get_popular_products(limit=5)
Заказы клиента
python
# Полная история заказов клиента
orders = db.get_customer_orders(customer_id=1)
📊 Импорт/экспорт данных
Импорт из CSV
python
# Импорт продуктов из CSV
db.import_csv_to_table(
    csv_file='products.csv',
    table_name='products',
    mapping={
        'product_name': 'name',
        'product_price': 'price',
        'category': 'category_id'
    }
)
Формат CSV:

csv
product_name,product_price,category,stock_quantity
iPhone 13,799.99,1,10
Samsung Galaxy,699.99,1,15
Импорт из JSON
python
# Импорт из JSON файла
db.import_json_to_table('categories.json', 'categories')
Формат JSON:

json
[
    {
        "name": "Электроника",
        "description": "Техника и гаджеты"
    },
    {
        "name": "Книги", 
        "description": "Литература"
    }
]
Экспорт в CSV
python
# Экспорт таблицы продуктов
db.export_table_to_csv(
    table_name='products',
    output_file='products_export.csv',
    delimiter=','
)
Экспорт в JSON
python
# Экспорт результатов запроса
db.export_query_to_json(
    query="SELECT * FROM products WHERE price > 100",
    output_file='expensive_products.json'
)
⚡ Оптимизация
Индексы
Система автоматически создает оптимальные индексы:

sql
-- Индексы для продуктов
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_price ON products(price);

-- Индексы для клиентов  
CREATE INDEX idx_customers_email ON customers(email);

-- Индексы для заказов
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_orders_status ON orders(status);
Мониторинг производительности
python
# Получение статистики БД
stats = db.get_database_stats()
print(f"Размер БД: {stats['database_size']} байт")
print(f"Количество продуктов: {stats['products_count']}")
Оптимизация БД
python
# Перестройка индексов и сжатие БД
db.optimize_database()
📁 Структура проекта
text
ecommerce-db-system/
├── database.py                 # Основной класс DatabaseManager
├── demo_ecommerce.db          # Пример базы данных
├── database_operations.log    # Лог операций
├── examples/                  # Примеры использования
│   ├── basic_usage.py        # Базовые операции
│   ├── complex_queries.py    # Сложные запросы
│   └── import_export.py      # Импорт/экспорт
├── data/                      # Примеры данных
│   ├── products.csv
│   ├── categories.json
│   └── sales_data.csv
├── docs/                      # Документация
│   ├── api.md
│   └── database_schema.md
├── tests/                     # Тесты
│   ├── test_crud.py
│   ├── test_queries.py
│   └── test_import_export.py
├── requirements.txt           # Зависимости
└── README.md                 # Эта документация
🛠 Разработка
Запуск тестов
bash
python -m pytest tests/ -v
Логирование
Система использует встроенный модуль logging:

python
import logging
logging.basicConfig(level=logging.INFO)
Расширение функциональности
python
class CustomDatabaseManager(DatabaseManager):
    def get_custom_report(self):
        """Пример добавления пользовательского отчета"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Ваша кастомная логика
            pass


🤝 Вклад в проект
Мы приветствуем вклад в развитие проекта! Пожалуйста:

Форкните репозиторий

Создайте ветку для функции (git checkout -b feature/amazing-feature)

Закоммитьте изменения (git commit -m 'Add amazing feature')

Запушьте в ветку (git push origin feature/amazing-feature)

Откройте Pull Request

📞 Поддержка
Если у вас есть вопросы или предложения:

Создайте Issue в репозитории

Напишите на email: your-email@example.com

Проверьте документацию в папке docs/

