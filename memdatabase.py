__author__ = 'cscharfe'

#in memory test db
class MemDatabase():
    def __init__(self):
        self.db = {}
        self.counter = 0

    def init_data(self, data):
        self.db = data
        self.counter = len(data)

    def get_all_items(self):
        return self.db

    def _increment_id(self):
        self.counter += 1
        return self.counter

    def add_item(self,item_data):
        self._increment_id()
        key = 'id' + str(self.counter)
        self.db[key] = item_data
        return self.counter

    def set_item(self, car_id, item_data):
        key = 'id' + str(car_id)
        self.db[key] = item_data
        return self.db[key]

    def partially_update_item(self, car_id, partial_item_data):
        key = 'id' + str(car_id)
        item = self.db[key]
        new_item_data = {}
        for field in partial_item_data.keys():
            new_item_data[field] = partial_item_data[field]

        for field in item.keys():
            if not field in partial_item_data.keys():
                new_item_data[field] = item[field]
        self.set_item(car_id, new_item_data)

    def get_item(self, car_id):
        return self.db["id" + str(car_id)]

    def contains(self, car_id):
        if self.db.has_key("id" + str(car_id)):
            return True
        else:
            return False

    def remove_item(self, car_id):
        if self.contains(car_id):
            del self.db["id" + str(car_id)]

    def get_size(self):
        return len(self.db)
