-- Rename tables from artifacts
EXEC sp_rename 'artifacts.[(''category'',)]', 'category', 'COLUMN';
EXEC sp_rename 'artifacts.[(''sell_price'',)]', 'sell_price', 'COLUMN';

-- Rename tables from fish
EXEC sp_rename 'fish.[(''fish_name'',)]', 'fish_name', 'COLUMN';
EXEC sp_rename 'fish.[(''category'',)]', 'category', 'COLUMN';
EXEC sp_rename 'fish.[(''sell_price_standard'',)]', 'sell_price_standard', 'COLUMN';
EXEC sp_rename 'fish.[(''sell_price_silver'',)]', 'sell_price_silver', 'COLUMN';
EXEC sp_rename 'fish.[(''sell_price_gold'',)]', 'sell_price_gold', 'COLUMN';
EXEC sp_rename 'fish.[(''sell_price_iridium'',)]', 'sell_price_iridium', 'COLUMN';

-- Rename tables from harvest
EXEC sp_rename 'harvest.[(''crop_name'',)]', 'crop_name', 'COLUMN';
EXEC sp_rename 'harvest.[(''category'',)]', 'category', 'COLUMN';
EXEC sp_rename 'harvest.[(''sell_price_standard'',)]', 'sell_price_standard', 'COLUMN';
EXEC sp_rename 'harvest.[(''sell_price_silver'',)]', 'sell_price_silver', 'COLUMN';
EXEC sp_rename 'harvest.[(''sell_price_gold'',)]', 'sell_price_gold', 'COLUMN';
EXEC sp_rename 'harvest.[(''sell_price_iridium'',)]', 'sell_price_iridium', 'COLUMN';

-- Rename tables from minerals
EXEC sp_rename 'minerals.[(''mineral_name'',)]', 'mineral_name', 'COLUMN';
EXEC sp_rename 'minerals.[(''category'',)]', 'category', 'COLUMN';
EXEC sp_rename 'minerals.[(''sell_price'',)]', 'sell_price', 'COLUMN';