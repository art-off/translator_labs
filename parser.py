import json
from tatsu import parse
from tatsu.util import asjson

GRAMMAR = '''
    @@grammar :: Laba4
    
    start = statement $ ;
    
    statement = type:'for' '(' init:expr ';' cond:expr ';' next:expr ')' 'do' body:body_expr 'end';
    
    body_expr
        = 
        {expr}*
        ;

    expr
        =
        | left:assignment_left op:':=' right:assignment_right
        | left:binary_op_item op:compare_op right:binary_op_item
        | type:'print' '(' arg:assignment_right ')'
        ;
    
    assignment_left 
        = 
        id:identifier 
        ;
    
    assignment_right 
        = 
        | expr
        | id:identifier 
        | num:number
        ;
    
    binary_op_item 
        = 
        | expr
        | id:identifier 
        | num:number
        ;
    
    compare_op
        =
        | '>'
        | '<'
        | '='
        | '+'
        | '-'
        ;

    number = /[0-9][a-fA-F0-9]*/ ;
    identifier = /[a-zA-Z][a-zA-Z0-9]*/ ;
'''


def get_ast_from_prog_text(prog_text: str) -> dict:
    ast = parse(GRAMMAR, prog_text)
    return asjson(ast)