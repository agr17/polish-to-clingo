# polishToClingo

Programa en Python para pasar expresiones lógicas en [notación polaca](https://en.wikipedia.org/wiki/Polish_notation) a un fichero para ser procesado por la herramienta [Clingo](https://potassco.org/clingo/).

Enunciado de la práctica: https://www.dc.fi.udc.es/~cabalar/kr/current/ex1.html

## Uso 

`python polishToClingo.py <input_file>`

## Salida

Devolverá el resultado en un fichero con el mismo nombre que el del fichero de entrada con su extensión cambiada por ".lp", de no tener extensión simplemente se le añade. De existir un fichero con el mismo nombre se sobreescribirá.
