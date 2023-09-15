import ast
import operator

node2op = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.__truediv__,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Pow: operator.pow,
}


class Interpreter(ast.NodeVisitor):
    def visit_BinOp(self, node: ast.BinOp):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return node2op[type(node.op)](left, right)

    def visit_UnaryOp(self, node: ast.UnaryOp):
        return node2op[type(node.op)](self.visit(node.operand))

    def visit_Constant(self, node: ast.Constant):
        return node.n

    def visit_Expr(self, node: ast.Expr):
        return self.visit(node.value)

    @classmethod
    def evaluate(cls, expression: str):
        tree = ast.parse(expression)
        calc = cls()
        return calc.visit(tree.body[0])


def safe_eval(expression: str) -> (bool, float):
    try:
        return True, Interpreter.evaluate(expression)
    except Exception:
        return False, -1
