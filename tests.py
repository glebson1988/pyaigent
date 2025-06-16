import unittest
import os
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file


class TestGetFilesInfo(unittest.TestCase):

    def setUp(self):
        self.working_dir = "test_env"
        os.makedirs(self.working_dir, exist_ok=True)

        self.pkg_dir = os.path.join(self.working_dir, "pkg")
        os.makedirs(self.pkg_dir, exist_ok=True)

        self.test_file = os.path.join(self.working_dir, "README.md")
        with open(self.test_file, "w") as f:
            f.write("test content")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.isdir(self.pkg_dir):
            os.rmdir(self.pkg_dir)
        if os.path.isdir(self.working_dir):
            os.rmdir(self.working_dir)

    def test_valid_directory_listing(self):
        output = get_files_info(self.working_dir, ".")
        self.assertIn("README.md", output)
        self.assertIn("pkg", output)
        self.assertIn("file_size=", output)
        self.assertIn("is_dir=", output)

    def test_valid_subdirectory_listing(self):
        output = get_files_info(self.working_dir, "pkg")
        self.assertEqual(output.strip(), "")

    def test_directory_outside_working_dir_absolute(self):
        output = get_files_info(self.working_dir, "/bin")
        self.assertTrue(output.startswith("Error:"))
        self.assertIn("outside the permitted working directory", output)

    def test_directory_outside_working_dir_relative(self):
        output = get_files_info(self.working_dir, "../")
        self.assertTrue(output.startswith("Error:"))
        self.assertIn("outside the permitted working directory", output)

    def test_not_a_directory(self):
        output = get_files_info(self.working_dir, "README.md")
        self.assertTrue(output.startswith("Error:"))
        self.assertIn("is not a directory", output)

    def test_directory_does_not_exist(self):
        output = get_files_info(self.working_dir, "nonexistent_dir")
        self.assertTrue(output.startswith("Error:"))

print("Test 1: run_python_file('calculator', 'main.py')")
print(run_python_file("calculator", "main.py"))
print("\n----------------\n")

print("Test 2: run_python_file('calculator', 'tests.py')")
print(run_python_file("calculator", "tests.py"))
print("\n----------------\n")

print("Test 3: run_python_file('calculator', '../main.py')")
print(run_python_file("calculator", "../main.py"))
print("\n----------------\n")

print("Test 4: run_python_file('calculator', 'nonexistent.py')")
print(run_python_file("calculator", "nonexistent.py"))
print("\n----------------\n")


if __name__ == "__main__":
    unittest.main()
