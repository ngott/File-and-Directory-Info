import unittest
import file_info

class TestFileInfo(unittest.TestCase):

    def test_read_all_file_fields_exist(self):
        file_class = file_info.FileInfo("test", False)
        path_dict = file_class.build_and_write_to_json()
        self.assertEqual(path_dict["test"]["test/simple_file.txt"]["file name"], "simple_file.txt")
        self.assertEqual(path_dict["test"]["test/simple_file.txt"]["file size (bytes)"], 20)
        self.assertEqual(path_dict["test"]["test/simple_file.txt"]["file owner"], "nicholasgott")
        self.assertEqual(path_dict["test"]["test/simple_file.txt"]["file permissions (octal)"], "0o100644")
        self.assertEqual(path_dict["test"]["test/simple_file.txt"]["file content"], "I am a simple file.\n")

    def test_read_only(self):
        file_class = file_info.FileInfo("test", False)
        path_dict = file_class.build_and_write_to_json()
        self.assertEqual(path_dict["test"]["test/test_read_only_file"]["file permissions (octal)"], "0o100444")

    def test_hidden_file(self):
        file_class = file_info.FileInfo("test", False)
        path_dict = file_class.build_and_write_to_json()
        self.assertEqual(path_dict["test"]["test/.hidden_file.txt"]["file name"], ".hidden_file.txt")

    def test_new_lines_present(self):
        file_class = file_info.FileInfo("test", False)
        path_dict = file_class.build_and_write_to_json()
        self.assertIn("\n",path_dict["test"]["test/only_new_lines.txt"]["file content"])

    def test_deep_directory(self):
        file_class = file_info.FileInfo("test", False)
        path_dict = file_class.build_and_write_to_json()
        self.assertEqual(path_dict["test"]["test/test_deep_dir"]["test/test_deep_dir/level_2"]["test/test_deep_dir/level_2/level_3"]["test/test_deep_dir/level_2/level_3/test_burried_file.txt"]["file name"], "test_burried_file.txt")

    def test_deep_directory_hidden(self):
        file_class = file_info.FileInfo("test", False)
        path_dict = file_class.build_and_write_to_json()
        self.assertEqual(path_dict["test"]["test/test_deep_dir"]["test/test_deep_dir/level_2"]["test/test_deep_dir/level_2/level_3"]["test/test_deep_dir/level_2/level_3/.test_burried_hidden_file.txt"]["file name"], ".test_burried_hidden_file.txt")

    def test_dir_not_in_deep_dir(self):
        file_class = file_info.FileInfo("test/test_deep_dir", False)
        path_dict = file_class.build_and_write_to_json()
        with self.assertRaises(Exception) as e:
            _ = path_dict["test"]


if __name__ == '__main__':
    unittest.main()