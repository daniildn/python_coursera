'''It's working. '''

class TestFactorize(unittest.TestCase):
    # Type float and str (value 'string', 1.5)
    # TypeError is raised.
    def test_wrong_types_raise_exception(self):
        with self.subTest(x="string"):
            self.assertRaises(TypeError, factorize, "string")

        with self.subTest(x=1.5):
            self.assertRaises(TypeError, factorize, 1.5)

    # For negative num -1, -10 и -100
    # ValueError is raised.
    def test_negative(self):
        for x in -1, -10, -100:
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    # For 0 tuple (0,) is returned,
    # and for 1 tuple (1,) is returned
    def test_zero_and_one_cases(self):
        for x in 0, 1:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), (x,))

    # Что для простых чисел 3, 13, 29 возвращается кортеж,
    # содержащий одно данное число.
    def test_simple_numbers(self):
        for x in 3, 13, 29:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), (x,))

    # Что для чисел 6, 26, 121
    # возвращаются соответственно кортежи (2, 3), (2, 13) и (11, 11).
    def test_two_simple_multipliers(self):
        with self.subTest(x=6):
            self.assertEqual(factorize(6), (2, 3))

        with self.subTest(x=26):
            self.assertEqual(factorize(26), (2, 13))

        with self.subTest(x=121):
            self.assertEqual(factorize(121), (11, 11))

    # Что для чисел 1001 и 9699690 возвращаются соответственно
    # кортежи (7, 11, 13) и (2, 3, 5, 7, 11, 13, 17, 19).
    def test_many_multipliers(self):
        with self.subTest(x=1001):
            self.assertEqual(factorize(1001), (7, 11, 13))

        with self.subTest(x=9699690):
            self.assertEqual(factorize(9699690), (2, 3, 5, 7, 11, 13, 17, 19))
