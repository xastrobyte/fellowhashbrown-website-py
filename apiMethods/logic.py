import os, requests, traceback
from flask import jsonify

class UnbalancedParentheses(Exception): pass
class MissingTruthValue(Exception): pass
class OperatorMismatch(Exception): pass
class MissingValue(Exception): pass

class LogicVar:
    """A class for a Logic Variable inside a Logical Expression (LogicNode).

        Args:
            value (str): The variable that is being stored in this LogicVar. Defaults to None.
            has_not (bool): Whether or not this LogicVar has a ~ (NOT) operator attached to it. Defaults to False.
            var_dict (dict): A dictionary containing both values above to allow for recursive object initialization.
    """

    PSEUDO = 1
    LOGIC = 2
    JAVA = 3

    OPERATORS = ["not", "~", "!"]

    # Built-in Methods
    def __init__(self, value = None, has_not = False, *, operator_type = None, var_dict = None):

        # Check if value is None or var_dict is None
        if value == None and var_dict == None:
            raise MissingValue("Required variable for LogicVar. Must use either value or var_dict.")
        
        # Check if value is not None
        elif value != None:
            self._value = value
            self._has_not = has_not
        
        # Check if var_dict is not None
        elif var_dict != None:

            # Try to load value
            try:
                self._value = var_dict["value"]
            except:
                raise MissingValue("Required key for LogicVar. Must have \"value\" key in var_dict.")
            
            # Try to load has_not
            try:
                self._has_not = var_dict["has_not"]
            except:
                self._has_not = has_not
    
    def __str__(self):
        """Returns the string representation of this LogicVar object.
        """
        if self.has_not():
            return "~" + self.get_value()
        return self.get_value()
    
    def __eq__(self, compare):
        """Compares this LogicVar object with another object.
        """
        if type(compare) != LogicVar:
            return False
        return (
            self.get_value() == compare.get_value() and
            self.has_not() == compare.has_not()
        )
    
    # Getter Methods
    def get_value(self):
        """Returns the value that is stored in this LogicVar.
        """
        return self._value
    
    def has_not(self):
        """Returns whether or not this LogicVar has a ~ (NOT) operator attached to it.
        """
        return self._has_not
    
    def get_not(self):
        """Returns the NOT operator symbol based off of the operator type.
        """
        return LogicVar.OPERATORS[self.get_operator_type()]
    
    def get_operator_type(self):
        """Returns the type of operator this LogicVar has by number.
        """
        return self._operator_type
    
    # Evaluation Methods
    def get_truth_values(self, truth_values = []):
        """Creates the truth values for this LogicVar.

            Args:
                truth_values (list): A list of truth values wrapped in dictionarys to test against this LogicVar.

            Returns:
                A list of truth values for this LogicVar.
        """

        # Keep track of evaluations
        evaluations = []

        # Only run this if there is a has_not
        if not self.has_not():
            return evaluations
        
        # Iterate through truth values
        for truth_value in truth_values:
            evaluation = {
                "expression": str(self),
                "truth_value": truth_value,
                "value": self.evaluate(truth_value)
            }

            # Only add the evaluation if it doesn't already exist
            if evaluation not in evaluations:
                evaluations.append(evaluation)
        
        return evaluations
    
    def evaluate(self, truth_value = {}):
        """Evaluates the LogicVar given the truth values to use to evaluate it.

            Args:
                truth_value (dict): A dictionary of truth values to use to evaluate this LogicVar.
            
            Raises:
                MissingTruthValue: When the truth value for this LogicVar does not exist in truth_value.
        """
        if self.get_value() not in truth_value:
            raise MissingTruthValue("Required truth value for the variable \"{}\"".format(self.get_value()))
        
        if self.has_not():
            return not truth_value[self.get_value()]
        
        return truth_value[self.get_value()]

