# Decisión técnica saneada · La Rioja · i-DE

Fecha: 2026-05-13.

## Resultado

No se debe importar La Rioja 175/175 como `verified_partial` a partir del mapa público de i-DE.

## Motivo

La inspección local del JS/HTML público muestra que el mapa de i-DE funciona como buscador interactivo por ubicación/punto, no como fuente municipal masiva.

Flujo observado de forma saneada:

1. La página inicializa variables de mapa y geocodificación.
2. Obtiene una ubicación mediante geocoder o localización.
3. Construye una consulta con `latLng`.
4. Ejecuta una acción protegida por reCAPTCHA.
5. Hace POST a un recurso de portlet/Liferay.
6. Recibe `service_response`.
7. Muestra el mensaje de distribuidora devuelto para ese punto.

Esto puede servir para consulta individual orientativa, pero no prueba cobertura municipal completa ni exclusividad de red.

## Decisión de datos

- No subir La Rioja a `verified_partial`.
- Mantener La Rioja como orientación regional mientras no exista fuente reproducible municipio/zona.
- No guardar coordenadas.
- No guardar direcciones.
- No guardar capturas.
- No guardar respuestas raw.
- No guardar tokens, claves públicas de terceros ni HTML/JS raw.
- No automatizar consultas protegidas por reCAPTCHA.

## Próximo PR recomendado

Abrir PR de UX/fiabilidad para diferenciar claramente:

- `verified_partial`: pista municipal/parcial con fuente fuerte.
- `regional_default`: orientación regional, no verificación municipal fuerte.

## Conclusión

La Rioja sigue siendo buena candidata para mejorar, pero necesita otra fuente: listado municipal oficial, capa pública descargable o documentación pública por municipio/zona. El mapa i-DE actual no basta para importar 175 municipios como verificados.
