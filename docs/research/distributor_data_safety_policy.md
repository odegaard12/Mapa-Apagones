# Política de seguridad para datos públicos de distribuidoras

Versión inicial: v0.10.4.3-distributor-data-safety-policy

## Objetivo

Esta política define qué datos pueden incorporarse al modelo público de pistas de distribuidora de Mapa Apagones y qué datos quedan prohibidos.

El objetivo es poder seguir ampliando información útil para la ciudadanía sin convertir el proyecto en una base de datos sensible, sin pedir CUPS, sin publicar ubicaciones privadas y sin exponer infraestructura crítica.

## Principios

Mapa Apagones solo debe publicar pistas públicas, prudentes y verificables sobre posibles distribuidoras por municipio, zona administrativa o ámbito geográfico amplio.

El dato publicado debe ayudar a orientar a la persona usuaria, pero no debe prometer exactitud absoluta ni sustituir a la comercializadora, distribuidora o canales oficiales.

## Permitido

Se permite publicar:

- Nombre público de la distribuidora.
- Municipio, provincia, comunidad autónoma o zona administrativa amplia.
- Nivel de confianza conservador.
- Indicaciones como `regional_default` o `verified_partial`.
- Fuentes públicas verificables.
- Fecha de revisión.
- Notas prudentes de cobertura parcial o posible convivencia de varias distribuidoras.

## Prohibido

No se debe publicar ni introducir en producción:

- CUPS.
- Cuentas de usuario.
- Correos personales.
- Teléfonos personales.
- Direcciones exactas.
- Viviendas exactas.
- Coordenadas privadas.
- Fotografías.
- Texto libre de usuarios.
- IPs reales.
- Tokens reales.
- Datos de contadores.
- Contratos.
- Facturas.
- Inventario de infraestructura crítica.
- Subestaciones.
- Centros de transformación.
- Líneas, cables, postes, torres o alimentadores concretos.
- Rutas privadas, logs, bases de datos, backups o artefactos locales.

## Niveles de confianza recomendados

### `verified_partial`

Usar cuando hay una fuente pública razonable que confirma presencia o actividad de una distribuidora en una zona, pero no permite afirmar exclusividad.

Texto recomendado en UI:

- Distribuidora probable.
- Varias distribuidoras posibles.
- Confirmar con la comercializadora o distribuidora.

### `regional_default`

Usar cuando una distribuidora principal cubre de forma orientativa una región o zona amplia, pero puede haber excepciones locales.

Texto recomendado en UI:

- Distribuidora orientativa.
- Confirmar con la comercializadora o distribuidora.
- Puede haber distribuidoras locales.

### Sin dato fiable

Cuando no hay fuente pública suficiente, mantener el fallback:

- Consultar distribuidora de la zona.

## Reglas para futuras importaciones

Antes de importar datos nuevos:

1. Revisar fuentes públicas.
2. Evitar exclusividad salvo confirmación clara.
3. Separar excepciones locales.
4. No añadir coordenadas privadas ni direcciones exactas.
5. No añadir CUPS ni datos de suministro.
6. No publicar infraestructura eléctrica concreta.
7. Ejecutar las guardias del repositorio.
8. Usar PRs pequeños por comunidad, provincia o lote verificable.

## Validación automática

El repositorio incluye una guardia específica para revisar el JSON público de distribuidoras y bloquear campos o patrones peligrosos.

La guardia no sustituye la revisión humana, pero reduce el riesgo de publicar datos sensibles por error.