class LogicNode:
    """A class for the Logic Node of a LogicTree.

        Args:
            operator (int): The operator this LogicNode holds.
            left (LogicNode | LogicVar): The left side of this LogicNode.
            right (LogicNode | LogicVar): The right side of this LogicNode.
            has_not (bool): Whether or not this LogicNode has a ~ (NOT) operator attached to it. Defaults to False.
            operator_type (int): The type of operator this LogicNode represents.
            node_dict (dict): A dictionary containing all values above to allow for recursive object initialization.
    """

    NOT = 0
    AND = 1
    OR = 2
    IMPLIES = 3
    BICONDITIONAL = 4
    NAND = 5
    NOR = 6

    PSEUDO = 0
    LOGIC = 1
    JAVA = 2

    OPERATORS = [
        ["not", "and", "or", "implies", "iff", "nand", "nor"],
        ["~", "^", "v", "->", "<->", "|", "⬇"],
        ["!", "&&", "||", "->", "<->", "|", "⬇"]
    ]

    # Built-in Methods
    def __init__(self, operator = None, left = None, right = None, has_not = False, *, operator_type = None, node_dict = None):

        # Check if operator, left, and right and node_dict are all None
        if operator == left == right == node_dict == None:
            raise MissingValue("Required variable(s) for LogicNode. Must use either operator, left, and right or node_dict.")
        
        # Check if operator, left, and right exist
        elif operator != None and left != None and right != None:
            self._operator = operator
            self._left = left
            self._right = right
            self._has_not = has_not
        
        # Check if node_dict exists
        elif node_dict != None:
            
            # Try loading operator
            try:
                self._operator = node_dict["operator"]
            except:
                raise MissingValue("Required key for LogicNode. Must have \"operator\" key in node_dict.")
            
            # Try loading left
            try:
                self._left = node_dict["left"]
            except:
                raise MissingValue("Required key for LogicNode. Must have \"left\" key in node_dict.")
            
            # Try loading right
            try:
                self._right = node_dict["right"]
            except:
                raise MissingValue("Required key for LogicNode. Must have \"right\" key in node_dict.")
            
            # Try loading has_not
            try:
                self._has_not = node_dict["has_not"]
            except:
                self._has_not = has_not
            
            # Try loading operator_type
            try:
                self._operator_type = node_dict["operator_type"]
            except:
                self._operator_type = LogicNode.LOGIC
        
        self._operator_type = self._operator_type if self._operator_type != None else LogicNode.LOGIC
        
        # Load values as they should be (LogicNode | LogicVar)
        if type(self._left) == dict:
            if "value" in self._left:
                self._left = LogicVar(var_dict = self._left)
            else:
                self._left = LogicNode(node_dict = self._left)
        
        if type(self._right) == dict:
            if "value" in self._right:
                self._right = LogicVar(var_dict = self._right)
            else:
                self._right = LogicNode(node_dict = self._right)
        
    def __str__(self):
        """Returns the string representation of this LogicNode object.
        """
        left = str(self.get_left())
        right = str(self.get_right())

        if type(self.get_left()) == LogicNode and not self.get_left().has_not():
            left = "(" + left + ")"
        if type(self.get_right()) == LogicNode and not self.get_right().has_not():
            right = "(" + right + ")"

        operator = self.get_operator()

        if self.has_not():
            return "~({} {} {})".format(
                left, operator, right
            )
        
        return "{} {} {}".format(
            left, operator, right
        )
    
    def __eq__(self, compare):
        """Compares this LogicNode object with another object.
        """
        if type(compare) != LogicNode:
            return False
        return (
            self.get_left() == compare.get_left() and 
            self.get_right() == compare.get_right() and
            self.get_operator_type() == compare.get_operator_type() and
            self.has_not() == compare.has_not()
        )
    
    # Getter Methods
    def get_operator_type(self):
        """Returns the type of operator this LogicNode has by number.
        """
        return self._operator_type
    
    def get_operator(self):
        """Returns the actual operator this LogicNode shows.
        """
        return LogicNode.OPERATORS[self.get_operator_type()][self._operator]
    
    def get_left(self):
        """Returns the left side of this LogicNode expression.
        """
        return self._left
    
    def get_right(self):
        """Returns the right side of this LogicNode expression.
        """
        return self._right
    
    def has_not(self):
        """Returns whether or not this LogicNode expression has a NOT operator attached to it.
        """
        return self._has_not
    
    def get_truth_values(self, truth_values = []):
        """Creates the truth values for this LogicNode.

            Args:
                truth_values (list): A list of truth values wrapped in dictionarys to test against this LogicNode.

            Returns:
                A list of truth values for this LogicNode.
        """

        # Keep track of evaluations
        evaluations = []

        # Get left evaluations
        left_evaluations = self.get_left().get_truth_values(truth_values)
        for left_evaluation in left_evaluations:
            if left_evaluation not in evaluations:
                evaluations.append(left_evaluation)
        
        # Get right evaluations
        right_evaluations = self.get_right().get_truth_values(truth_values)
        for right_evaluation in right_evaluations:
            if right_evaluation not in evaluations:
                evaluations.append(right_evaluation)
        
        # Iterate through all the truth values
        for truth_value in truth_values:

            # Evaluate self
            self_evaluation = self.evaluate(truth_value)
            self_evaluation = {
                "expression": str(self),
                "truth_value": truth_value,
                "value": self_evaluation
            }

            # Only add the evaluation if it doesn't already exist
            if self_evaluation not in evaluations:
                evaluations.append(self_evaluation)
        
        return evaluations
    
    def evaluate(self, truth_value = {}, include_not = True):
        """Evaluates this LogicNode expression.

            Args:
                truth_value (dict): The dictionary of truth values to use to evaluate this LogicNode expression.
                include_not (bool): Whether or not to include the NOT operator in the evaluation.
            
            Returns:
                The evaluation of this LogicNode expression.
        """

        left = self.get_left().evaluate(truth_value)
        right = self.get_right().evaluate(truth_value)

        if self._operator == LogicNode.AND:
            if self.has_not():
                return not (left and right)
            return left and right
        
        if self._operator == LogicNode.OR:
            if self.has_not():
                return not (left or right)
            return left or right
        
        if self._operator == LogicNode.IMPLIES:
            if self.has_not():
                return not (not left or right)
            return not left or right
        
        if self._operator == LogicNode.BICONDITIONAL:
            if self.has_not():
                return not (left == right)
            return left == right
        
        if self._operator == LogicNode.NAND:
            if self.has_not():
                return left and right
            return not (left and right)
        
        if self._operator == LogicNode.NOR:
            if self.has_not():
                return left or right
            return not (left or right)

