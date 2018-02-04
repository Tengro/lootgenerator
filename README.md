*Loot Generator 0.1.0*

Simple and plain console script for on-the-fly loot generation for tabletop RPGs.

To install:
pip install lootgenerator


`from loot_generator.tables import CSVLootTable`

`from loot_generator.generators import BasicLootGenerator`

`table = CSVLootTable('my_loot_table_path.csv')`

`generator = BasicLootGenerator(table)`

`generator.generate(1000)`
