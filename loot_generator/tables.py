import json
import csv
import abc

class AbstractLootTable(object):
    __metaclass__ = abc.ABCMeta

    def to_list(self):
        raise NotImplementedError

    def to_repr(self):
        raise NotImplementedError

    def to_intermediate(self):
        raise NotImplementedError


class FileLootTable(AbstractLootTable):
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file


class ListLootTable(AbstractLootTable):
    def __init__(self, loot_list):
        self.loot_list = loot_list

    def to_list(self):
        return self.loot_list

    def to_repr(self):
        return str(self.to_list())

    def to_intermediate(self):
        return self.loot_list


class JSONLootTable(FileLootTable):
    def to_intermediate(self):
        if hasattr(self, 'intermediate_result'):
            return self.intermediate_result
        loot_file = open(self.path_to_file, 'r')
        intermediate_result = json.load(loot_file)
        loot_file.close()
        self.intermediate_result = intermediate_result
        return intermediate_result

    def to_repr(self):
        return json.dumps(self.to_intermediate(), indent=4)

    def to_list(self):
        return self.to_intermediate()


class CSVLootTable(FileLootTable):
    def to_intermediate(self):
        if hasattr(self, 'intermediate_result'):
            return self.intermediate_result
        loot_file = open(self.path_to_file, 'r')
        row_parser = csv.reader(loot_file, quotechar='"', delimiter=',')
        intermediate_result = []
        keys_list = []
        for index, raw_row in enumerate(row_parser):            
            row = map(lambda s: s.strip(), raw_row)
            row_raw_values = [cell for cell in row]
            if index == 0:
                keys_list = row_raw_values
            else:
                prepared_row = map(self._map_to_float, row_raw_values)
                row_dict = zip(keys_list, prepared_row)
                intermediate_result.append(row_dict)
        self.intermediate_result = intermediate_result
        loot_file.close()
        return intermediate_result

    def _map_to_float(self, item):
        try:
            return float(item)
        except ValueError:
            return item

    def to_repr(self):
        return json.dumps(self.to_intermediate(), indent=4)

    def to_list(self):
        return self.to_intermediate()
