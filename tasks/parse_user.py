from typing import List


def parse_user(line: str) -> List[int]:
    items = line.split(' ')
    for i in items:
        if i.startswith('User'):
            n = i[4:]
            print(int(n))


parse_user('User103                  User104                  User105')
