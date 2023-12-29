-- Create a table named 'pictures'
CREATE TABLE IF NOT EXISTS pictures (
            id varchar(36) NOT NULL,
            path varchar(250) NOT NULL,
            size int(12) NOT NULL,
            date varchar(28) NOT NULL,
            PRIMARY KEY (id)
        );

-- Create a table named 'tags'
CREATE TABLE IF NOT EXISTS tags (
            tag varchar(36) NOT NULL,
            picture_id varchar(36) NOT NULL,
            confidence int NOT NULL,
            date varchar(28) NOT NULL,
            PRIMARY KEY (tag, picture_id),
            FOREIGN KEY (picture_id) REFERENCES pictures(id)
        );