OPERATORS = {
    "NAND": "|",
    "nand": "|",

    "NOR": "⬇",
    "nor": "⬇",

    "OR": "v",
    "or": "v",
    "||": "v",

    "AND": "^",
    "and": "^",
    "&&": "^",

    "NOT ": "~",
    "not ": "~",
    "NOT": "~",
    "not": "~",
    "!": "~",
    
    "IFF": "-",
    "iff": "-",
    "<->": "-",

    "IMPLIES": ">",
    "implies": ">",
    "->": ">"
}

class LogicTree:
    """A class for a LogicTree that represents a logical expression.

        Args:
            expression (str): The 
    """

    def __init__(self, expression):
        self._expression = expression
        self._variables = []
        self._root = None
        self.parse()
    
    def __str__(self):
        """Returns the string representation of this LogicTree object.
        """
        return str(self._root)
    
    def __eq__(self, compare):
        """Compares this LogicTree object with another object.
        """

        return (
            self._expression == compare._expression and
            self._variables == compare._variables and
            self._root == compare._root
        )
    
    def get_expression(self):
        """Returns the parsed expression.
        """
        return self._expression
    
    def get_variables(self):
        """Returns the variables found in the expression.
        """
        return self._variables
    
    def parse(self):
        """Parses the logical expression.
        """
        exp = parse_expression(self.get_expression())
        expression = exp["expression"]
        variables = exp["variables"]

        self._root = LogicNode(node_dict = expression)

        self._variables = variables
        self._expression = str(self._root)
    
    def show_when_true(self):
        """Returns a list of values when the expression is True."""
        
        # Create the truth values and get only the results of the root expression
        truth_values = self.get_truth_values()
        values = []
        for truth in truth_values:
            if truth["expression"] == str(self) and truth["value"]:
                values.append(truth)
        
        return values
        
    def show_when_false(self):
        """Returns a list of values when the expression is False."""
        
        # Create the truth values and get only the results of the root expression
        truth_values = self.get_truth_values()
        values = []
        for truth in truth_values:
            if truth["expression"] == str(self) and not truth["value"]:
                values.append(truth)
        
        return values
    
    def make_table(self):
        """Returns a truth table for this logical expression."""

        lines = []
        result = ""

        # Setup truth table
        evaluations = self.get_truth_values()
        table_dict = {}
        for evaluation in evaluations:
            if evaluation["expression"] not in table_dict:
                table_dict[evaluation["expression"]] = []
            
            table_dict[evaluation["expression"]].append(evaluation["value"])

        # Add column labels
        count = 0
        length = len(table_dict)
        for column in table_dict:
            line = "| " + column.center(len(column))
            if count > 0:
                line = " " + line
            if count == length - 1:
                line += " |"
            result += line
            count += 1
        lines.append(result)
        result = ""

        # Add label split lin
        count = 0
        for column in table_dict:
            line = "+" + "-".center(len(column) + 1, "-")
            if count > 0:
                line = "-" + line
            if count == length - 1:
                line += "-+"
            result += line
            count += 1
        lines.append(result)
        result = ""

        # Add truth values
        max_truths = -1
        for column in table_dict:
            if max_truths == -1:
                max_truths = len(table_dict[column])
                break
        
        for index in range(max_truths):
            count = 0
            for column in table_dict:
                value = table_dict[column][index]
                value = "T" if value == True else ("F" if value == False else "-")
                line = "| " + value.center(len(column))
                if count > 0:
                    line = " " + line
                if count == length - 1:
                    line += " |"
                result += line
                count += 1
            lines.append(result)
            result = ""

        return lines

    def get_truth_values(self):
        """Returns all the truth values for the LogicNode expression."""
        
        # Create every possible truth combination for all variables
        truth_values = []

        # Iterate through 2 ** variable_amount possible combinations
        for value in range(2 ** len(self.get_variables())):

            # Iterate through all variables
            value_dict = {}
            for index in range(len(self.get_variables())):

                # Get the power based off of the variable's index in the list
                power = len(self.get_variables()) - index - 1
                variable = self.get_variables()[index]

                # Get the truth value using the get_truth_value function
                value_dict[variable] = get_truth_value(value, power)
            
            truth_values.append(value_dict)
        
        # Create truth values for other operations
        # For example, if there is a "~a", then there will be a column designated to that.
        #              if there is a "~(a v b)", then there will be a column designated to that
        #                 as well as the "a v b" part.
        truth_evaluations = []

        root_truth_evaluations = self._root.get_truth_values(truth_values)

        # Add all the truth evaluations from the root
        for truth_evaluation in root_truth_evaluations:
            if truth_evaluation not in truth_evaluations:
                truth_evaluations.append(truth_evaluation)
            
        # Add all the truth values as evaluations
        for truth_value in truth_values:
            for truth_variable in truth_value:
                truth_evaluation = {
                    "expression": truth_variable,
                    "truth_value": {
                        truth_variable: truth_value[truth_variable]
                    },
                    "value": truth_value[truth_variable]
                }
                
                truth_evaluations.append(truth_evaluation)
        
        truth_evaluations = sorted(truth_evaluations, key = lambda i: len(i["expression"])) 
        
        return truth_evaluations
    
