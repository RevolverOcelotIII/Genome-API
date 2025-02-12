CREATE DATABASE snpfinder;

USE snpfinder;

CREATE TABLE Project (
    id INTEGER PRIMARY KEY,
    uuid VARCHAR(200),
    name VARCHAR(200)
);

CREATE TABLE Sample (
    id INTEGER PRIMARY KEY,
    uuid VARCHAR(200),
    name VARCHAR(200),
    state INTEGER,
    project_id INTEGER,
    FOREIGN KEY (project_id) REFERENCES Project(id)
);

CREATE TABLE Gene (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200)
);

CREATE TABLE Sample_x_Gene (
    sample_id INTEGER,
    gene_id INTEGER,
    PRIMARY KEY (sample_id, gene_id),
    FOREIGN KEY (sample_id) REFERENCES Sample(id),
    FOREIGN KEY (gene_id) REFERENCES Gene(id)
);
