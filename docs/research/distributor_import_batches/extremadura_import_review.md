# Revisión previa de distribuidoras: Extremadura

Fecha de revisión: 2026-05-11

## Resumen

- Dataset revisado: `extremadura`.
- Municipios/zonas en GeoJSON público: **388**.
- Producción actual antes de esta revisión: Extremadura sigue pendiente de pistas públicas de distribuidora.
- Recomendación actual: **no importar Extremadura completa como una única distribuidora todavía**.

## Motivo

Hay evidencia pública suficiente de presencia relevante de i-DE en Extremadura, pero también hay fuentes públicas de la Junta de Extremadura que muestran varias empresas distribuidoras en la comunidad.

Por tanto, importar los 388 municipios como `regional_default` de una sola empresa sería demasiado agresivo para el criterio actual del proyecto.

## Fuentes públicas de alto nivel

- i-DE / Iberdrola España: comunicación pública sobre presencia e inversiones de i-DE en Extremadura.
  - https://www.iberdrolaespana.com/sala-comunicacion/noticias/i-de-redes-electricas-coordinacion-junta-extremadura
- Junta de Extremadura: herramienta pública de mapa de empresas de distribución de energía eléctrica.
  - https://asistenteagile.juntaex.es/AsistenteAGILE/AsistenteMapViewDistribuidoras.xhtml
- CNMC: censo/listado público general de distribuidoras de electricidad.
  - https://sede.cnmc.gob.es/listado/censo/1

## Criterio de seguridad

No se deben copiar CUPS, direcciones exactas, coordenadas privadas, datos de suministro, contratos, contadores, facturas ni inventario de infraestructura crítica.

Si una fuente oficial contiene CUPS o direcciones, solo debe usarse para confirmar que existen varias distribuidoras a nivel general, sin trasladar esos campos al repositorio.

## Decisión operativa

- No importar datos productivos en este PR.
- Preparar Extremadura como lote de revisión, no como lote cerrado.
- Siguiente paso recomendado: separar municipios con distribuidora local identificable mediante fuentes públicas no sensibles.
- Solo usar `regional_default` cuando la evidencia sea suficientemente clara y la UI mantenga el texto de pista orientativa.
- Usar `verified_partial` cuando haya presencia pública razonablemente verificada de una distribuidora local, sin afirmar exclusividad.

## Municipios pendientes de clasificación

