-- The MySQL syntax for implementing the database schema for tradeQuick application
-- Create database and use it
CREATE DATABASE IF NOT EXISTS tradequick;

USE tradequick;

-- Create users table
CREATE TABLE
    IF NOT EXISTS users (
        user_id VARCHAR(36) NOT NULL PRIMARY KEY,
        fullname VARCHAR(30) NOT NULL,
        verified BOOLEAN NOT NULL DEFAULT FALSE,
        email VARCHAR(225) NOT NULL UNIQUE,
        password VARCHAR(225) NOT NULL,
        gender ENUM ('Male', 'Female', 'Other') NOT NULL,
        phone1 VARCHAR(15) NOT NULL,
        phone2 VARCHAR(15),
        about TEXT,
        address VARCHAR(50) NOT NULL,
        town VARCHAR(30) NOT NULL,
        city VARCHAR(30) NOT NULL,
        state VARCHAR(20) NOT NULL,
        photo VARCHAR(225),
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

-- Create index to use user_id as foreign a key
CREATE INDEX idx_users_user_id ON users (user_id);

-- Create items table
CREATE TABLE
    IF NOT EXISTS items (
        item_id VARCHAR(36) NOT NULL,
        user_id VARCHAR(36) NOT NULL,
        item_name VARCHAR(20) NOT NULL,
        price INT NOT NULL,
        description VARCHAR(200) NOT NULL,
        photo1 VARCHAR(225) NOT NULL,
        photo2 VARCHAR(225),
        photo3 VARCHAR(225),
        sold BOOLEAN NOT NULL DEFAULT FALSE,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (item_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    );

-- Create index on item_id, for it to be used as a foreign key
CREATE INDEX idx_items_item_id ON items (item_id);

-- Crate table for comments
CREATE TABLE
    IF NOT EXISTS comments (
        comment_id VARCHAR(36) NOT NULL,
        commenter VARCHAR(36) NOT NULL,
        item_id VARCHAR(36) NOT NULL,
        comment VARCHAR(300) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (comment_id),
        FOREIGN KEY (commenter) REFERENCES users (user_id) ON DELETE CASCADE,
        FOREIGN KEY (item_id) REFERENCES items (item_id) ON DELETE CASCADE
    );

-- Create likes/dislikes table
CREATE TABLE
    IF NOT EXISTS likes (
        item_id VARCHAR(36) NOT NULL,
        user_id VARCHAR(36) NOT NULL,
        liked BOOLEAN NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (item_id, user_id),
        FOREIGN KEY (item_id) REFERENCES items (item_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    );

-- Create the table to store private chats
CREATE TABLE
    IF NOT EXISTS chats (
        message_id VARCHAR(36) NOT NULL,
        sender_id VARCHAR(36) NOT NULL,
        receiver_id VARCHAR(36) NOT NULL,
        message TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (message_id),
        FOREIGN KEY (sender_id) REFERENCES users (user_id) ON DELETE CASCADE,
        FOREIGN KEY (receiver_id) REFERENCES users (user_id) ON DELETE CASCADE
    );

-- Create rating table
CREATE TABLE
    IF NOT EXISTS ratings (
        rating_id VARCHAR(36) NOT NULL,
        user_id VARCHAR(36) NOT NULL,
        rating INT CHECK (rating > 0 AND rating <= 5) NOT NULL,
        comment VARCHAR(225),
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (rating_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    );