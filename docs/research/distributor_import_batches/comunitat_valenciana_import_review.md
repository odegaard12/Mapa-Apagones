# Comunitat Valenciana — importación prudente de pistas de distribuidora

Fecha de revisión: 2026-05-10
Estado: importación a producción con excepciones cooperativas conocidas

## Resumen

Se importan pistas públicas de distribuidora para los 544 municipios del dataset geográfico `comunitat_valenciana`.

Criterio:

- `regional_default` para i-DE Redes Eléctricas Inteligentes, S.A.U. en municipios sin excepción local identificada.
- `verified_partial` para cooperativas/distribuidoras locales con fuente pública específica.
- No se afirma exclusividad.
- Se mantiene aviso de confirmación con comercializadora o distribuidora.

## Fuentes públicas usadas

### i-DE

Fuente:
- i-DE — mapa oficial de distribuidoras por zona geográfica
- URL: https://www.i-de.es/conexion-red-electrica/mapa-de-distribuidoras

Lectura prudente:
- Herramienta oficial para comprobar distribuidora por dirección o municipio.
- Se usa como apoyo para pista orientativa, no para afirmar exclusividad.
- Se aplica como `regional_default` donde no hay excepción local identificada.

### Federación Cooperativas Eléctricas CV

Fuente:
- Federación Cooperativas Eléctricas — cooperativas socias
- URL: https://www.coopelectricas.com/cooperativas-socias/

Lectura prudente:
- La web indica que las cooperativas socias desarrollan generación y distribuyen a través de sociedades participadas.
- Se usa para marcar excepciones locales como `verified_partial`.
- No se publican direcciones exactas, teléfonos ni correos.

### IDAE / Grupo Enercoop

Fuente:
- IDAE — Grupo Enercoop / cooperativas distribuidoras eléctricas CV
- URL: https://www.idae.es/sites/default/files/imagenes/idae/ofrecemos/jornadas_y_ferias/comptem_enercoop_crevillent_-_idae_comunidades_energeticas_27.11.2020.pdf

Lectura prudente:
- Se usa como apoyo documental para cooperativas distribuidoras valencianas.
- Se usa para Crevillent, Callosa de Segura, Albatera y Biar.
- No se importan datos de suministro, CUPS ni infraestructura.

## Excepciones locales importadas como `verified_partial`

- Crevillent — Cooperativa Eléctrica Benéfica San Francisco de Asís de Crevillent.
- Callosa de Segura — Eléctrica de Callosa de Segura, Sdad. Coop. Valenciana.
- Albatera — Eléctrica Benéfica Albaterense, Coop. V.
- Biar — Eléctrica Nuestra Señora de Gracia, Sdad. Coop. Valenciana.
- Meliana — Eléctrica de Meliana, Coop. V.
- Sot de Chera — Eléctrica de Sot de Chera, Coop. V.
- Catral — Eléctrica Benéfica Catralense, Coop. V.
- Vinalesa — Eléctrica de Vinalesa, Coop. V.
- Guadassuar — Eléctrica de Guadassuar, Coop. V.
- Alginet — Suministros Especiales Alginetenses, Coop. V.
- Chera — Eléctrica de Chera, Coop. V.

## Resultado esperado

- Comunitat Valenciana pasa de 0 / 544 a 544 / 544 zonas con pista pública.
- Total de pistas públicas pasa de 1.415 a 1.959.
- Pendientes pasan de 6.800 a 6.256.
- La cobertura total aproximada pasa de 17,2% a 23,8%.

## Limitaciones

Esta importación no afirma exclusividad. Puede haber otras distribuidoras locales no separadas todavía. La pista regional se mantiene como orientación y debe confirmarse siempre con comercializadora o distribuidora.

## Seguridad y privacidad

Esta revisión no contiene CUPS, cuentas, texto libre de usuarios, fotos, direcciones exactas, coordenadas privadas, IPs reales, tokens reales, contratos, facturas ni inventario de infraestructura crítica.
