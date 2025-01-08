CREATE TABLE Categories(
    id_category INT IDENTITY(1,1) PRIMARY KEY,
	category NVARCHAR(255) NOT NULL UNIQUE
);

-- Agarrar todas las cateogrias de todas las tablas e insertarlas en la tabla categories
INSERT INTO Categories(category)
SELECT category FROM animals
UNION
SELECT category FROM artifacts
UNION
SELECT category FROM crops
UNION
SELECT category FROM fish
UNION
SELECT category FROM harvest
UNION
SELECT category FROM minerals
UNION
SELECT category FROM fruit;

-- Change the category name for the id in the catogeries table

UPDATE animals
SET animals.category = Categories.id_category
FROM animals
	JOIN Categories ON animals.category = Categories.category;

UPDATE artifacts
SET artifacts.category = Categories.id_category
FROM artifacts
	JOIN Categories ON artifacts.category = Categories.category;

UPDATE crops
SET crops.category = Categories.id_category
FROM crops
	JOIN Categories ON crops.category = Categories.category;

UPDATE fish
SET fish.category = Categories.id_category
FROM fish
	JOIN Categories ON fish.category = Categories.category;

UPDATE fruit
SET fruit.category = Categories.id_category
FROM fruit
	JOIN Categories ON fruit.category = Categories.category;

UPDATE harvest
SET harvest.category = Categories.id_category
FROM harvest
	JOIN Categories ON harvest.category = Categories.category;

UPDATE minerals
SET minerals.category = Categories.id_category
FROM minerals
	JOIN Categories ON minerals.category = Categories.category;