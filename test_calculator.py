import unittest
import calculator
from collections import deque


class TestCalculator(unittest.TestCase):

    def test_convert_to_postfix(self):
        self.assertEqual(deque([12, 4, 2, "-", "*"]), calculator.convert_to_postfix(deque("12 * ( 4 - 2 )".split())))
        self.assertEqual(deque([10, 2, 8, "*", "+", 3, "-"]),
                         calculator.convert_to_postfix(deque("10 + 2 * 8 - 3".split())))
        self.assertEqual(deque([2, 3, "+"]), calculator.convert_to_postfix(deque("2 + 3".split())))
        self.assertEqual(deque([10, 2, "+", 8, "-", 3, "+"]),
                         calculator.convert_to_postfix(deque("10 + 2 - 8 + 3".split())))

    def test_normalize_input(self):
        self.assertEqual("8 * 3 + 12 * ( 4 - 2 )", calculator.normalize_input("8*3 + 12*(4-2)"))
        self.assertEqual("- 2 + 4 - 5 + 6", calculator.normalize_input("-2+4-5+6"))
        self.assertEqual("9 + 10 + 8", calculator.normalize_input("9+++10--8"))
        self.assertEqual("3 - 5", calculator.normalize_input("3---5"))
        self.assertEqual("14 - 12", calculator.normalize_input("+14-12"))
        self.assertEqual("5", calculator.normalize_input(" + 5"))
        self.assertEqual("- 5", calculator.normalize_input(" --- 5"))
        self.assertEqual("- 5 -", calculator.normalize_input(" + - +  5 - - -  "))
        self.assertEqual("n = 3", calculator.normalize_input("n = 3"))
        self.assertEqual("a = 5", calculator.normalize_input("a  =   5"))
        self.assertEqual("b = a", calculator.normalize_input("b = a"))
        self.assertEqual("v = 7", calculator.normalize_input("v=   7"))
        self.assertEqual("n = 9", calculator.normalize_input("n =9"))
        self.assertEqual("a", calculator.normalize_input(" a  "))
        self.assertEqual("a1 = 8", calculator.normalize_input("a1=8"))

    def test_eval_assignment_invalid(self):
        self.assertRaises(NameError, calculator.eval_assignment, deque(["a1", "=", "8"]))

    def test_eval_assignment(self):
        calculator.storage = {}

        calculator.eval_assignment(deque(["m", "=", "4"]))
        self.assertIn("m", calculator.storage)
        self.assertEqual(4, calculator.storage.get("m"))

        calculator.eval_assignment(deque(["m", "=", "25"]))
        self.assertIn("m", calculator.storage)
        self.assertEqual(25, calculator.storage.get("m"))

    def test_eval_expression_invalid(self):
        calculator.storage = {}
        self.assertRaises(TypeError, calculator.eval_expression, deque(["4", "*", "*", "2"]))
        self.assertRaises(KeyError, calculator.eval_expression, deque(["c"]))
        self.assertRaises(AssertionError, calculator.eval_expression, deque(["c21"]))

    def test_eval_expression(self):
        self.assertEqual(256, calculator.eval_expression(deque(["2", "^", "8"])))
        self.assertEqual(16, calculator.eval_expression(deque(["2", "*", "8"])))
        self.assertEqual(3, calculator.eval_expression(deque(["-", "2", "+", "4", "-", "5", "+", "6"])))
        self.assertEqual(-3, calculator.eval_expression(
            deque(["33", "+", "20", "+", "11", "+", "49", "-", "32", "-", "9", "+", "1", "-", "80", "+", "4"])))
        self.assertEqual(-7, calculator.eval_expression(deque(["23", "-", "17", "-", "13"])))
        self.assertEqual(8, calculator.eval_expression(deque(["8"])))
        self.assertEqual(27, calculator.eval_expression(deque(["9", "+", "10", "+", "8"])))
        self.assertEqual(-2, calculator.eval_expression(deque(["3", "-", "5"])))
        self.assertEqual(2, calculator.eval_expression(deque(["14", "-", "12"])))
        self.assertEqual(12, calculator.eval_expression(deque(["7", "+", "1", "+", "4"])))
        self.assertEqual(5, calculator.eval_expression(deque(["5"])))
