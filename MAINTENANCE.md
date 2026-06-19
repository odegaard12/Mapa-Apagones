# Política de mantenimiento

Este documento describe cómo se mantiene Mapa Apagones y qué condiciones debe
cumplir un cambio antes de llegar a `main`.

## Principios

- Privacidad y seguridad antes que velocidad.
- Datos públicos reproducibles antes que inferencias.
- Pull requests con valor funcional o técnico suficiente.
- No abrir PRs mínimos salvo correcciones urgentes o de seguridad.
- Cambios relacionados deben agruparse en un lote coherente.
- `main` debe permanecer desplegable.

## Pull requests

Un PR debe incluir, según corresponda:

- objetivo y alcance;
- archivos y comportamiento modificados;
- riesgos;
- validaciones ejecutadas;
- impacto sobre privacidad y datos;
- confirmación de que no contiene secretos;
- plan de reversión cuando exista riesgo operativo.

Las investigaciones que todavía no producen datos verificables pueden
agruparse en una cola o workbench. No deben generar una sucesión de PRs sin
impacto real.

## Dependencias

La política actual es conservadora:

- backend: actualizaciones automáticas de parche;
- cambios mayores o incompatibles: revisión manual;
- frontend: actualizaciones seguras agrupadas;
- GitHub Actions: cambios mayores revisados manualmente;
- ninguna actualización se fusiona solo porque Dependabot la proponga;
- instalación limpia, smokes, guards y build deben pasar antes del merge.

Las PRs automáticas obsoletas, duplicadas o incompatibles se cierran.

## Datos de distribuidoras

Una pista productiva requiere evidencia pública suficientemente fuerte.

No se permite:

- inferir municipios desde presencia regional;
- convertir noticias repetidas en varias fuentes independientes;
- importar automáticamente resultados del watcher privado;
- afirmar exclusividad de una distribuidora sin evidencia;
- publicar infraestructura crítica, CUPS, direcciones o coordenadas privadas.

El watcher privado solo genera candidatos pendientes de revisión humana.

## Automatización mínima

Antes de fusionar cambios relevantes deben pasar:

- CI;
- secret-scan;
- guards del repositorio;
- comprobaciones de cobertura geográfica;
- validadores de distribuidoras;
- build del frontend;
- smokes aplicables.

Después del merge se comprueba el despliegue público cuando el cambio afecta
a Cloudflare Pages o a la API.

## Cadencia

- Revisión de dependencias: al menos semanal.
- Revisión de candidatos de datos: por lotes, cuando exista evidencia útil.
- Validación general del repositorio: después de merges relevantes.
- Revisión de documentación pública: con cada cambio visible de producto.
- Revisión de esta política y de SECURITY.md: al menos trimestral.

## Versionado

La versión visible se actualiza cuando cambia el producto, la interfaz pública
o el dataset publicado. Los cambios internos de documentación o gobernanza no
requieren por sí solos una nueva versión de producto.

## Incidencias de seguridad

Las vulnerabilidades se comunican siguiendo `SECURITY.md`. No deben abrirse
issues públicas con detalles explotables, secretos o datos personales.
