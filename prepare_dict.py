class PrepareDictBuilder:
    def __init__(self, dict_input):
        self.dict_ = dict_input
        self.__prepopulate()

    def set_acno(self, acno_):
        self.dict_["acno"] = acno_
        return self

    def set_type(self, type_):
        self.dict_["type"] = type_
        return self

    def set_cbg(self, cbg_):
        self.dict_["cbg"] = cbg_
        return self

    def set_source(self, source_):
        self.dict_["source"] = source_
        return self

    def build(self):
        return self.dict_

    def __prepopulate(self):
        self.set_acno(None)
        self.set_type(None)
        self.set_cbg(None)
        self.set_source(None)