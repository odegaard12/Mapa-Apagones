# Aragón wave 2 candidate gate v0.10.8.3

## Resultado

- Municipios revisados: **734**
- Contexto regional únicamente: **733**
- Candidatos secundarios fuertes: **1**
- Candidatos con fuente primaria municipal exacta: **0**
- Municipios elegibles para importar: **0**
- Hints productivos importados por esta fase: **0**

## Barbastro

Barbastro queda clasificado como `strong_secondary_candidate`.

Hay varias referencias municipales explícitas, pero pertenecen a una única
familia editorial y todavía no confirman de forma primaria la entidad jurídica
de la distribuidora. Por ello continúa con `import_eligible=no`.

## Puerta de importación

Una futura fila solo puede pasar a `import_eligible=yes` cuando cumpla todo:

1. fuente primaria oficial;
2. municipio mencionado de forma exacta;
3. entidad jurídica confirmada;
4. decisión de revisión aprobada;
5. ninguna inferencia basada únicamente en cobertura regional.

## Corrección de wave 1

Los 734 `repository-local reference hits` son referencias cruzadas de
inventario, no 734 pruebas de distribuidora.

## Privacidad y seguridad

No se incluyen CUPS, direcciones, coordenadas exactas, geometría de red,
respuestas raw, contratos ni datos de clientes.
