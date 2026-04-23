class Windows:
    def __init__(self) -> None:
        self.__obj_lst = []

    def add_obj(self, obj):
        self.__obj_lst.append(obj)

    def render(self, screen): 