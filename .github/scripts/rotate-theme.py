"""Select another profile theme and update the three artwork URLs together."""
import os
from pathlib import Path
import re
import secrets

THEMES = ('cosmos', 'rosa', 'alvorada')
ART = re.compile(
    r'collection/(?P<theme>cosmos|rosa|alvorada)/atuais/'
    r'steam-(?P=theme)(?P<part>-portfolio|-logic)?\.svg'
)


def rotate(text, choose=secrets.choice):
    images = list(ART.finditer(text))
    if len(images) != 3 or {m['part'] for m in images} != {None, '-portfolio', '-logic'}:
        raise ValueError('Expected exactly one hero and two showcase images')
    current = {m['theme'] for m in images}
    if len(current) != 1:
        raise ValueError('The three images must belong to the same theme')
    previous = current.pop()
    selected = choose([theme for theme in THEMES if theme != previous])
    if selected not in THEMES or selected == previous:
        raise ValueError('The selected theme must differ from the current one')
    updated = ART.sub(
        lambda m: f'collection/{selected}/atuais/steam-{selected}{m["part"] or ""}.svg',
        text,
    )
    updated = updated.replace(f'alt="toybile — {previous.capitalize()}"',
                              f'alt="toybile — {selected.capitalize()}"')
    return updated, previous, selected


if __name__ == '__main__':
    readme = Path('README.md')
    updated, previous, selected = rotate(readme.read_text(encoding='utf-8'))
    readme.write_text(updated, encoding='utf-8')
    print(f'{previous} -> {selected}')
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as output:
            output.write(f'theme={selected}\n')
