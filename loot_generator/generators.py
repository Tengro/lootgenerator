import pprint
import random

class AbstractLootGenerator(object):
    RESULT_NAME = None
    VALUE_NAME = None
    EXTRA_NAME = None

    def __init__(self, loot_table, return_object=True, result_file_name=None, *args,  **kwargs):
        self.loot_table = loot_table
        self.result_file_name = result_file_name
        self.selection_options = loot_table.to_list()
        self.return_object = return_object

    def generate(self, amount, *args, **kwargs):
        result_dict = {}
        generateable = True
        while generateable:
            generation_options = self.select_for_generation(amount, *args, **kwargs)
            generateable = bool(generation_options)
            if generateable:
                result = self.select_loot(generation_options)
                amount = amount - result[self.VALUE_NAME]
                if result[self.RESULT_NAME] in result_dict.keys():
                    result_dict[result[self.RESULT_NAME]] += 1
                else:
                    result_dict[result[self.RESULT_NAME]] = 1
            else:
                result_dict[self.EXTRA_NAME] = amount
        self.print_result(result_dict)
        if self.return_object:
            return result_dict

    def select_for_generation(self, amount,  *args, **kwargs):
        raise NotImplementedError

    def select_loot(self, generation_options):
        raise NotImplementedError

    def print_result(self, result):
        if self.result_file_name:
            result_file = open(self.result_file_name, 'w')
            printer = pprint.PrettyPrinter(indent=4, stream=result_file)
        else:
            printer = pprint.PrettyPrinter(indent=4)
        printer.pprint(result)
        if self.result_file_name:
            result_file.close()


class BasicLootGenerator(AbstractLootGenerator):
    RESULT_NAME = 'item'
    VALUE_NAME = 'value'
    EXTRA_NAME = 'extra'

    def select_loot(self, generation_options):
        return random.choice(generation_options)
    
    def select_for_generation(self, amount, *args, **kwargs):
        filtered_selection_options = filter(lambda x: x[self.VALUE_NAME] <= amount, self.selection_options)
        return filtered_selection_options


class MiscLootGenerator(BasicLootGenerator):
    MISC_KWARG = 'exclude_misc'
    MISC_NAME = 'is_misc'

    def select_for_generation(self, amount, *args, **kwargs):
        filtered_selection_options = super(MiscLootGenerator, self).select_for_generation(amount, *args, **kwargs)
        if self.MISC_KWARG in kwargs:
            filtered_selection_options = filter(lambda x: not x[self.MISC_NAME], filtered_selection_options)
        return filtered_selection_options



class WeightedLootGenerator(MiscLootGenerator):
    WEIGHT_NAME = 'weight'

    def select_loot(self, generation_options):
        weights_list = [item[self.WEIGHT_NAME] for item in generation_options]
        return generation_options[self.weighted_choice_sub(weights_list)]

    def weighted_choice_sub(self, weights):
        rnd = random.random() * sum(weights)
        for i, w in enumerate(weights):
            rnd -= w
            if rnd < 0:
                return i
