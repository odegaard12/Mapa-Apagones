# Madrid — revisión previa antes de importar pistas de distribuidora

Fecha de revisión: 2026-05-10
Estado: investigación previa, no importación masiva

## Conclusión prudente

No se debe importar toda la Comunidad de Madrid con una única distribuidora por defecto.

La Comunidad de Madrid tiene 181 municipios en el dataset geográfico del repositorio, pero las fuentes públicas revisadas indican presencia de más de una distribuidora o herramientas oficiales que requieren consulta por zona/dirección/municipio.

## Fuentes públicas revisadas

### UFD / Naturgy

Naturgy indica públicamente que UFD da servicio a más de 1,2 millones de puntos de suministro en 47 municipios de la Comunidad de Madrid.

Fuente:
- Naturgy — “UFD refuerza la calidad del suministro eléctrico en el Sur de la Comunidad de Madrid”
- URL: https://www.naturgy.com/notas-de-prensa/ufd-refuerza-la-calidad-del-suministro-electrico-en-el-sur-de-la-comunidad-de-madrid/

Lectura prudente:
- UFD tiene presencia pública confirmada en la Comunidad de Madrid.
- La fuente habla de 47 municipios, no de los 181.
- No permite importar Madrid completo como UFD.

### i-DE

i-DE ofrece un mapa interactivo para localizar dirección o municipio y comprobar qué distribuidora opera en una zona.

Fuente:
- i-DE — Mapa de Distribuidora
- URL: https://www.i-de.es/conexion-red-electrica/mapa-de-distribuidoras

Lectura prudente:
- i-DE tiene herramienta pública de comprobación de zona.
- La herramienta confirma la necesidad de revisar por municipio/zona.
- No permite convertir toda Madrid en un único `regional_default`.

### UFD — mapa / CUPS

UFD indica que se puede comprobar si un suministro está en su zona con su mapa, o por prefijo CUPS.

Fuente:
- UFD — Dónde estamos
- URL: https://www.ufd.es/quienes-somos/donde-estamos/

Lectura prudente:
- No se debe pedir ni guardar CUPS.
- El mapa puede servir para revisión manual, pero no para publicar datos sin validación municipal.
- No se debe importar información de dirección exacta ni coordenadas privadas.

## Decisión para producción

- No importar Madrid entero todavía.
- Crear un lote posterior solo con municipios confirmados por fuente pública clara.
- Usar `verified_partial` para presencia confirmada sin exclusividad.
- Usar `regional_default` solo si una fuente pública suficiente permite afirmar orientación regional prudente.
- Mantener fallback genérico donde no haya certeza.

## Seguridad y privacidad

Esta revisión no contiene CUPS, cuentas, texto libre de usuarios, fotos, direcciones exactas, coordenadas privadas, IPs reales, tokens reales, contratos, facturas ni inventario de infraestructura crítica.