| Municipio | Provincia | zone_id | Estado recomendado |
|---|---|---|---|
| Acedera | Badajoz | `municipality:badajoz::acedera` | pendiente de revisión municipal |
| Aceuchal | Badajoz | `municipality:badajoz::aceuchal` | pendiente de revisión municipal |
| Ahillones | Badajoz | `municipality:badajoz::ahillones` | pendiente de revisión municipal |
| Alange | Badajoz | `municipality:badajoz::alange` | pendiente de revisión municipal |
| Alburquerque | Badajoz | `municipality:badajoz::alburquerque` | pendiente de revisión municipal |
| Alconchel | Badajoz | `municipality:badajoz::alconchel` | pendiente de revisión municipal |
| Alconera | Badajoz | `municipality:badajoz::alconera` | pendiente de revisión municipal |
| Aljucén | Badajoz | `municipality:badajoz::aljucen` | pendiente de revisión municipal |
| Almendral | Badajoz | `municipality:badajoz::almendral` | pendiente de revisión municipal |
| Almendralejo | Badajoz | `municipality:badajoz::almendralejo` | pendiente de revisión municipal |
| Arroyo de San Serván | Badajoz | `municipality:badajoz::arroyo_de_san_servan` | pendiente de revisión municipal |
| Atalaya | Badajoz | `municipality:badajoz::atalaya` | pendiente de revisión municipal |
| Azuaga | Badajoz | `municipality:badajoz::azuaga` | pendiente de revisión municipal |
| Badajoz | Badajoz | `municipality:badajoz::badajoz` | pendiente de revisión municipal |
| Barcarrota | Badajoz | `municipality:badajoz::barcarrota` | pendiente de revisión municipal |
| Baterno | Badajoz | `municipality:badajoz::baterno` | pendiente de revisión municipal |
| Benquerencia de la Serena | Badajoz | `municipality:badajoz::benquerencia_de_la_serena` | pendiente de revisión municipal |
| Berlanga | Badajoz | `municipality:badajoz::berlanga` | pendiente de revisión municipal |
| Bienvenida | Badajoz | `municipality:badajoz::bienvenida` | pendiente de revisión municipal |
| Bodonal de la Sierra | Badajoz | `municipality:badajoz::bodonal_de_la_sierra` | pendiente de revisión municipal |
| Burguillos del Cerro | Badajoz | `municipality:badajoz::burguillos_del_cerro` | pendiente de revisión municipal |
| Cabeza del Buey | Badajoz | `municipality:badajoz::cabeza_del_buey` | pendiente de revisión municipal |
| Cabeza la Vaca | Badajoz | `municipality:badajoz::cabeza_la_vaca` | pendiente de revisión municipal |
| Calamonte | Badajoz | `municipality:badajoz::calamonte` | pendiente de revisión municipal |
| Calera de León | Badajoz | `municipality:badajoz::calera_de_leon` | pendiente de revisión municipal |
| Calzadilla de los Barros | Badajoz | `municipality:badajoz::calzadilla_de_los_barros` | pendiente de revisión municipal |
| Campanario | Badajoz | `municipality:badajoz::campanario` | pendiente de revisión municipal |
| Campillo de Llerena | Badajoz | `municipality:badajoz::campillo_de_llerena` | pendiente de revisión municipal |
| Capilla | Badajoz | `municipality:badajoz::capilla` | pendiente de revisión municipal |
| Carmonita | Badajoz | `municipality:badajoz::carmonita` | pendiente de revisión municipal |
| Casas de Don Pedro | Badajoz | `municipality:badajoz::casas_de_don_pedro` | pendiente de revisión municipal |
| Casas de Reina | Badajoz | `municipality:badajoz::casas_de_reina` | pendiente de revisión municipal |
| Castilblanco | Badajoz | `municipality:badajoz::castilblanco` | pendiente de revisión municipal |
| Castuera | Badajoz | `municipality:badajoz::castuera` | pendiente de revisión municipal |
| Cheles | Badajoz | `municipality:badajoz::cheles` | pendiente de revisión municipal |
| Cordobilla de Lácara | Badajoz | `municipality:badajoz::cordobilla_de_lacara` | pendiente de revisión municipal |
| Corte de Peleas | Badajoz | `municipality:badajoz::corte_de_peleas` | pendiente de revisión municipal |
| Cristina | Badajoz | `municipality:badajoz::cristina` | pendiente de revisión municipal |
| Don Benito | Badajoz | `municipality:badajoz::don_benito` | pendiente de revisión municipal |
| Don Álvaro | Badajoz | `municipality:badajoz::don_alvaro` | pendiente de revisión municipal |
| El Carrascalejo | Badajoz | `municipality:badajoz::el_carrascalejo` | pendiente de revisión municipal |
| Entrín Bajo | Badajoz | `municipality:badajoz::entrin_bajo` | pendiente de revisión municipal |
| Esparragalejo | Badajoz | `municipality:badajoz::esparragalejo` | pendiente de revisión municipal |
| Esparragosa de Lares | Badajoz | `municipality:badajoz::esparragosa_de_lares` | pendiente de revisión municipal |
| Esparragosa de la Serena | Badajoz | `municipality:badajoz::esparragosa_de_la_serena` | pendiente de revisión municipal |
| Feria | Badajoz | `municipality:badajoz::feria` | pendiente de revisión municipal |
| Fregenal de la Sierra | Badajoz | `municipality:badajoz::fregenal_de_la_sierra` | pendiente de revisión municipal |
| Fuenlabrada de los Montes | Badajoz | `municipality:badajoz::fuenlabrada_de_los_montes` | pendiente de revisión municipal |
| Fuente de Cantos | Badajoz | `municipality:badajoz::fuente_de_cantos` | pendiente de revisión municipal |
| Fuente del Arco | Badajoz | `municipality:badajoz::fuente_del_arco` | pendiente de revisión municipal |
| Fuente del Maestre | Badajoz | `municipality:badajoz::fuente_del_maestre` | pendiente de revisión municipal |
| Fuentes de León | Badajoz | `municipality:badajoz::fuentes_de_leon` | pendiente de revisión municipal |
| Garbayuela | Badajoz | `municipality:badajoz::garbayuela` | pendiente de revisión municipal |
| Garlitos | Badajoz | `municipality:badajoz::garlitos` | pendiente de revisión municipal |
| Granja de Torrehermosa | Badajoz | `municipality:badajoz::granja_de_torrehermosa` | pendiente de revisión municipal |
| Guadiana | Badajoz | `municipality:badajoz::guadiana` | pendiente de revisión municipal |
| Guareña | Badajoz | `municipality:badajoz::guarena` | pendiente de revisión municipal |
| Helechosa de los Montes | Badajoz | `municipality:badajoz::helechosa_de_los_montes` | pendiente de revisión municipal |
| Herrera del Duque | Badajoz | `municipality:badajoz::herrera_del_duque` | pendiente de revisión municipal |
| Higuera de Llerena | Badajoz | `municipality:badajoz::higuera_de_llerena` | pendiente de revisión municipal |
| Higuera de Vargas | Badajoz | `municipality:badajoz::higuera_de_vargas` | pendiente de revisión municipal |
| Higuera de la Serena | Badajoz | `municipality:badajoz::higuera_de_la_serena` | pendiente de revisión municipal |
| Higuera la Real | Badajoz | `municipality:badajoz::higuera_la_real` | pendiente de revisión municipal |
| Hinojosa del Valle | Badajoz | `municipality:badajoz::hinojosa_del_valle` | pendiente de revisión municipal |
| Hornachos | Badajoz | `municipality:badajoz::hornachos` | pendiente de revisión municipal |
| Jerez de los Caballeros | Badajoz | `municipality:badajoz::jerez_de_los_caballeros` | pendiente de revisión municipal |
| La Albuera | Badajoz | `municipality:badajoz::la_albuera` | pendiente de revisión municipal |
| La Codosera | Badajoz | `municipality:badajoz::la_codosera` | pendiente de revisión municipal |
| La Coronada | Badajoz | `municipality:badajoz::la_coronada` | pendiente de revisión municipal |
| La Garrovilla | Badajoz | `municipality:badajoz::la_garrovilla` | pendiente de revisión municipal |
| La Haba | Badajoz | `municipality:badajoz::la_haba` | pendiente de revisión municipal |
| La Lapa | Badajoz | `municipality:badajoz::la_lapa` | pendiente de revisión municipal |
| La Morera | Badajoz | `municipality:badajoz::la_morera` | pendiente de revisión municipal |
| La Nava de Santiago | Badajoz | `municipality:badajoz::la_nava_de_santiago` | pendiente de revisión municipal |
| La Parra | Badajoz | `municipality:badajoz::la_parra` | pendiente de revisión municipal |
| La Roca de la Sierra | Badajoz | `municipality:badajoz::la_roca_de_la_sierra` | pendiente de revisión municipal |
| La Zarza | Badajoz | `municipality:badajoz::la_zarza` | pendiente de revisión municipal |
| Llera | Badajoz | `municipality:badajoz::llera` | pendiente de revisión municipal |
| Llerena | Badajoz | `municipality:badajoz::llerena` | pendiente de revisión municipal |
| Lobón | Badajoz | `municipality:badajoz::lobon` | pendiente de revisión municipal |
| Los Santos de Maimona | Badajoz | `municipality:badajoz::los_santos_de_maimona` | pendiente de revisión municipal |
| Magacela | Badajoz | `municipality:badajoz::magacela` | pendiente de revisión municipal |
| Maguilla | Badajoz | `municipality:badajoz::maguilla` | pendiente de revisión municipal |
| Malcocinado | Badajoz | `municipality:badajoz::malcocinado` | pendiente de revisión municipal |
| Malpartida de la Serena | Badajoz | `municipality:badajoz::malpartida_de_la_serena` | pendiente de revisión municipal |
| Manchita | Badajoz | `municipality:badajoz::manchita` | pendiente de revisión municipal |
| Medellín | Badajoz | `municipality:badajoz::medellin` | pendiente de revisión municipal |
| Medina de las Torres | Badajoz | `municipality:badajoz::medina_de_las_torres` | pendiente de revisión municipal |
| Mengabril | Badajoz | `municipality:badajoz::mengabril` | pendiente de revisión municipal |
| Mirandilla | Badajoz | `municipality:badajoz::mirandilla` | pendiente de revisión municipal |
| Monesterio | Badajoz | `municipality:badajoz::monesterio` | pendiente de revisión municipal |
| Montemolín | Badajoz | `municipality:badajoz::montemolin` | pendiente de revisión municipal |
| Monterrubio de la Serena | Badajoz | `municipality:badajoz::monterrubio_de_la_serena` | pendiente de revisión municipal |
| Montijo | Badajoz | `municipality:badajoz::montijo` | pendiente de revisión municipal |
| Mérida | Badajoz | `municipality:badajoz::merida` | pendiente de revisión municipal |
| Navalvillar de Pela | Badajoz | `municipality:badajoz::navalvillar_de_pela` | pendiente de revisión municipal |
| Nogales | Badajoz | `municipality:badajoz::nogales` | pendiente de revisión municipal |
| Oliva de Mérida | Badajoz | `municipality:badajoz::oliva_de_merida` | pendiente de revisión municipal |
| Oliva de la Frontera | Badajoz | `municipality:badajoz::oliva_de_la_frontera` | pendiente de revisión municipal |
| Olivenza | Badajoz | `municipality:badajoz::olivenza` | pendiente de revisión municipal |
| Orellana de la Sierra | Badajoz | `municipality:badajoz::orellana_de_la_sierra` | pendiente de revisión municipal |
| Orellana la Vieja | Badajoz | `municipality:badajoz::orellana_la_vieja` | pendiente de revisión municipal |
| Palomas | Badajoz | `municipality:badajoz::palomas` | pendiente de revisión municipal |
| Peraleda del Zaucejo | Badajoz | `municipality:badajoz::peraleda_del_zaucejo` | pendiente de revisión municipal |
| Peñalsordo | Badajoz | `municipality:badajoz::penalsordo` | pendiente de revisión municipal |
| Puebla de Alcocer | Badajoz | `municipality:badajoz::puebla_de_alcocer` | pendiente de revisión municipal |
| Puebla de Obando | Badajoz | `municipality:badajoz::puebla_de_obando` | pendiente de revisión municipal |
| Puebla de Sancho Pérez | Badajoz | `municipality:badajoz::puebla_de_sancho_perez` | pendiente de revisión municipal |
| Puebla de la Calzada | Badajoz | `municipality:badajoz::puebla_de_la_calzada` | pendiente de revisión municipal |
| Puebla de la Reina | Badajoz | `municipality:badajoz::puebla_de_la_reina` | pendiente de revisión municipal |
| Puebla del Maestre | Badajoz | `municipality:badajoz::puebla_del_maestre` | pendiente de revisión municipal |
| Puebla del Prior | Badajoz | `municipality:badajoz::puebla_del_prior` | pendiente de revisión municipal |
| Pueblonuevo del Guadiana | Badajoz | `municipality:badajoz::pueblonuevo_del_guadiana` | pendiente de revisión municipal |
| Quintana de la Serena | Badajoz | `municipality:badajoz::quintana_de_la_serena` | pendiente de revisión municipal |
| Reina | Badajoz | `municipality:badajoz::reina` | pendiente de revisión municipal |
| Rena | Badajoz | `municipality:badajoz::rena` | pendiente de revisión municipal |
| Retamal de Llerena | Badajoz | `municipality:badajoz::retamal_de_llerena` | pendiente de revisión municipal |
| Ribera del Fresno | Badajoz | `municipality:badajoz::ribera_del_fresno` | pendiente de revisión municipal |
| Risco | Badajoz | `municipality:badajoz::risco` | pendiente de revisión municipal |
| Salvaleón | Badajoz | `municipality:badajoz::salvaleon` | pendiente de revisión municipal |
| Salvatierra de los Barros | Badajoz | `municipality:badajoz::salvatierra_de_los_barros` | pendiente de revisión municipal |
| San Pedro de Mérida | Badajoz | `municipality:badajoz::san_pedro_de_merida` | pendiente de revisión municipal |
| San Vicente de Alcántara | Badajoz | `municipality:badajoz::san_vicente_de_alcantara` | pendiente de revisión municipal |
| Sancti-Spíritus | Badajoz | `municipality:badajoz::sancti_spiritus` | pendiente de revisión municipal |
| Santa Amalia | Badajoz | `municipality:badajoz::santa_amalia` | pendiente de revisión municipal |
| Santa Marta | Badajoz | `municipality:badajoz::santa_marta` | pendiente de revisión municipal |
| Segura de León | Badajoz | `municipality:badajoz::segura_de_leon` | pendiente de revisión municipal |
| Siruela | Badajoz | `municipality:badajoz::siruela` | pendiente de revisión municipal |
| Solana de los Barros | Badajoz | `municipality:badajoz::solana_de_los_barros` | pendiente de revisión municipal |
| Talarrubias | Badajoz | `municipality:badajoz::talarrubias` | pendiente de revisión municipal |
| Talavera la Real | Badajoz | `municipality:badajoz::talavera_la_real` | pendiente de revisión municipal |
| Tamurejo | Badajoz | `municipality:badajoz::tamurejo` | pendiente de revisión municipal |
| Torre de Miguel Sesmero | Badajoz | `municipality:badajoz::torre_de_miguel_sesmero` | pendiente de revisión municipal |
| Torremayor | Badajoz | `municipality:badajoz::torremayor` | pendiente de revisión municipal |
| Torremejía | Badajoz | `municipality:badajoz::torremejia` | pendiente de revisión municipal |
| Trasierra | Badajoz | `municipality:badajoz::trasierra` | pendiente de revisión municipal |
| Trujillanos | Badajoz | `municipality:badajoz::trujillanos` | pendiente de revisión municipal |
| Táliga | Badajoz | `municipality:badajoz::taliga` | pendiente de revisión municipal |
| Usagre | Badajoz | `municipality:badajoz::usagre` | pendiente de revisión municipal |
| Valdecaballeros | Badajoz | `municipality:badajoz::valdecaballeros` | pendiente de revisión municipal |
| Valdelacalzada | Badajoz | `municipality:badajoz::valdelacalzada` | pendiente de revisión municipal |
| Valdetorres | Badajoz | `municipality:badajoz::valdetorres` | pendiente de revisión municipal |
| Valencia de las Torres | Badajoz | `municipality:badajoz::valencia_de_las_torres` | pendiente de revisión municipal |
| Valencia del Mombuey | Badajoz | `municipality:badajoz::valencia_del_mombuey` | pendiente de revisión municipal |
| Valencia del Ventoso | Badajoz | `municipality:badajoz::valencia_del_ventoso` | pendiente de revisión municipal |
| Valle de Matamoros | Badajoz | `municipality:badajoz::valle_de_matamoros` | pendiente de revisión municipal |
| Valle de Santa Ana | Badajoz | `municipality:badajoz::valle_de_santa_ana` | pendiente de revisión municipal |
| Valle de la Serena | Badajoz | `municipality:badajoz::valle_de_la_serena` | pendiente de revisión municipal |
| Valverde de Burguillos | Badajoz | `municipality:badajoz::valverde_de_burguillos` | pendiente de revisión municipal |
| Valverde de Leganés | Badajoz | `municipality:badajoz::valverde_de_leganes` | pendiente de revisión municipal |
| Valverde de Llerena | Badajoz | `municipality:badajoz::valverde_de_llerena` | pendiente de revisión municipal |
| Valverde de Mérida | Badajoz | `municipality:badajoz::valverde_de_merida` | pendiente de revisión municipal |
| Villafranca de los Barros | Badajoz | `municipality:badajoz::villafranca_de_los_barros` | pendiente de revisión municipal |
| Villagarcía de la Torre | Badajoz | `municipality:badajoz::villagarcia_de_la_torre` | pendiente de revisión municipal |
| Villagonzalo | Badajoz | `municipality:badajoz::villagonzalo` | pendiente de revisión municipal |
| Villalba de los Barros | Badajoz | `municipality:badajoz::villalba_de_los_barros` | pendiente de revisión municipal |
| Villanueva de la Serena | Badajoz | `municipality:badajoz::villanueva_de_la_serena` | pendiente de revisión municipal |
| Villanueva del Fresno | Badajoz | `municipality:badajoz::villanueva_del_fresno` | pendiente de revisión municipal |
| Villar de Rena | Badajoz | `municipality:badajoz::villar_de_rena` | pendiente de revisión municipal |
| Villar del Rey | Badajoz | `municipality:badajoz::villar_del_rey` | pendiente de revisión municipal |
| Villarta de los Montes | Badajoz | `municipality:badajoz::villarta_de_los_montes` | pendiente de revisión municipal |
| Zafra | Badajoz | `municipality:badajoz::zafra` | pendiente de revisión municipal |
| Zahínos | Badajoz | `municipality:badajoz::zahinos` | pendiente de revisión municipal |
| Zalamea de la Serena | Badajoz | `municipality:badajoz::zalamea_de_la_serena` | pendiente de revisión municipal |
| Zarza-Capilla | Badajoz | `municipality:badajoz::zarza_capilla` | pendiente de revisión municipal |
| Abadía | Cáceres | `municipality:caceres::abadia` | pendiente de revisión municipal |
| Abertura | Cáceres | `municipality:caceres::abertura` | pendiente de revisión municipal |
| Acebo | Cáceres | `municipality:caceres::acebo` | pendiente de revisión municipal |
| Acehúche | Cáceres | `municipality:caceres::acehuche` | pendiente de revisión municipal |
| Aceituna | Cáceres | `municipality:caceres::aceituna` | pendiente de revisión municipal |
| Ahigal | Cáceres | `municipality:caceres::ahigal` | pendiente de revisión municipal |
| Alagón del Río | Cáceres | `municipality:caceres::alagon_del_rio` | pendiente de revisión municipal |
| Albalá | Cáceres | `municipality:caceres::albala` | pendiente de revisión municipal |
| Alcollarín | Cáceres | `municipality:caceres::alcollarin` | pendiente de revisión municipal |
| Alcuéscar | Cáceres | `municipality:caceres::alcuescar` | pendiente de revisión municipal |
| Alcántara | Cáceres | `municipality:caceres::alcantara` | pendiente de revisión municipal |
| Aldea del Cano | Cáceres | `municipality:caceres::aldea_del_cano` | pendiente de revisión municipal |
| Aldeacentenera | Cáceres | `municipality:caceres::aldeacentenera` | pendiente de revisión municipal |
| Aldeanueva de la Vera | Cáceres | `municipality:caceres::aldeanueva_de_la_vera` | pendiente de revisión municipal |
| Aldeanueva del Camino | Cáceres | `municipality:caceres::aldeanueva_del_camino` | pendiente de revisión municipal |
| Aldehuela de Jerte | Cáceres | `municipality:caceres::aldehuela_de_jerte` | pendiente de revisión municipal |
| Aliseda | Cáceres | `municipality:caceres::aliseda` | pendiente de revisión municipal |
| Almaraz | Cáceres | `municipality:caceres::almaraz` | pendiente de revisión municipal |
| Almoharín | Cáceres | `municipality:caceres::almoharin` | pendiente de revisión municipal |
| Alía | Cáceres | `municipality:caceres::alia` | pendiente de revisión municipal |
| Arroyo de la Luz | Cáceres | `municipality:caceres::arroyo_de_la_luz` | pendiente de revisión municipal |
| Arroyomolinos | Cáceres | `municipality:caceres::arroyomolinos` | pendiente de revisión municipal |
| Arroyomolinos de la Vera | Cáceres | `municipality:caceres::arroyomolinos_de_la_vera` | pendiente de revisión municipal |
| Barrado | Cáceres | `municipality:caceres::barrado` | pendiente de revisión municipal |
| Baños de Montemayor | Cáceres | `municipality:caceres::banos_de_montemayor` | pendiente de revisión municipal |
| Belvís de Monroy | Cáceres | `municipality:caceres::belvis_de_monroy` | pendiente de revisión municipal |
| Benquerencia | Cáceres | `municipality:caceres::benquerencia` | pendiente de revisión municipal |
| Berrocalejo | Cáceres | `municipality:caceres::berrocalejo` | pendiente de revisión municipal |
| Berzocana | Cáceres | `municipality:caceres::berzocana` | pendiente de revisión municipal |
| Bohonal de Ibor | Cáceres | `municipality:caceres::bohonal_de_ibor` | pendiente de revisión municipal |
| Botija | Cáceres | `municipality:caceres::botija` | pendiente de revisión municipal |
| Brozas | Cáceres | `municipality:caceres::brozas` | pendiente de revisión municipal |
| Cabañas del Castillo | Cáceres | `municipality:caceres::cabanas_del_castillo` | pendiente de revisión municipal |
| Cabezabellosa | Cáceres | `municipality:caceres::cabezabellosa` | pendiente de revisión municipal |
| Cabezuela del Valle | Cáceres | `municipality:caceres::cabezuela_del_valle` | pendiente de revisión municipal |
| Cabrero | Cáceres | `municipality:caceres::cabrero` | pendiente de revisión municipal |
| Cachorrilla | Cáceres | `municipality:caceres::cachorrilla` | pendiente de revisión municipal |
| Cadalso | Cáceres | `municipality:caceres::cadalso` | pendiente de revisión municipal |
| Calzadilla | Cáceres | `municipality:caceres::calzadilla` | pendiente de revisión municipal |
| Caminomorisco | Cáceres | `municipality:caceres::caminomorisco` | pendiente de revisión municipal |
| Campillo de Deleitosa | Cáceres | `municipality:caceres::campillo_de_deleitosa` | pendiente de revisión municipal |
| Campo Lugar | Cáceres | `municipality:caceres::campo_lugar` | pendiente de revisión municipal |
| Carbajo | Cáceres | `municipality:caceres::carbajo` | pendiente de revisión municipal |
| Carcaboso | Cáceres | `municipality:caceres::carcaboso` | pendiente de revisión municipal |
| Carrascalejo | Cáceres | `municipality:caceres::carrascalejo` | pendiente de revisión municipal |
| Casar de Cáceres | Cáceres | `municipality:caceres::casar_de_caceres` | pendiente de revisión municipal |
| Casar de Palomero | Cáceres | `municipality:caceres::casar_de_palomero` | pendiente de revisión municipal |
| Casares de las Hurdes | Cáceres | `municipality:caceres::casares_de_las_hurdes` | pendiente de revisión municipal |
| Casas de Don Antonio | Cáceres | `municipality:caceres::casas_de_don_antonio` | pendiente de revisión municipal |
| Casas de Don Gómez | Cáceres | `municipality:caceres::casas_de_don_gomez` | pendiente de revisión municipal |
| Casas de Millán | Cáceres | `municipality:caceres::casas_de_millan` | pendiente de revisión municipal |
| Casas de Miravete | Cáceres | `municipality:caceres::casas_de_miravete` | pendiente de revisión municipal |
| Casas del Castañar | Cáceres | `municipality:caceres::casas_del_castanar` | pendiente de revisión municipal |
| Casas del Monte | Cáceres | `municipality:caceres::casas_del_monte` | pendiente de revisión municipal |
| Casatejada | Cáceres | `municipality:caceres::casatejada` | pendiente de revisión municipal |
| Casillas de Coria | Cáceres | `municipality:caceres::casillas_de_coria` | pendiente de revisión municipal |
| Castañar de Ibor | Cáceres | `municipality:caceres::castanar_de_ibor` | pendiente de revisión municipal |
| Cañamero | Cáceres | `municipality:caceres::canamero` | pendiente de revisión municipal |
| Cañaveral | Cáceres | `municipality:caceres::canaveral` | pendiente de revisión municipal |
| Ceclavín | Cáceres | `municipality:caceres::ceclavin` | pendiente de revisión municipal |
| Cedillo | Cáceres | `municipality:caceres::cedillo` | pendiente de revisión municipal |
| Cerezo | Cáceres | `municipality:caceres::cerezo` | pendiente de revisión municipal |
| Cilleros | Cáceres | `municipality:caceres::cilleros` | pendiente de revisión municipal |
| Collado de la Vera | Cáceres | `municipality:caceres::collado_de_la_vera` | pendiente de revisión municipal |
| Conquista de la Sierra | Cáceres | `municipality:caceres::conquista_de_la_sierra` | pendiente de revisión municipal |
| Coria | Cáceres | `municipality:caceres::coria` | pendiente de revisión municipal |
| Cuacos de Yuste | Cáceres | `municipality:caceres::cuacos_de_yuste` | pendiente de revisión municipal |
| Cáceres | Cáceres | `municipality:caceres::caceres` | pendiente de revisión municipal |
| Deleitosa | Cáceres | `municipality:caceres::deleitosa` | pendiente de revisión municipal |
| Descargamaría | Cáceres | `municipality:caceres::descargamaria` | pendiente de revisión municipal |
| El Gordo | Cáceres | `municipality:caceres::el_gordo` | pendiente de revisión municipal |
| El Torno | Cáceres | `municipality:caceres::el_torno` | pendiente de revisión municipal |
| Eljas | Cáceres | `municipality:caceres::eljas` | pendiente de revisión municipal |
| Escurial | Cáceres | `municipality:caceres::escurial` | pendiente de revisión municipal |
| Fresnedoso de Ibor | Cáceres | `municipality:caceres::fresnedoso_de_ibor` | pendiente de revisión municipal |
| Galisteo | Cáceres | `municipality:caceres::galisteo` | pendiente de revisión municipal |
| Garciaz | Cáceres | `municipality:caceres::garciaz` | pendiente de revisión municipal |
| Garganta la Olla | Cáceres | `municipality:caceres::garganta_la_olla` | pendiente de revisión municipal |
| Gargantilla | Cáceres | `municipality:caceres::gargantilla` | pendiente de revisión municipal |
| Gargüera | Cáceres | `municipality:caceres::garguera` | pendiente de revisión municipal |
| Garrovillas de Alconétar | Cáceres | `municipality:caceres::garrovillas_de_alconetar` | pendiente de revisión municipal |
| Garvín | Cáceres | `municipality:caceres::garvin` | pendiente de revisión municipal |
| Gata | Cáceres | `municipality:caceres::gata` | pendiente de revisión municipal |
| Guadalupe | Cáceres | `municipality:caceres::guadalupe` | pendiente de revisión municipal |
| Guijo de Coria | Cáceres | `municipality:caceres::guijo_de_coria` | pendiente de revisión municipal |
| Guijo de Galisteo | Cáceres | `municipality:caceres::guijo_de_galisteo` | pendiente de revisión municipal |
| Guijo de Granadilla | Cáceres | `municipality:caceres::guijo_de_granadilla` | pendiente de revisión municipal |
| Guijo de Santa Bárbara | Cáceres | `municipality:caceres::guijo_de_santa_barbara` | pendiente de revisión municipal |
| Herguijuela | Cáceres | `municipality:caceres::herguijuela` | pendiente de revisión municipal |
| Hernán-Pérez | Cáceres | `municipality:caceres::hernan_perez` | pendiente de revisión municipal |
| Herrera de Alcántara | Cáceres | `municipality:caceres::herrera_de_alcantara` | pendiente de revisión municipal |
| Herreruela | Cáceres | `municipality:caceres::herreruela` | pendiente de revisión municipal |
| Hervás | Cáceres | `municipality:caceres::hervas` | pendiente de revisión municipal |
| Higuera de Albalat | Cáceres | `municipality:caceres::higuera_de_albalat` | pendiente de revisión municipal |
| Hinojal | Cáceres | `municipality:caceres::hinojal` | pendiente de revisión municipal |
| Holguera | Cáceres | `municipality:caceres::holguera` | pendiente de revisión municipal |
| Hoyos | Cáceres | `municipality:caceres::hoyos` | pendiente de revisión municipal |
| Huélaga | Cáceres | `municipality:caceres::huelaga` | pendiente de revisión municipal |
| Ibahernando | Cáceres | `municipality:caceres::ibahernando` | pendiente de revisión municipal |
| Jaraicejo | Cáceres | `municipality:caceres::jaraicejo` | pendiente de revisión municipal |
| Jarandilla de la Vera | Cáceres | `municipality:caceres::jarandilla_de_la_vera` | pendiente de revisión municipal |
| Jaraíz de la Vera | Cáceres | `municipality:caceres::jaraiz_de_la_vera` | pendiente de revisión municipal |
| Jarilla | Cáceres | `municipality:caceres::jarilla` | pendiente de revisión municipal |
| Jerte | Cáceres | `municipality:caceres::jerte` | pendiente de revisión municipal |
| La Aldea del Obispo | Cáceres | `municipality:caceres::la_aldea_del_obispo` | pendiente de revisión municipal |
| La Cumbre | Cáceres | `municipality:caceres::la_cumbre` | pendiente de revisión municipal |
| La Garganta | Cáceres | `municipality:caceres::la_garganta` | pendiente de revisión municipal |
| La Granja | Cáceres | `municipality:caceres::la_granja` | pendiente de revisión municipal |
| La Pesga | Cáceres | `municipality:caceres::la_pesga` | pendiente de revisión municipal |
| Ladrillar | Cáceres | `municipality:caceres::ladrillar` | pendiente de revisión municipal |
| Logrosán | Cáceres | `municipality:caceres::logrosan` | pendiente de revisión municipal |
| Losar de la Vera | Cáceres | `municipality:caceres::losar_de_la_vera` | pendiente de revisión municipal |
| Madrigal de la Vera | Cáceres | `municipality:caceres::madrigal_de_la_vera` | pendiente de revisión municipal |
| Madrigalejo | Cáceres | `municipality:caceres::madrigalejo` | pendiente de revisión municipal |
| Madroñera | Cáceres | `municipality:caceres::madronera` | pendiente de revisión municipal |
| Majadas | Cáceres | `municipality:caceres::majadas` | pendiente de revisión municipal |
| Malpartida de Cáceres | Cáceres | `municipality:caceres::malpartida_de_caceres` | pendiente de revisión municipal |
| Malpartida de Plasencia | Cáceres | `municipality:caceres::malpartida_de_plasencia` | pendiente de revisión municipal |
| Marchagaz | Cáceres | `municipality:caceres::marchagaz` | pendiente de revisión municipal |
| Mata de Alcántara | Cáceres | `municipality:caceres::mata_de_alcantara` | pendiente de revisión municipal |
| Membrío | Cáceres | `municipality:caceres::membrio` | pendiente de revisión municipal |
| Mesas de Ibor | Cáceres | `municipality:caceres::mesas_de_ibor` | pendiente de revisión municipal |
| Miajadas | Cáceres | `municipality:caceres::miajadas` | pendiente de revisión municipal |
| Millanes | Cáceres | `municipality:caceres::millanes` | pendiente de revisión municipal |
| Mirabel | Cáceres | `municipality:caceres::mirabel` | pendiente de revisión municipal |
| Mohedas de Granadilla | Cáceres | `municipality:caceres::mohedas_de_granadilla` | pendiente de revisión municipal |
| Monroy | Cáceres | `municipality:caceres::monroy` | pendiente de revisión municipal |
| Montehermoso | Cáceres | `municipality:caceres::montehermoso` | pendiente de revisión municipal |
| Montánchez | Cáceres | `municipality:caceres::montanchez` | pendiente de revisión municipal |
| Moraleja | Cáceres | `municipality:caceres::moraleja` | pendiente de revisión municipal |
| Morcillo | Cáceres | `municipality:caceres::morcillo` | pendiente de revisión municipal |
| Navaconcejo | Cáceres | `municipality:caceres::navaconcejo` | pendiente de revisión municipal |
| Navalmoral de la Mata | Cáceres | `municipality:caceres::navalmoral_de_la_mata` | pendiente de revisión municipal |
| Navalvillar de Ibor | Cáceres | `municipality:caceres::navalvillar_de_ibor` | pendiente de revisión municipal |
| Navas del Madroño | Cáceres | `municipality:caceres::navas_del_madrono` | pendiente de revisión municipal |
| Navezuelas | Cáceres | `municipality:caceres::navezuelas` | pendiente de revisión municipal |
| Nuñomoral | Cáceres | `municipality:caceres::nunomoral` | pendiente de revisión municipal |
| Oliva de Plasencia | Cáceres | `municipality:caceres::oliva_de_plasencia` | pendiente de revisión municipal |
| Palomero | Cáceres | `municipality:caceres::palomero` | pendiente de revisión municipal |
| Pasarón de la Vera | Cáceres | `municipality:caceres::pasaron_de_la_vera` | pendiente de revisión municipal |
| Pedroso de Acim | Cáceres | `municipality:caceres::pedroso_de_acim` | pendiente de revisión municipal |
| Peraleda de San Román | Cáceres | `municipality:caceres::peraleda_de_san_roman` | pendiente de revisión municipal |
| Peraleda de la Mata | Cáceres | `municipality:caceres::peraleda_de_la_mata` | pendiente de revisión municipal |
| Perales del Puerto | Cáceres | `municipality:caceres::perales_del_puerto` | pendiente de revisión municipal |
| Pescueza | Cáceres | `municipality:caceres::pescueza` | pendiente de revisión municipal |
| Piedras Albas | Cáceres | `municipality:caceres::piedras_albas` | pendiente de revisión municipal |
| Pinofranqueado | Cáceres | `municipality:caceres::pinofranqueado` | pendiente de revisión municipal |
| Piornal | Cáceres | `municipality:caceres::piornal` | pendiente de revisión municipal |
| Plasencia | Cáceres | `municipality:caceres::plasencia` | pendiente de revisión municipal |
| Plasenzuela | Cáceres | `municipality:caceres::plasenzuela` | pendiente de revisión municipal |
| Portaje | Cáceres | `municipality:caceres::portaje` | pendiente de revisión municipal |
| Portezuelo | Cáceres | `municipality:caceres::portezuelo` | pendiente de revisión municipal |
| Pozuelo de Zarzón | Cáceres | `municipality:caceres::pozuelo_de_zarzon` | pendiente de revisión municipal |
| Pueblonuevo de Miramontes | Cáceres | `municipality:caceres::pueblonuevo_de_miramontes` | pendiente de revisión municipal |
| Puerto de Santa Cruz | Cáceres | `municipality:caceres::puerto_de_santa_cruz` | pendiente de revisión municipal |
| Rebollar | Cáceres | `municipality:caceres::rebollar` | pendiente de revisión municipal |
| Riolobos | Cáceres | `municipality:caceres::riolobos` | pendiente de revisión municipal |
| Robledillo de Gata | Cáceres | `municipality:caceres::robledillo_de_gata` | pendiente de revisión municipal |
| Robledillo de Trujillo | Cáceres | `municipality:caceres::robledillo_de_trujillo` | pendiente de revisión municipal |
| Robledillo de la Vera | Cáceres | `municipality:caceres::robledillo_de_la_vera` | pendiente de revisión municipal |
| Robledollano | Cáceres | `municipality:caceres::robledollano` | pendiente de revisión municipal |
| Romangordo | Cáceres | `municipality:caceres::romangordo` | pendiente de revisión municipal |
| Rosalejo | Cáceres | `municipality:caceres::rosalejo` | pendiente de revisión municipal |
| Ruanes | Cáceres | `municipality:caceres::ruanes` | pendiente de revisión municipal |
| Salorino | Cáceres | `municipality:caceres::salorino` | pendiente de revisión municipal |
| Salvatierra de Santiago | Cáceres | `municipality:caceres::salvatierra_de_santiago` | pendiente de revisión municipal |
| San Martín de Trevejo | Cáceres | `municipality:caceres::san_martin_de_trevejo` | pendiente de revisión municipal |
| Santa Ana | Cáceres | `municipality:caceres::santa_ana` | pendiente de revisión municipal |
| Santa Cruz de Paniagua | Cáceres | `municipality:caceres::santa_cruz_de_paniagua` | pendiente de revisión municipal |
| Santa Cruz de la Sierra | Cáceres | `municipality:caceres::santa_cruz_de_la_sierra` | pendiente de revisión municipal |
| Santa Marta de Magasca | Cáceres | `municipality:caceres::santa_marta_de_magasca` | pendiente de revisión municipal |
| Santiago de Alcántara | Cáceres | `municipality:caceres::santiago_de_alcantara` | pendiente de revisión municipal |
| Santiago del Campo | Cáceres | `municipality:caceres::santiago_del_campo` | pendiente de revisión municipal |
| Santibáñez el Alto | Cáceres | `municipality:caceres::santibanez_el_alto` | pendiente de revisión municipal |
| Santibáñez el Bajo | Cáceres | `municipality:caceres::santibanez_el_bajo` | pendiente de revisión municipal |
| Saucedilla | Cáceres | `municipality:caceres::saucedilla` | pendiente de revisión municipal |
| Segura de Toro | Cáceres | `municipality:caceres::segura_de_toro` | pendiente de revisión municipal |
| Serradilla | Cáceres | `municipality:caceres::serradilla` | pendiente de revisión municipal |
| Serrejón | Cáceres | `municipality:caceres::serrejon` | pendiente de revisión municipal |
| Sierra de Fuentes | Cáceres | `municipality:caceres::sierra_de_fuentes` | pendiente de revisión municipal |
| Talaveruela de la Vera | Cáceres | `municipality:caceres::talaveruela_de_la_vera` | pendiente de revisión municipal |
| Talaván | Cáceres | `municipality:caceres::talavan` | pendiente de revisión municipal |
| Talayuela | Cáceres | `municipality:caceres::talayuela` | pendiente de revisión municipal |
| Tejeda de Tiétar | Cáceres | `municipality:caceres::tejeda_de_tietar` | pendiente de revisión municipal |
| Tiétar | Cáceres | `municipality:caceres::tietar` | pendiente de revisión municipal |
| Toril | Cáceres | `municipality:caceres::toril` | pendiente de revisión municipal |
| Tornavacas | Cáceres | `municipality:caceres::tornavacas` | pendiente de revisión municipal |
| Torre de Don Miguel | Cáceres | `municipality:caceres::torre_de_don_miguel` | pendiente de revisión municipal |
| Torre de Santa María | Cáceres | `municipality:caceres::torre_de_santa_maria` | pendiente de revisión municipal |
| Torrecilla de los Ángeles | Cáceres | `municipality:caceres::torrecilla_de_los_angeles` | pendiente de revisión municipal |
| Torrecillas de la Tiesa | Cáceres | `municipality:caceres::torrecillas_de_la_tiesa` | pendiente de revisión municipal |
| Torrejoncillo | Cáceres | `municipality:caceres::torrejoncillo` | pendiente de revisión municipal |
| Torrejón el Rubio | Cáceres | `municipality:caceres::torrejon_el_rubio` | pendiente de revisión municipal |
| Torremenga | Cáceres | `municipality:caceres::torremenga` | pendiente de revisión municipal |
| Torremocha | Cáceres | `municipality:caceres::torremocha` | pendiente de revisión municipal |
| Torreorgaz | Cáceres | `municipality:caceres::torreorgaz` | pendiente de revisión municipal |
| Torrequemada | Cáceres | `municipality:caceres::torrequemada` | pendiente de revisión municipal |
| Trujillo | Cáceres | `municipality:caceres::trujillo` | pendiente de revisión municipal |
| Valdastillas | Cáceres | `municipality:caceres::valdastillas` | pendiente de revisión municipal |
| Valdecañas de Tajo | Cáceres | `municipality:caceres::valdecanas_de_tajo` | pendiente de revisión municipal |
| Valdefuentes | Cáceres | `municipality:caceres::valdefuentes` | pendiente de revisión municipal |
| Valdehúncar | Cáceres | `municipality:caceres::valdehuncar` | pendiente de revisión municipal |
| Valdelacasa de Tajo | Cáceres | `municipality:caceres::valdelacasa_de_tajo` | pendiente de revisión municipal |
| Valdemorales | Cáceres | `municipality:caceres::valdemorales` | pendiente de revisión municipal |
| Valdeobispo | Cáceres | `municipality:caceres::valdeobispo` | pendiente de revisión municipal |
| Valencia de Alcántara | Cáceres | `municipality:caceres::valencia_de_alcantara` | pendiente de revisión municipal |
| Valverde de la Vera | Cáceres | `municipality:caceres::valverde_de_la_vera` | pendiente de revisión municipal |
| Valverde del Fresno | Cáceres | `municipality:caceres::valverde_del_fresno` | pendiente de revisión municipal |
| Vegaviana | Cáceres | `municipality:caceres::vegaviana` | pendiente de revisión municipal |
| Viandar de la Vera | Cáceres | `municipality:caceres::viandar_de_la_vera` | pendiente de revisión municipal |
| Villa del Campo | Cáceres | `municipality:caceres::villa_del_campo` | pendiente de revisión municipal |
| Villa del Rey | Cáceres | `municipality:caceres::villa_del_rey` | pendiente de revisión municipal |
| Villamesías | Cáceres | `municipality:caceres::villamesias` | pendiente de revisión municipal |
| Villamiel | Cáceres | `municipality:caceres::villamiel` | pendiente de revisión municipal |
| Villanueva de la Sierra | Cáceres | `municipality:caceres::villanueva_de_la_sierra` | pendiente de revisión municipal |
| Villanueva de la Vera | Cáceres | `municipality:caceres::villanueva_de_la_vera` | pendiente de revisión municipal |
| Villar de Plasencia | Cáceres | `municipality:caceres::villar_de_plasencia` | pendiente de revisión municipal |
| Villar del Pedroso | Cáceres | `municipality:caceres::villar_del_pedroso` | pendiente de revisión municipal |
| Villasbuenas de Gata | Cáceres | `municipality:caceres::villasbuenas_de_gata` | pendiente de revisión municipal |
| Zarza de Granadilla | Cáceres | `municipality:caceres::zarza_de_granadilla` | pendiente de revisión municipal |
| Zarza de Montánchez | Cáceres | `municipality:caceres::zarza_de_montanchez` | pendiente de revisión municipal |
| Zarza la Mayor | Cáceres | `municipality:caceres::zarza_la_mayor` | pendiente de revisión municipal |
| Zorita | Cáceres | `municipality:caceres::zorita` | pendiente de revisión municipal |

## Seguridad y privacidad

Esta revisión no añade CUPS, cuentas, texto libre de usuarios, fotos, direcciones exactas, coordenadas privadas, IPs reales, tokens reales, contratos, facturas, logs, bases de datos reales ni inventario de infraestructura crítica.

No cambia backend, frontend funcional, reportes ciudadanos, Turnstile, HMAC, rate limiting, proxy/IP, SQLite, datasets geográficos ni datos productivos de distribuidoras.
