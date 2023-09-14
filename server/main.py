import sys
import ast
import requests
import operator

from flask import Flask, jsonify, abort, request
from urllib.parse import urlparse

_OP_MAP = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.__truediv__,
    ast.Invert: operator.neg,
}
class Calc(ast.NodeVisitor):
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return _OP_MAP[type(node.op)](left, right)
    def visit_Num(self, node):
        return node.n
    def visit_Expr(self, node):
        return self.visit(node.value)
    @classmethod
    def evaluate(cls, expression):
        tree = ast.parse(expression)
        calc = cls()
        return calc.visit(tree.body[0])

app = Flask(__name__)

def formula_parsing(formula: str) -> (bool, float):
    try:
        return True, Calc.evaluate(formula)
    except Exception:
        pass
    return False, -1

@app.route('/calculations', methods=['GET'])
def get_tasks():
    return requests.get('http://localhost:6000//calculations/db').json(), 201


@app.route('/calculate', methods=['POST'])
def create_task():
    if not request.json or not 'formula' in request.json:
        abort(400)
    
    exist, answer = formula_parsing(request.json['formula'])
    if exist:
        calculation = {
            'formula': request.json['formula'],
            'answer' : str(answer)
        }
        res = requests.post('http://localhost:6000//add', json=calculation)
        return answer, res.status_code
    else:
        return -1, 404

if __name__ == '__main__':
    app.run(debug=True)
