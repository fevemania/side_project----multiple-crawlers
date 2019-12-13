CREATE TABLE categories (
    id BIGINT NOT NULL AUTO_INCREMENT,
    category_id INT NOT NULL,
    category_name TEXT NOT NULL,
    PRIMARY KEY(id),
    UNIQUE(category_id)
) CHARACTER SET utf8mb4;
