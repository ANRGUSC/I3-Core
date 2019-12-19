USE `i3database`;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
	id INTEGER AUTO_INCREMENT,
	user_id INTEGER,
	username VARCHAR(25) NOT NULL,
	pw VARCHAR(128) NOT NULL,
	super INT(1) NOT NULL DEFAULT 0,
	PRIMARY KEY (id),
	FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
  );

CREATE UNIQUE INDEX users_username ON users (username);

DROP TABLE IF EXISTS acls;

CREATE TABLE acls (
	id INTEGER AUTO_INCREMENT,
	user_id INTEGER,
	username VARCHAR(30) NOT NULL,
	topic VARCHAR(256) NOT NULL,
	topic_id INTEGER,
	rw INTEGER(1) NOT NULL DEFAULT 1,	-- 1: read-only, 2: read-write
	PRIMARY KEY (id),
	FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
	FOREIGN KEY (topic_id) REFERENCES products_product(id) ON DELETE CASCADE
	);
CREATE UNIQUE INDEX acls_user_topic ON acls (username, topic(228));

