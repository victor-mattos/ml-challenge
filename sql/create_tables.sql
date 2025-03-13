
CREATE OR REPLACE TABLE CLIENT (
    client_id  VARCHAR(50) PRIMARY KEY,
    email      VARCHAR(100) UNIQUE NOT NULL,
    name       VARCHAR(100) NOT NULL,
    cellphone  VARCHAR(20),
    address    VARCHAR(255),
    birth_date DATE NOT NULL
);


CREATE TABLE CATEGORIA (
    category_id   INTEGER PRIMARY KEY AUTOINCREMENT, 
    category_name TEXT NOT NULL UNIQUE              
);


CREATE TABLE ITEM (
    datetime_ref DATETIME NOT NULL,
    item_id      VARCHAR(50) NOT NULL,
    seller_id    VARCHAR(100) NOT NULL,
    published_at DATETIME NOT NULL,
    price        DECIMAL(10,2) NOT NULL,
    category_id  VARCHAR(50) NOT NULL,
    condition    VARCHAR(50) NOT NULL,
    shipping     VARCHAR(100) NOT NULL,
    PRIMARY KEY (datetime_ref, item_id, seller_id),
    FOREIGN KEY (category_id) REFERENCES CATEGORIA(category_id),
    FOREIGN KEY (seller_id) REFERENCES CLIENT(client_id)
);


CREATE TABLE TRANSACTIONS (
    order_id  	VARCHAR(50) PRIMARY KEY,
    buyer_id    VARCHAR(100) NOT NULL,
    seller_id   VARCHAR(100) NOT NULL,
    created_at  DATETIME NOT NULL,
    item_id     VARCHAR(255) NOT NULL,
    category_id VARCHAR(255) NOT NULL,
    condition	VARCHAR(255) NOT NULL,
    shipping	VARCHAR(255) NOT NULL,
    price		FLOAT NOT NULL,
    quantity	INTEGER NOT NULL
);
