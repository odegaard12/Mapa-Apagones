# Euskadi — importación prudente de pistas de distribuidora

Fecha de revisión: 2026-05-10  
Estado: importación a producción con excepciones locales conocidas

## Resumen

Se importan pistas públicas de distribuidora para los 255 municipios del dataset geográfico `euskadi`.

Criterio:

- `regional_default` para i-DE Redes Eléctricas Inteligentes, S.A.U. en municipios sin excepción local identificada.
- `verified_partial` para excepciones locales con fuente pública específica.
- No se afirma exclusividad.
- Se mantiene aviso de confirmación con comercializadora o distribuidora.

## Fuentes públicas usadas

### i-DE / Iberdrola España

Fuente:
- Iberdrola España — i-DE en el País Vasco
- URL: https://www.iberdrolaespana.com/sala-comunicacion/noticias/modernizacion-redes-electricas-electrificacion-pais-vasco

Lectura prudente:
- Fuente pública suficiente para pista regional orientativa.
- No se usa para afirmar exclusividad municipal.
- Se aplica como `regional_default`, no como verificación local.

### Tolosa — Tolargi

Fuente:
- Tolargi — zona de distribución en el municipio de Tolosa
- URL: https://www.tolargi.eus/?lang=es

Lectura prudente:
- Fuente pública específica para Tolosa.
- Se importa como `verified_partial`.

### Oñati / Oñate — Oñargi

Fuente:
- CNMC INS/DE/031/25 — Oñargi, S.L.
- URL: https://www.cnmc.es/sites/default/files/5909946.pdf

Lectura prudente:
- Fuente regulatoria pública específica para Oñati/Oñate.
- Se importa como `verified_partial`.

### Aramaio — Aramaioko Argindar Banatzailea

Fuente:
- CNMC — censo/listado público de distribuidoras eléctricas
- URL: https://sede.cnmc.gob.es/listado/censo/1

Lectura prudente:
- Fuente pública regulatoria.
- Se importa como `verified_partial`.

## Resultado esperado

- Euskadi pasa de 0 / 255 a 255 / 255 zonas con pista pública.
- Total de pistas públicas pasa de 1.160 a 1.415.
- Pendientes pasan de 7.055 a 6.800.
- La cobertura total aproximada pasa de 14,1% a 17,2%.

## Seguridad y privacidad

Esta revisión no contiene CUPS, cuentas, texto libre de usuarios, fotos, direcciones exactas, coordenadas privadas, IPs reales, tokens reales, contratos, facturas ni inventario de infraestructura crítica.
