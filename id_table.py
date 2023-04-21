import os
import re

from typing import Optional, Dict
from operator import attrgetter

from prettytable import PrettyTable


class Token:
    def __init__(self, type: str, position: (int, int), value: str):
        self.type = type
        self.position = position
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.position == other.position and self.value == other.value


class IDToken:
    def __init__(self, token: Token, scope: int):
        self.token = token
        self.scope = scope

    def __eq__(self, other):
        if not isinstance(other, IDToken):
            return False
        return self.token == other.token and self.scope == other.scope

    def __str__(self):
        return f'({self.scope}) -- {self.token.value} number'


class IDTokenNode:
    def __init__(self, id_token: IDToken, next_id_token: Optional[IDToken]):
        self.id_token = id_token
        self.next_id_token = next_id_token

    def __repr__(self):
        return f'{self.id_token}'


def _get_token_lines() -> list[str]:
    try:
        os.remove("tokens.txt")
    except:
        pass
    os.system("./a.out prog >> tokens.txt")
    with open('tokens.txt') as file:
        tokens = file.readlines()
    # Удаляем '\n'
    tokens = [token[:-1] for token in tokens]
    return tokens


def parse_token(s) -> Optional[Token]:
    match = re.match(r'(.*) \((.*), (.*)\): (.*)', s)

    if match is None:
        return None

    type = match.group(1)
    position = (int(match.group(2)), int(match.group(3)))
    value = match.group(4)
    return Token(type, position, value)


def get_tokens() -> list[Token]:
    return [parse_token(line) for line in _get_token_lines()]


class IDTable:
    def __init__(self):
        self.scope_level = 0
        self.table: Dict[str, IDTokenNode] = dict()

    def insert_token(self, token: Token):
        assert token.type == 'IDENTIFIER'
        self._insert_token_recursively(token)

    def lookup_token(self, token: Token) -> Optional[IDToken]:
        assert token.type == 'IDENTIFIER'
        return self._lookup_recursively(token)

    def increment_scope(self):
        self.scope_level += 1

    def decrement_scope(self):
        self.scope_level -= 1

    def _insert_token_recursively(self, token: Token):
        new_node = self._make_node(token)

        if self.table.get(token.value) is None:
            self.table[token.value] = new_node
            return

        current_node = self.table[token.value]

        while True:
            if current_node.id_token == new_node.id_token:
                return
            if current_node.next_id_token is None:
                break
            current_node = current_node.next_id_token

        current_node.next_id_token = new_node

    def _lookup_recursively(self, token: Token) -> Optional[IDToken]:
        current_node = self.table.get(token.value)

        if current_node is None:
            return None

        equal_identifiers_tokens: list[IDToken] = []

        while True:
            equal_identifiers_tokens.append(current_node.id_token)
            if current_node.next_id_token is None:
                break
            current_node = current_node.next_id_token

        sorted_identifiers_tokens = sorted(equal_identifiers_tokens, key=attrgetter('scope'), reverse=True)
        right_scope_tokens = list(filter(lambda x: x.scope >= self.scope_level, sorted_identifiers_tokens))

        if not len(right_scope_tokens):
            return None
        return right_scope_tokens[0]

    def _make_node(self, token):
        return IDTokenNode(
            IDToken(token, self.scope_level),
            None
        )


id_table = IDTable()


def fill_id_table(tokens: list[Token]):
    for index, token in enumerate(tokens):
        if token.type == 'KEYWORD' and token.value == 'do':
            id_table.increment_scope()
        elif token.type == 'KEYWORD' and token.value == 'do':
            id_table.decrement_scope()
        elif token.type == 'IDENTIFIER':
            if index+1 < len(tokens) and tokens[index+1].type == 'ASSIGNMEN':
                id_table.insert_token(token)
            else:
                token = id_table.lookup_token(token)


def main():
    tokens = get_tokens()
    fill_id_table(tokens)

    my_table = PrettyTable()
    my_table.field_names = ["Scope", "Name", "Type"]

    for token in id_table.table.values():
        my_table.add_row([token.id_token.scope, token.id_token.token.value, 'number'])

    print(my_table)

main()
