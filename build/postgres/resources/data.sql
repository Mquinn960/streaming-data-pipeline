\c menustats

CREATE TABLE term (
   id SERIAL,
   term_id VARCHAR NOT NULL PRIMARY KEY,
   term_name VARCHAR NOT NULL
);

CREATE TABLE match (
   id SERIAL PRIMARY KEY,
   menu_id VARCHAR NOT NULL,
   term_id VARCHAR NOT NULL,
   product_name VARCHAR NOT NULL,
   product_description VARCHAR,
   CONSTRAINT fk_term
      FOREIGN KEY (term_id) 
	      REFERENCES term (term_id)
);
