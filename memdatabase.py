__author__ = 'cscharfe'


class PartialUpdateException(Exception):
    pass


class MemDatabase():
    def __init__(self):
        self.db = {}
        self._counter = 0

    def _increment_counter(self):
        self._counter += 1
        return self._counter

    def init_data(self, data):
        self.db = data.copy() if data else {}
        self._counter = len(data) if data else 0

    def get_item(self, car_id):
        if self.contains(car_id):
            return self.db["id" + str(car_id)]

    def get_all_items(self):
        return self.db

    def get_size(self):
        return len(self.db)

    def get_counter(self):
        return self._counter

    def contains(self, car_id):
        key = "id" + str(car_id)
        return True if self.db.has_key(key) else False

    def add_item(self,item_data):
        self._increment_counter()
        key = 'id' + str(self._counter)
        self.db[key] = item_data
        return self.get_counter()

    def remove_item(self, car_id):
        if self.contains(car_id):
            del self.db["id" + str(car_id)]

    def set_item(self, car_id_num, item_data):
        key = 'id' + str(car_id_num)
        self.db[key] = item_data
        return self.db[key]

    def partially_update_item(self, car_id, partial_item_data):
        key = 'id' + str(car_id)
        original_item = self.db[key]
        new_item = partial_item_data.copy()

        if all([x in original_item for x in partial_item_data]):
            for field in original_item:
                if not field in partial_item_data:
                    new_item[field] = original_item[field]
            return self.set_item(car_id, new_item)
        else:
            raise PartialUpdateException("unrecognized fields")




