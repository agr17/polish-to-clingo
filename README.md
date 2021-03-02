# polishToClingo

Programa en Python para pasar expresiones de lógica en [notación polaca](https://en.wikipedia.org/wiki/Polish_notation) a un fichero para ser procesado por la herramienta [Clingo](https://potassco.org/clingo/).

## Uso en linux

`chmod +c polishToClingo.py <input_file>`

`./polishToClingo.py`

## Salida

Devolverá el resultado en un fichero con el mismo nombre que el del fichero de entrada sin su extensión, si es que tiene. De existir un fichero con el mismo nombre se sobreescribirá.
