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
        | left:compare_item op:compare_op right:compare_item
        ;
    
    assignment_left 
        = 
        identifier 
        ;
    
    assignment_right 
        = 
        | expr
        | identifier 
        | number
        ;
    
    compare_item 
        = 
        | expr
        | identifier 
        | number
        ;
    
    compare_op
        =
        | '>'
        | '<'
        | '='
        ;

    number = /[0-9][a-fA-F0-9]*/ ;
    identifier = /[a-zA-Z][a-zA-Z0-9]*/ ;
'''


def get_prog_text() -> str:
    with open('prog') as f:
        return f.read()


if __name__ == '__main__':
    import json
    from tatsu import parse
    from tatsu.util import asjson

    ast = parse(GRAMMAR, get_prog_text())
    print(json.dumps(asjson(ast), indent=2))