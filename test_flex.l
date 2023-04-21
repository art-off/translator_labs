%option noyywrap yylineno

%{
    #include <stdio.h>
    int ch;

    void send_type(char* type_name) {
        printf("%s (%d, %d): %s\n", type_name, yylineno, ch, yytext);
        ch += yyleng;
    }
%}

letter[a-zA-Z]
hex_letter[a-fA-F]
digit[0-9]

%%
("for"|"do"|"end") {
    send_type("KEYWORD");
}

":=" {
    send_type("ASSIGNMEN");
}

[<>=+\-*/] {
    send_type("OPERATOR");
}

{letter}({letter}|{digit})* {
    send_type("IDENTIFIER");
}

{digit}({hex_letter}|{digit})* {
    send_type("NUMBER");
}

"(" {
    send_type("L_PAREN");
}

")" {
    send_type("R_PAREN");
}

";" {
    send_type("SEMICOLON");
}

[ \t\n] {
    ch += yyleng;
}

. {
    send_type("__UNKNOWN");
}
%%

int main(int argc, char **argv) {
    /* 
    Входной язык содержит операторы цикла for (...; ...; ...) do ..., 
    разделённые символом ; (точка с запятой). 
    Операторы цикла содержат идентификаторы, знаки сравнения <, >, =, шестнадцатеричные числа, знак присваивания (:=). 
    Шестнадцатеричными числами считать последовательность цифр и символов a, b, c, d, e, f, 
    начинающуюся с цифры (например, 89, 45ac, 0abc). 
    */
    if (argc < 2) {
        printf("\nNot enough arguments. Please specify filename.\n");
        return -1;
    }
    if ((yyin = fopen(argv[1], "r")) == NULL) {
        printf("\nCannot open file %s.\n", argv[1]);
        return -1; 
    }
    ch = 1;
    yylineno = 1;
    yylex();
    fclose(yyin);
    return 0;
}