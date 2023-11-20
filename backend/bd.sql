CREATE TABLE groups_contacts (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE contacts (
    id INTEGER PRIMARY KEY,
    id_group INTEGER,
    name VARCHAR(50),
    phone VARCHAR(13),
    FOREIGN KEY (id_group) REFERENCES groups_contacts(id)
);

/*
ALTER TABLE contacts
ADD CONSTRAINT fk_group_id
FOREIGN KEY (id_group)
REFERENCES groups_contacts(id_group);
*/

