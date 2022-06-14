# Polish-to-Clingo

Programa en Python para pasar expresiones lógicas en [notación polaca](https://en.wikipedia.org/wiki/Polish_notation) a un fichero para ser procesado por la herramienta [Clingo](https://potassco.org/clingo/). Para ello, se realizará una reducción a [Forma Normal Conjuntiva](https://es.wikipedia.org/wiki/Forma_normal_conjuntiva), como se explica en el enunciado.

[Enunciado de la práctica](https://www.dc.fi.udc.es/~cabalar/kr/2021/ex1.html)

## Uso 

`python polishToClingo.py <input_file>`

## Salida

Devolverá el resultado en un fichero con el mismo nombre que el del fichero de entrada con su extensión cambiada por ".lp", de no tener extensión simplemente se le añade. De existir un fichero con el mismo nombre se sobreescribirá.
