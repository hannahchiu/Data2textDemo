import re
import json


def read_json(filename):
    '''Read in a json file.'''
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data

class Controller(object):
    """docstring for Controller"""
    def __init__(self, intent_pattern, entity_info):
        super(Controller, self).__init__()
        self.intent_pattern = read_json(intent_pattern)
        self.entity_info = read_json(entity_info)
        self.regex = {}
        self.prepare_regex()
        # print(self.regex['search_item'][16])
    def prepare_regex(self):
        # loop thru every items
        find_paren_exp = r'\(([\w\|]*)\)'

        for k, p_list in self.intent_pattern.items():
            self.regex[k] = []
            for p in p_list:
                # if p != "((brand_1)的)?(name)的(price|feeling|color|smell|volume|CP|url|brand_2|pic|listed_time|comment|effect|info|tips|article|texture)(是什麼|如何)":
                #     continue
                pattern = p
                m = re.findall(find_paren_exp, p)
                if m:
                    # print('---------------------')
                    # print('pattern', p)
                    # print(m)
                    for subreg in m:
                        # if subreg[:5] == 'brand' or subreg[:4] == 'name':
                        #     continue
                        subreg_expand = subreg
                        if subreg_expand[-2:] == '_1' or subreg_expand[-2:] == '_2':
                            subreg_expand = subreg_expand[:-2]
                        
                        ent_list = subreg_expand.split('|')
                        for ent in ent_list:
                            if ent[:4] == 'name':
                                continue
                            elif ent[:5] == 'brand':
                                a = self.check_item_brand(ent)
                            else:
                                a = self.check_item(ent)
                            subreg_expand = subreg_expand.replace(ent, a)
                            # if ent == 'effect':
                            #     print('effect')
                            #     print('subre', subreg_expand)
                        # if k == 'search_item' and p == "(有沒有)(推薦)(的)?(brand|color|effect)?(的)?(item|商品_commodity)":
                        #     print('subref', subreg_expand)
                        pattern = pattern.replace(subreg, subreg_expand)

                # print('*'*50)
                # print(pattern)
                try:
                    compiled = re.compile(pattern)
                except:
                    print(pattern)
                    exit(0)
                self.regex[k].append(compiled)

    def check_item(self, item):
        try:
            senses, terms = self.entity_info[item]
            # print('senses', senses)
            # print('terms', terms)
        except:
            return item
        sense_str_list = []
        
        terms = ['('+l+')' for l in terms]
        term_str = '|'.join(terms)
        if senses:
            for s in senses:
                sense_str = self.check_item(s)
                sense_str_list.append(sense_str)
            if terms:
                sense_str_list.append(term_str)
            return '|'.join(sense_str_list)
        else:
            return term_str

    def check_item_brand(self, item):
        try:
            senses, terms = self.entity_info[item]
            # print('senses', senses)
            # print('terms', terms)
        except:
            return item
        sense_str_list = []
        
        terms = ['('+l.replace('+', '\+').replace('.', '\.').replace('*', '\*').replace('(', '\(').replace(')', '\)').replace('=', '\=')+')' for l in terms]
        term_str = '|'.join(terms)
        if senses:
            for s in senses:
                sense_str = self.check_item_brand(s)
                sense_str_list.append(sense_str)
            if terms:
                sense_str_list.append(term_str)
            return '|'.join(sense_str_list)
        else:
            return term_str

    def check_intent(self, cmd):
        match_str = ""
        match_intent = None
        match_idx = 0
        for intent, reg_list in self.regex.items():
            for i, reg in enumerate(reg_list):
                search_str = re.search(reg, cmd)
                if search_str:
                    if len(search_str.group(0)) > len(match_str):
                        match_str = search_str.group(0)
                        match_intent = intent
                        match_idx = i
        if match_str == "":
            return "nomatch", "NO PATTERNS FOUND..."
        else:
            print('match_str', match_str)
            return match_intent, self.intent_pattern[match_intent][match_idx]

    def control(self, cmd):
        cmd_string, pattern_string = self.check_intent(cmd)
        return cmd_string, pattern_string

ctrl = Controller('app/pattern/intent_pattern.json', 'app/pattern/entity_info.json')




if __name__ == '__main__':
    ctrl = Controller('app/pattern/intent_pattern.json', 'app/pattern/entity_info.json')
    # ctrl = Controller('app/pattern/intent_pattern.json', 'ent.json')
    for k, v in ctrl.intent_pattern.items():
        print(k)
    # find_paren_exp = r'\(([\w\|]*)\)'

    # for k, p_list in ctrl.intent_pattern.items():
    #     for p in p_list:
    #         if p != "((brand_1)的)?(name)的(price|feeling|color|smell|volume|CP|url|brand_2|pic|listed_time|comment|effect|info|tips|article|texture)(是什麼|如何)":
    #             continue
    #         pattern = p
    #         m = re.findall(find_paren_exp, p)
    #         if m:
    #             # print('---------------------')
    #             # print('pattern', p)
    #             # print(m)
    #             for subreg in m:
    #                 subreg_expand = subreg
    #                 if subreg_expand[-2:] == '_1' or subreg_expand[-2:] == '_2':
    #                     subreg_expand = subreg_expand[:-2]
    #                 print('subreg', subreg_expand)
    #                 ent_list = subreg_expand.split('|')
    #                 for ent in ent_list:
    #                     a = ctrl.check_item(ent)
    #                     subreg_expand = subreg_expand.replace(ent, a)
    #                 pattern = pattern.replace(subreg, subreg_expand)

    #         # print('====')
    #         print('new pattern', pattern)
        
# 