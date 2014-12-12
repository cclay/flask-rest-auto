__author__ = 'cscharfe'

import unittest
import memdatabase
from dbdata import DB_DATA as TEST_DB_DATA
from jsontextfields import TXT_FIELDS

class InitDataTestCase(unittest.TestCase):
    def setUp(self):
        self.memdb = memdatabase.MemDatabase()

    def test_db_has_same_amount_of_items_and_values_as_supplied(self):
        self.memdb.init_data(TEST_DB_DATA)

        initial_TEST_DB_DATA_size = len(TEST_DB_DATA)

        self.assertTrue(len(self.memdb.db), initial_TEST_DB_DATA_size)
        self.assertTrue(self.memdb._counter, initial_TEST_DB_DATA_size)
        self.assertEqual(self.memdb.db, TEST_DB_DATA)

    def test_modify_data_source_after_initialization_does_not_change_db(self):
        self.memdb.init_data(TEST_DB_DATA)

        TEST_DB_DATA["id3"] = {"description":"green"}

        self.assertNotEqual(len(self.memdb.db), len(TEST_DB_DATA))

    def test_init_data_null_case(self):
        self.memdb.init_data(None)

        self.assertEqual({}, self.memdb.db)


class InitializedMemDatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.memdb = memdatabase.MemDatabase()
        self.memdb.init_data(TEST_DB_DATA)

    def test_contains_is_true_when_item_is_in_db(self):
        self.assertTrue(self.memdb.contains(1))

    def test_contains_is_false_when_item_is_not_in_db(self):
        self.assertFalse(self.memdb.contains(200))

    def test_get_item_returns_single_item(self):
        self.assertEqual(TEST_DB_DATA["id1"], self.memdb.get_item(1))

    def test_get_all_items_size_is_same_as_source(self):
        self.assertEqual(len(TEST_DB_DATA), len(self.memdb.get_all_items()))
        self.assertEqual(TEST_DB_DATA, self.memdb.get_all_items())

    def test_get_all_items_size_changes_afer_manually_adding_item(self):
        new_values = {"key1": "value1", "key2": "value2"}
        self.memdb.db["new_item"] = new_values

        self.assertEqual(len(TEST_DB_DATA) + 1, len(self.memdb.get_all_items()))
        self.assertNotEqual(TEST_DB_DATA, self.memdb.get_all_items())
        self.assertIn("new_item", self.memdb.get_all_items())
        self.assertEqual(new_values, self.memdb.get_all_items()["new_item"])

    def test_get_counter_no_db_init_data_called(self):
        self.memdb = memdatabase.MemDatabase()

        self.assertEqual(0, self.memdb.get_counter())

    def test_get_counter_normal_db_init(self):
        self.assertEqual(len(TEST_DB_DATA), self.memdb.get_counter())

    def test_get_size_returns_size_of_db(self):
        self.assertEqual(len(self.memdb.get_all_items()), self.memdb.get_size())



    def test_add_item_actually_adds_item_to_db(self):
        counter_before_adding = self.memdb.get_counter()
        new_item_data = {"description": "tesla", "engine": "V8-300"}

        self.assertEqual(TEST_DB_DATA, self.memdb.get_all_items())
        self.assertEqual(counter_before_adding, len(self.memdb.get_all_items()))

        added_id_num = self.memdb.add_item(new_item_data)  #Add the item

        self.assertNotEqual(TEST_DB_DATA, self.memdb.get_all_items())
        self.assertEqual(counter_before_adding + 1, len(self.memdb.get_all_items()))
        self.assertTrue(self.memdb.contains(added_id_num))

    def test_remove_item_removes_single_item_from_db(self):
        id_to_remove = 1
        item_count_before = self.memdb.get_size()

        self.memdb.remove_item(id_to_remove)

        self.assertEqual(item_count_before, self.memdb.get_size() + 1)
        self.assertFalse(self.memdb.contains(id_to_remove))

    def test_add_remove_add_item_second_item_added_has_different_counter_id_assigned(self):
        test_item_data = {"description": "tesla", "engine": "V8-300"}

        first_added_item_id = self.memdb.add_item(test_item_data)
        self.memdb.remove_item(first_added_item_id)
        second_added_item_id = self.memdb.add_item(test_item_data)

        self.assertNotEqual(first_added_item_id, second_added_item_id)
        self.assertEqual(first_added_item_id + 1, second_added_item_id)


    def test_set_item_erases_item_data_and_resets_with_new_data(self):
        test_item_data = {"test_description": "tesla", "test_engine": "V8-300"}
        id_to_set = 1
        item_to_set = self.memdb.get_item(id_to_set)

        for original_field in TXT_FIELDS:
            self.assertIn(original_field, item_to_set)

        newly_set_item = self.memdb.set_item(id_to_set,test_item_data)

        for original_field in TXT_FIELDS:
            self.assertNotIn(original_field, newly_set_item)
        for new_field in test_item_data:
            self.assertIn(new_field, newly_set_item)

    def test_partially_update_item_updates_fields(self):
        partial_update_data = {"description": "tesla", "engine": "V8-300"}
        id_to_update = 1
        original_item_to_update = self.memdb.get_item(id_to_update)

        updated_item = self.memdb.partially_update_item(id_to_update,partial_update_data)

        for field in partial_update_data:
            self.assertEqual(partial_update_data[field], updated_item[field])
        for field in TXT_FIELDS:
            if field not in partial_update_data:
                self.assertEqual(original_item_to_update[field], updated_item[field])


    def test_partially_update_item_doesnt_update_previously_unknown_fields(self):
        partial_update_data = {"heartrate": "120bpm", "temperature(C)": "37"}
        id_to_update = 1

        self.assertRaises(
            memdatabase.PartialUpdateException,
            self.memdb.partially_update_item,
            id_to_update,
            partial_update_data
        )

    def test_modifying_parameters_after_partially_update_item_call_will_not_change_updated_item_data(self):
        partial_update_data = {"description": "roadster (new)"}
        updated_item = self.memdb.partially_update_item(1, partial_update_data)

        partial_update_data["new_field"] = "new value"

        self.assertNotIn("new_field", updated_item)
