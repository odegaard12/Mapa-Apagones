# Estado de mantenimiento y respuesta a auditoría

Fecha de revisión: **2026-06-19**

## Estado observado antes de este cambio

- `main`: `f442d3e`
- PR abiertas detectadas: **0**
- CI y secret-scan configurados.
- Dependabot usa una política de bajo ruido.
- Existe cobertura geográfica nacional de 8.215 municipios.
- El watcher privado nacional revisa candidatos sin importar datos ni crear PRs.

## Corrección de la auditoría externa

La auditoría recibida describía siete PRs de dependencias abiertas y falta de
integración reciente. Ese diagnóstico correspondía a una captura anterior.

Desde entonces se completaron, entre otros:

- política Dependabot con menos ruido;
- actualización controlada de dependencias;
- cola nacional de investigación;
- Aragón wave 1;
- Aragón wave 2;
- cierre de las PRs automáticas obsoletas.

La recomendación de añadir una política formal de seguridad y hacer visible el
estado de CI seguía siendo válida.

## Mejoras incluidas en este lote

- `SECURITY.md`;
- `MAINTENANCE.md`;
- badges visibles de CI y secret-scan;
- página pública `/seguridad/`;
- canal privado para vulnerabilidades;
- instrucciones de seguridad en `CONTRIBUTING.md`;
- enlace desde la aplicación y el sitemap;
- guard automático de gobernanza;
- integración en la validación post-merge.

## Próximas mejoras agrupables

Estas mejoras deben abordarse en lotes sustanciales, no en PRs mínimos:

1. página pública de salud y frescura de datasets;
2. auditoría de accesibilidad móvil;
3. revisión periódica de candidatos del watcher privado;
4. publicación de lotes de distribuidoras solo con evidencia primaria;
5. revisión trimestral de seguridad y mantenimiento.

## Regla de entrega

No se abrirá un PR por cada documento, candidato o ajuste menor. Los cambios
se agruparán cuando formen una mejora coherente, salvo una incidencia urgente
de seguridad o disponibilidad.
