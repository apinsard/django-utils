# -*- coding: utf-8 -*-
from django.test import TestCase
from djutils.utils.parsing import expand_curly_braces


class ExpandCurlyBracesTestCase(TestCase):

    def test_simple(self):
        expr = 'foo{bar,baz}bar'
        expected = ['foobarbar', 'foobazbar']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_leading(self):
        expr = '{foo,bar}baz'
        expected = ['foobaz', 'barbaz']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_trailing(self):
        expr = 'foo{bar,baz}'
        expected = ['foobar', 'foobaz']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_full(self):
        expr = '{foo,bar,baz}'
        expected = ['foo', 'bar', 'baz']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_leading_comma(self):
        expr = 'foo{,bar}'
        expected = ['foo', 'foobar']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_trailing_comma(self):
        expr = 'foo{bar,}'
        expected = ['foobar', 'foo']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_two(self):
        expr = '{foo,bar}baz{foo,bar}'
        expected = ['foobazfoo', 'foobazbar', 'barbazfoo', 'barbazbar']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_nested(self):
        expr = '{foo{r,},ba{r,z}}'
        expected = ['foor', 'foo', 'bar', 'baz']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_overly_nested(self):
        expr = '{f{o{o{b{a{r,r},a},b},o},o},f}'
        expected = ['foobar', 'foobar', 'fooba', 'foob', 'foo', 'fo', 'f']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_empty_braces(self):
        expr = 'foo{}bar'
        expected = ['foobar']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_single_comma(self):
        expr = 'foo{,}bar'
        expected = ['foobar', 'foobar']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_escape_braces(self):
        expr = 'foo\{bar,baz\}'
        expected = ['foo{bar,baz}']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_escape_comma(self):
        expr = 'foo{bar\,baz,baz\,bar}'
        expected = ['foobar,baz', 'foobaz,bar']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_no_comma(self):
        expr = 'foo{bar}baz'
        expected = ['foobarbaz']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_missing_closing_brace(self):
        expr = 'foo{bar'
        with self.assertRaises(ValueError):
            list(expand_curly_braces(expr))

    def test_missing_opening_brace(self):
        expr = 'bar}foo'
        with self.assertRaises(ValueError):
            list(expand_curly_braces(expr))

    def test_comma_without_braces(self):
        expr = 'foo,bar'
        expected = ['foo,bar']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_double_comma(self):
        expr = 'foo{,,}bar'
        expected = ['foobar', 'foobar', 'foobar']
        self.assertListEqual(list(expand_curly_braces(expr)), expected)

    def test_missing_nested_closing_brace(self):
        expr = 'foo{ba{r,z'
        with self.assertRaises(ValueError):
            list(expand_curly_braces(expr))
