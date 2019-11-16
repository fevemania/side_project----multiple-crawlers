CREATE TABLE categories (
    id BIGINT NOT NULL AUTO_INCREMENT,
    category_id INT NOT NULL,
    category_name TEXT NOT NULL,
    PRIMARY KEY(id),
    UNIQUE(category_id)
) CHARACTER SET utf8;


CREATE TABLE products (
    id BIGINT NOT NULL AUTO_INCREMENT,
    product_id BIGINT NOT NULL,
    product_name TEXT NOT NULL,
    price_min FLOAT,
    price_max FLOAT,
    category_id INT NOT NULL,
    PRIMARY KEY(id),
    UNIQUE(product_id)
) CHARACTER SET utf8mb4;
