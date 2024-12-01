def add_sample_data():
    # Adding users
    user_data = [
        ("Alice", "alice@example.com"),
        ("Bob", "bob@example.com"),
        ("Charlie", "charlie@example.com"),
        ("David", "david@example.com"),
        ("Eve", "eve@example.com"),
        ("Frank", "frank@example.com"),
        ("Grace", "grace@example.com"),
        ("Heidi", "heidi@example.com"),
        ("Ivan", "ivan@example.com"),
        ("Judy", "judy@example.com")
    ]
    for name, email in user_data:
        add_user(name, email)

    # Adding products
    product_data = [
        ("Laptop", 1000),
        ("Smartphone", 500),
        ("Tablet", 300),
        ("Monitor", 150),
        ("Keyboard", 50),
        ("Mouse", 25),
        ("Printer", 200),
        ("Router", 75),
        ("Webcam", 60),
        ("Headphones", 80)
    ]
    for name, price in product_data:
        add_product(name, price)

    # Adding orders
    for i in range(1, 11):
        add_order(i)

    # Adding order_items
    order_item_data = [
        (1, 1, 2),
        (1, 2, 1),
        (2, 3, 1),
        (2, 4, 2),
        (3, 5, 3),
        (3, 6, 1),
        (4, 7, 2),
        (4, 8, 1),
        (5, 9, 1),
        (5, 10, 2),
        (6, 1, 1),
        (6, 2, 2),
        (7, 3, 1),
        (7, 4, 1),
        (8, 5, 2),
        (8, 6, 1),
        (9, 7, 3),
        (9, 8, 1),
        (10, 9, 1),
        (10, 10, 1)
    ]
    for order_id, product_id, quantity in order_item_data:
        add_order_item(order_id, product_id, quantity)

