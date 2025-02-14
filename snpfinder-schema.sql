DROP DATABASE IF EXISTS snpfinder;
CREATE DATABASE snpfinder;
USE snpfinder;

CREATE TABLE project (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    uuid VARCHAR(200),
    name VARCHAR(200)
);

CREATE TABLE sample (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    uuid VARCHAR(200),
    name VARCHAR(200),
    state INTEGER,
    project_id INTEGER,
    FOREIGN KEY (project_id) REFERENCES project(id)
);

CREATE TABLE gene (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200)
);

CREATE TABLE sample_x_gene (
    sample_id INTEGER,
    gene_id INTEGER,
    PRIMARY KEY (sample_id, gene_id),
    FOREIGN KEY (sample_id) REFERENCES sample(id),
    FOREIGN KEY (gene_id) REFERENCES gene(id)
);

INSERT INTO gene (name) VALUES ('RHD');
INSERT INTO gene (name) VALUES ('RHCE');