#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pset_1` package."""

import os
from tempfile import TemporaryDirectory
from unittest import TestCase

from {{cookiecutter.repo_name}}.{{ cookiecutter.project_slug }}.hash_str import hash_str, get_csci_salt, get_user_id
from {{cookiecutter.repo_name}}.{{ cookiecutter.project_slug }}.io import atomic_write


import pandas as pd
from {{cookiecutter.repo_name}}.{{ cookiecutter.project_slug }}.__main__ import get_user_hash, excel_to_parquet, get_parquet_columns


from contextlib import contextmanager

@contextmanager
def set_environment(**kwargs):
    '''Set dummy environment for testing with reading salt from the environment'''
    env_variables = dict(os.environ)
    os.environ.update(kwargs)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(env_variables)


class FakeFileFailure(IOError):
    pass


class HashTests(TestCase):
    """Ensures that hash_str works as expected for valid values of the string and salt"""
    def test_hashes(self):
        self.assertEqual(hash_str("world!", salt="hello, ").hex()[:6], "68e656")
        self.assertEqual(hash_str("World!", salt="hello, ").hex()[:6], "68e656")
        self.assertEqual(hash_str("wOrLd!", salt="hello, ").hex()[:6], "68e656")
        self.assertEqual(hash_str("World!", salt="hello, ").hex()[:6], "68e656")
        self.assertEqual(hash_str("World!", salt="hello, ").hex()[:6], "68e656")
        self.assertEqual(hash_str("", salt="").hex()[:6], "e3b0c4")



    def test_hash_errors(self):
        """Ensures that hash_str() handles negative values and decimal values as expected"""
        self.assertRaises(TypeError, hash_str, 10.01)
        self.assertRaises(TypeError, hash_str, "hello", salt=-1)
        self.assertRaises(TypeError, hash_str, "hello", salt=None)


    def test_get_csci_salt(self):
        """Ensures that get_csci_salt() returns the CSCI salt from environment variables"""
        salt = "saltx".encode()
        salt_hex = salt.hex()

        with set_environment(CSCI_SALT=salt_hex):
            self.assertEqual(get_csci_salt(), salt)

    def test_get_user_id(self):
        salt = "saltx".encode()
        salt_hex = salt.hex()
        with set_environment(CSCI_SALT=salt_hex):
            self.assertEqual(get_user_id("rpc0"), "eb740031")
            self.assertEqual(get_user_id("gorlins"), "a7ea3c11")


class AtomicWriteTests(TestCase):
    def test_atomic_write(self):
        """Ensure file exists after being written successfully"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with atomic_write(fp, "w") as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                f.write("asdf")

            assert not os.path.exists(tmpfile)
            assert os.path.exists(fp)

            with open(fp) as f:
                self.assertEqual(f.read(), "asdf")


    def test_atomic_failure(self):
        """Ensure that file does not exist after failure during write"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with self.assertRaises(FakeFileFailure):
                with atomic_write(fp, "w") as f:
                    tmpfile = f.name
                    assert os.path.exists(tmpfile)
                    raise FakeFileFailure()

            assert not os.path.exists(tmpfile)
            assert not os.path.exists(fp)


    def test_file_exists(self):
        """Ensure an error is raised when a file exists"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")
            file = open(os.path.join(tmp, "asdf.txt"), "w+")
            file.close()

            with self.assertRaises(FileExistsError):
                with atomic_write(fp, "w") as f:
                    print("Running test...")


    def test_as_file_false(self):
        """Ensure that when as_file is set to False a string representing path to a temporary file is returned"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with atomic_write(fp, "w", as_file=False) as f:
                self.assertIsInstance(f, str)



class SaltTests(TestCase):

    def test_get_user_hash(self):
        self.assertEqual(get_user_hash("rpc0", salt="somebody").hex()[:6], "27f823")




class ParquetTests(TestCase):

    def test_excel_to_parquet(self):
        '''Ensures excel_to_parquet converts correctly to parquet format'''
        with TemporaryDirectory() as tmp:

            # Prepare temp file paths for testing
            xlsx_file = os.path.join(tmp, "asdf.xlsx")
            parquet_file = os.path.join(tmp, "asdf.parquet")

            # Create a DataFrame with some dummy data
            df = pd.DataFrame({"gorlins": ["hello", "world"], "rpc0": ["world", "hello"]})

            # Save the DataFrame to an xlsx file at tmp/asdf.xlsx using atomic_write
            with atomic_write(xlsx_file, as_file=False) as f:
                df.to_excel(f)

            # Convert the excel file to a parquet file
            parquet_converted_from_excel = excel_to_parquet(xlsx_file)

            # Ensure the file exists
            self.assertTrue(os.path.exists(parquet_file))

            # Ensure that the parquet file is created in the correct location
            self.assertEqual(parquet_file, parquet_converted_from_excel)

            # Read back the parquet file
            parquet_df = pd.read_parquet(parquet_file, engine="fastparquet")
            xlsx_read_df = pd.read_excel(xlsx_file)

            # Ensure that the data stored is the data intended to be written
            self.assertTrue(xlsx_read_df.equals(parquet_df))


    def test_get_parquet_columns(self):
        '''Ensures get_parquet_columns returns the right columns from the right files'''
        with TemporaryDirectory() as tmp:
            parquet_file = os.path.join(tmp, "asdf.parquet")

            # Create a DataFrame with some dummy data
            df = pd.DataFrame({"column1": ["hello", "world"], "column2": ["world", "hello"]})

            # Save the DataFrame to a parquet file using atomic_write
            with atomic_write(parquet_file, as_file=False) as f:
                df.to_parquet(f, engine="fastparquet", compression="GZIP")

            # Ensure that the values match
            for columns in [["column1"], ["column2"], ["column1", "column2"]]:
                df_read_from_parquet = get_parquet_columns(parquet_file, columns)
                self.assertIsInstance(df_read_from_parquet, pd.DataFrame)
                self.assertTrue(df_read_from_parquet.equals(df[columns]))


    def test_parquet_inputs_bad(self):
        '''Ensures that parquet functions raise exceptions if the input files are not found'''
        with TemporaryDirectory() as tmp:
            self.assertRaises(FileNotFoundError, excel_to_parquet, "asdf.parquet")
            self.assertRaises(FileNotFoundError, get_parquet_columns, "asdf.parquet", ["hashed_id"])