def get_truth_value(value, power):
    """Returns the truth value for the specific value of a variable."""
    return ((value // 2 ** power) % 2) == 0

def is_expression_valid(expression):
    """Returns whether or not the expression is valid."""

    # Remove parentheses and spaces and nots
    expression = expression.replace("(", "").replace(")", "").replace(" ", "").replace("~", "")

    # Iterate through operators and split by it
    # Find if there are variables containing multiple characters
    for operator in LogicNode.OPERATORS[LogicNode.LOGIC]:
        token_split = expression.split(operator)
        if len(token_split) > 1:

            # Go through each index of the token_split list
            # And check if the item has length > 1
            for item in token_split:

                # Check if length of item is greater than 1
                if len(item) > 1:

                    # Check if item has an operator in last or first index
                    if item[0] in LogicNode.OPERATORS[LogicNode.LOGIC] or item[-1] in LogicNode.OPERATORS[LogicNode.LOGIC]:
                        return False

                    # Check if item has any operators
                    elif len([op for op in LogicNode.OPERATORS[LogicNode.LOGIC] if op in item]) == 0:
                        return False
                    
                    # recursive call
                    return is_expression_valid(item)
                
                # Check if length of item is 0
                elif len(item) == 0:
                    return False
        
    return True   
                

def parse_expression(expression, has_not = False, operator_type = None):
    """Parses a logical expression recursively.

        Args:
            expression (str): The logical expression to parse.
            has_not (bool): Whether or not the logical expression has a NOT operator attached to it. Used most during recursion.
        
        Returns:
            A dictionary of the expression split up into left and right sides, the operator, and the NOT gate.
    """

    # Remove all spaces from the expression
    expression = expression.replace(" ", "")

    # Go through all operators and replace expressions
    for operator in OPERATORS:

        # Find first operator that can be replaced and set operator_type to the proper type
        if operator in expression and operator_type == None:

            # Iterate through operator_types
            for op_type in [LogicNode.LOGIC, LogicNode.JAVA, LogicNode.PSEUDO]:
                if operator.lower() in LogicNode.OPERATORS[op_type]:
                    operator_type = op_type
                    break
            
            if operator_type == None:
                operator_type = LogicNode.LOGIC
        
        # Standardize all operators to LOGIC type
        expression = expression.replace(operator, OPERATORS[operator])
    
    # Loop through and find any ^ (AND) or v (OR) operators as expressions
    has_not = has_not
    left = None
    operator = None
    right = None
    variables = []

    parent_depth = 0
    last = 0

    char_has_not = False
    temp_has_not = False

    # Check if an expression is valid
    if not is_expression_valid(expression):
        raise ValueError("That is an invalid expression.")

    for index in range(len(expression)):
        char = expression[index]

        # Check for open parenthesis
        if char == "(":
            if parent_depth == 0:
                last = index + 1
            parent_depth += 1
        
        # Check for close parenthesis
        elif char == ")":
            parent_depth -= 1

            # Parse expression if parenthesis depth reaches 0
            if parent_depth == 0:

                # Check if there is a ~ (NOT) operator directly in front of the parenthesis
                if last - 1 > 0:
                    if expression[last - 2] == "~":
                        temp_has_not = True
                
                exp = parse_expression(expression[last: index], temp_has_not, operator_type)
                if index == len(expression) - 1 and last == 0:
                    has_not = temp_has_not
                temp_has_not = False

                # Check if there is no operator; Must be left side
                if operator == None:
                    left = exp["expression"]
                else:
                    right = exp["expression"]
        
        # No parenthesis depth anymore
        if parent_depth == 0:
            
            # Check for operator only if not within a parenthesis
            if char in ["^", "v", ">", "-", "|", "⬇"]:

                # Check if operator does not exist yet
                if operator == None:
                    if char == "^":
                        operator = LogicNode.AND
                    elif char == "v":
                        operator = LogicNode.OR
                    elif char == ">":
                        operator = LogicNode.IMPLIES
                    elif char == "-":
                        operator = LogicNode.BICONDITIONAL
                    elif char == "|":
                        operator = LogicNode.NAND
                    elif char == "⬇":
                        operator = LogicNode.NOR
                
                # Operator exists; String of logical expressions exists
                # Make the left, operator, right into the left expression
                else:
                    left = {
                        "has_not": has_not,
                        "left": left,
                        "operator": operator,
                        "operator_type": operator_type,
                        "right": right
                    }

                    if char == "^":
                        operator = LogicNode.AND
                    elif char == "v":
                        operator = LogicNode.OR
                    elif char == ">":
                        operator = LogicNode.IMPLIES
                    elif char == "-":
                        operator = LogicNode.BICONDITIONAL
                    elif char == "|":
                        operator = LogicNode.NAND
                    elif char == "⬇":
                        operator = LogicNode.NOR

                    right = None
                    has_not = False

        # Check if the value is an integer; We can't have those
        if char.isdigit():
            raise ValueError("You cannot use a number as a logical variable.")
        
        # Check for variable only if not within parentheses
        if ord(char) in range(ord('a'), ord('z') + 1) and ord(char) != ord('v'):

            # See if there is a ~ (NOT) operator directly in front of the variable
            if index > 0:
                if expression[index - 1] == "~":
                    char_has_not = True
                else:
                    char_has_not = False
            
            # Check if there is no operator; Must be left side
            if operator == None:
                left = {
                    "has_not": char_has_not,
                    "value": char
                }
            else:
                right = {
                    "has_not": char_has_not,
                    "value": char
                }
            
            char_has_not = False
            
            if char not in variables:
                variables.append(char)
    
    if parent_depth != 0:
        raise UnbalancedParentheses("You have a missing parenthesis somewhere.")
    
    variables.sort()

    # Check if the expression is a single expression wrapped in parentheses
    if operator == right == None:
        has_not = left["has_not"]
        operator = left["operator"]
        operator_type = left["operator_type"]
        right = left["right"]
        left = left["left"]
    
    return {
        "expression": {
            "has_not": has_not,
            "left": left,
            "operator": operator,
            "right": right,
            "operator_type": operator_type
        },
        "variables": variables
    }


def logicAPI(expression, compare = None, as_table = False):
    
    try:

        if expression == None:
            result = {"success": False, "error": "You need an expression to parse."}
            code = 400
        
        else:
            exp_tree = LogicTree(expression)

            if as_table:
                result = {"success": True, "value": exp_tree.make_table()}
                code = 200
            
            else:
                result = {"success": True, "value": exp_tree.get_truth_values()}
                code = 200

    except UnbalancedParentheses as up:
        result = {"success": False, "error": str(up)}
        code = 400
    except MissingTruthValue as mtv:
        result = {"success": False, "error": str(mtv)}
        code = 400
    except ValueError as ve:
        result = {"success": False, "error": str(ve)}
        code = 400
    except Exception as e:

        exc = "".join(traceback.format_exception(type(e), e, e.__traceback__))

        requests.post(
            "https://maker.ifttt.com/trigger/on_error/with/key/{}".format(os.environ["IFTTT_WEBHOOK_KEY"]),
            json = {
                "value1": "logicAPI",
                "value2": exc,
                "value3": "\n" + expression
            }
        )
        result = {"success": False, "error": "An unknown error has occurred and has been sent to the developer."}
        code = 400

    return jsonify(result), code