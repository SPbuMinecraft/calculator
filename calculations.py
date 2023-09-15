import operator
import ast

_OP_MAP = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.__truediv__,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Pow: operator.pow,
}

class Calc(ast.NodeVisitor):
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return _OP_MAP[type(node.op)](left, right)
    def visit_UnaryOp(self, node):
        tmp = self.visit(node.operand)
        return _OP_MAP[type(node.op)](tmp)
    def visit_Constant(self, node):
        return node.n
    def visit_Expr(self, node):
        return self.visit(node.value)
    @classmethod
    def evaluate(cls, expression):
        tree = ast.parse(expression)
        calc = cls()
        return calc.visit(tree.body[0])

def formula_parsing(formula: str) -> (bool, float):
    try:
        return True, Calc.evaluate(formula)
    except Exception:
        pass
    return False, -1