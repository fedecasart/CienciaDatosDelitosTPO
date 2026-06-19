# Ciencia de Datos — Trabajo Práctico Obligatorio

## Análisis geoespacial de delitos en CABA y proximidad a sedes policiales

**Materia:** Ciencia de Datos  
**Trabajo:** Trabajo Práctico Obligatorio  
**Cuatrimestre:** 1.er cuatrimestre 2026  
**Docente:** Santiago Martin  
**Universidad:** UADE  
**Integrantes:** [completar integrantes del grupo]  
**Repositorio:** `https://github.com/fedecasart/CienciaDatosDelitosTPO.git`  
**Plataforma de ejecución:** Visual Studio Code + Jupyter Notebook + Python  

---

## Resumen ejecutivo

Este trabajo analiza delitos geolocalizados de la Ciudad Autónoma de Buenos Aires durante 2023, con foco interpretativo en robos y hurtos. El objetivo inicial fue evaluar si la cercanía física a una sede policial se asociaba con una menor ocurrencia de delitos registrados. Para ello se integraron fuentes oficiales de delitos, comisarías, jurisdicciones policiales, barrios y población.

El proyecto siguió una tubería de ciencia de datos: limpieza de coordenadas, descarte de registros no georreferenciables, análisis exploratorio, enriquecimiento geoespacial, cálculo de distancia a la sede policial más cercana, asignación de comisaría jurisdiccional y generación de franjas mediante K-Means.

El resultado preliminar, basado en cantidades absolutas, parecía sugerir una baja de delitos en el entorno inmediato de las comisarías y un pico entre 501 y 900 metros. Sin embargo, al incorporar superficie territorial y población estimada, la interpretación cambió. La franja de 0 a 500 metros registra menos delitos absolutos que la franja de 501 a 900 metros, pero presenta mayor concentración por km² y mayor tasa cada 10.000 habitantes estimados.

La conclusión principal es que no se observa evidencia de un efecto disuasorio asociado exclusivamente con la proximidad física a una sede policial. La menor cantidad absoluta en el primer rango se explica por su menor superficie y menor población total. La proximidad a una sede no debe interpretarse como causalidad: las comisarías suelen ubicarse en zonas más densas, transitadas o comercialmente activas.

---

## 1. Adecuación a la consigna del TPO

El proyecto fue estructurado para responder a los lineamientos del Trabajo Práctico Obligatorio de la materia.

| Requisito del TPO | Implementación en el proyecto |
|---|---|
| Dominio de negocio conocido o de interés | Seguridad urbana y análisis territorial de delitos en CABA |
| Selección de fuentes de datos | Delitos, comisarías, jurisdicciones, barrios y población |
| Desarrollo de hipótesis | Evaluar la relación entre distancia a sedes policiales y concentración delictiva |
| Análisis exploratorio del dataset | Notebook 02: distribución temporal, territorial y por tipo de hecho |
| Técnica de minería / modelo utilizado | K-Means para segmentar distancias a sedes policiales |
| Visualización + storytelling | Comparación entre lectura preliminar y resultados normalizados |
| Aplicación funcional | Panel o app interactiva basada en filtros por barrio, franja horaria, tipo de delito y distancia |
| Valor para el dominio | Evitar decisiones basadas en totales absolutos sin normalización territorial o poblacional |
| Expectativas superadoras | Integración de múltiples fuentes, geoprocesamiento, versionado y narrativa analítica |

El foco del informe no es solamente mostrar gráficos, sino evidenciar el proceso de ciencia de datos: explorar, formular una hipótesis, incorporar variables de control y revisar la conclusión inicial.

---

## 2. Dominio del negocio y audiencia

### 2.1 Dominio

El dominio seleccionado es la seguridad urbana en CABA. El problema se aborda desde una perspectiva de análisis territorial: cómo se distribuyen los delitos registrados en relación con barrios, comunas, franjas horarias y proximidad a sedes policiales.

### 2.2 Audiencia

La audiencia definida por la consigna es gerencial, tanto comercial como técnica.

Para una audiencia gerencial, el valor del proyecto está en transformar datos públicos dispersos en indicadores interpretables: dónde se concentran los hechos, cómo cambian al controlar por superficie y población, qué variables conviene mostrar en un tablero y qué hipótesis no quedan respaldadas por los datos.

Para una audiencia técnica, el valor está en la tubería reproducible: limpieza de datos, normalización de coordenadas, enriquecimiento geoespacial, uso de geometrías y distancias, generación de reportes y visualizaciones.

---

## 3. Problema e hipótesis

### 3.1 Problema

Una lectura simple de delitos por distancia a comisarías puede inducir a conclusiones incorrectas. Si se observan únicamente cantidades absolutas, una franja con más territorio o más población puede parecer más riesgosa solo porque contiene mayor exposición.

El problema abordado es:

> ¿La cercanía física a una sede policial se asocia con una menor concentración de delitos registrados?

### 3.2 Hipótesis inicial

La hipótesis preliminar fue:

> Si existe un efecto disuasorio asociado a la cercanía de una sede policial, los delitos deberían presentar menor concentración relativa en el entorno inmediato de esas sedes.

### 3.3 Reformulación durante el análisis

El análisis preliminar mostró una curva de delitos absolutos que primero subía y luego bajaba. Esto habilitaba una interpretación inicial compatible con una posible disuasión en los primeros 500 metros.

Sin embargo, al normalizar por superficie y población, la interpretación cambió:

> La cercanía física a una sede policial no muestra evidencia de un efecto disuasorio en la concentración relativa de delitos registrados. La menor cantidad absoluta en el primer rango se explica por menor superficie y menor población total.

---

## 4. Fuentes de datos

El proyecto utilizó varias fuentes, lo cual fortalece el análisis y cumple una expectativa superadora del TPO.

| Fuente | Archivo | Uso en el proyecto |
|---|---|---|
| Delitos CABA 2023 | `delitos_2023.csv` / `delitos_2023_caba_limpio.csv` | Base principal de hechos delictivos |
| Comisarías Policía de la Ciudad | `comisarias_policia.csv` | Cálculo de sede policial más cercana |
| Jurisdicciones policiales | `division_comisaria_vecinal.csv` | Asignación de comisaría jurisdiccional |
| Barrios CABA | `barrios.csv` | Polígonos barriales y superficie |
| Población por barrio | `caba_pob_barrios_2010.csv` | Estimación poblacional por franja |
| Comunas | `gcba_pob_comunas_17.csv` | Fuente auxiliar, no usada como base principal por ser más agregada |

La decisión metodológica fue trabajar con barrios para la estimación poblacional porque las comunas son demasiado grandes y pueden ocultar variaciones internas importantes.

---

## 5. Arquitectura de la solución y tubería de datos

```text
Fuentes crudas
     │
     ├── Delitos CABA 2023
     ├── Comisarías
     ├── Jurisdicciones policiales
     ├── Barrios
     └── Población barrial
     │
     ▼
01 Limpieza y normalización
     │
     ├── Conversión de coordenadas
     ├── Descarte de coordenadas vacías
     ├── Descarte de coordenadas 0,0
     └── Descarte de registros fuera de CABA
     │
     ▼
02 Análisis exploratorio
     │
     ├── Tipos de delito
     ├── Barrios y comunas
     ├── Meses, días y franjas horarias
     └── Uso de arma y moto
     │
     ▼
03 Enriquecimiento geoespacial
     │
     ├── Comisaría jurisdiccional
     ├── Sede policial más cercana
     ├── Distancia en metros
     ├── K-Means sobre distancias
     └── Franjas de distancia
     │
     ▼
04 Normalización territorial
     │
     ├── Superficie de cada franja
     └── Delitos por km²
     │
     ▼
05 Normalización poblacional
     │
     ├── Estimación de población por franja
     └── Delitos cada 10.000 habitantes
     │
     ▼
Reportes, visualizaciones y aplicación interactiva
```

---

## 6. Limpieza y preparación de datos

El dataset original contenía 155.897 registros. Durante la limpieza se descartaron 3.158 registros no aptos para análisis espacial.

| Motivo de descarte | Cantidad |
|---|---:|
| Coordenadas vacías o no utilizables | 348 |
| Coordenadas 0,0 | 2.779 |
| Coordenadas con ubicación fuera de CABA o sin barrio/comuna | 31 |
| **Total descartado** | **3.158** |

El dataset limpio final quedó compuesto por **152.739 delitos válidos dentro de CABA**.

Variables derivadas principales:

- `franja_horaria`;
- `es_fin_de_semana`;
- `comisaria_jurisdiccional`;
- `comisaria_mas_cercana`;
- `distancia_comisaria_metros`;
- `franja_distancia_comisaria`.

---

## 7. Análisis exploratorio de datos

### 7.1 Distribución por tipo de delito

| Tipo | Cantidad | % |
| --- | --- | --- |
| Robo | 64.813 | 42,43% |
| Hurto | 62.389 | 40,85% |
| Vialidad | 8.933 | 5,85% |
| Lesiones | 8.788 | 5,75% |
| Amenazas | 7.726 | 5,06% |
| Homicidios | 90 | 0,06% |

Robos y hurtos suman **127.202 hechos**, equivalentes al **83,28%** del dataset limpio.

### 7.2 Barrios con mayor cantidad de delitos registrados

| Barrio | Delitos | % |
| --- | --- | --- |
| PALERMO | 13.047 | 8,54% |
| BALVANERA | 9.958 | 6,52% |
| FLORES | 8.085 | 5,29% |
| RECOLETA | 6.961 | 4,56% |
| CABALLITO | 6.514 | 4,26% |
| VILLA LUGANO | 6.247 | 4,09% |
| ALMAGRO | 5.953 | 3,90% |
| SAN NICOLAS | 5.564 | 3,64% |
| BARRACAS | 5.375 | 3,52% |
| BELGRANO | 4.959 | 3,25% |

La concentración en barrios como Palermo, Balvanera, Flores, Recoleta y Caballito sugiere la importancia de controlar por exposición urbana. Son zonas con alta circulación, actividad comercial, transporte y población flotante.

### 7.3 Franjas horarias

| Franja horaria | Delitos | % |
| --- | --- | --- |
| NOCHE | 45.788 | 29,98% |
| TARDE | 44.738 | 29,29% |
| MAÑANA | 41.434 | 27,13% |
| MADRUGADA | 20.779 | 13,60% |

La distribución horaria permite construir filtros útiles para la aplicación funcional. Sin embargo, el eje principal del presente informe es espacial: la distancia entre los hechos y las sedes policiales.

---

## 8. Feature engineering

El proyecto requirió ingeniería de variables para transformar datos crudos en información analítica.

### 8.1 Variables temporales

Se derivaron variables para facilitar el análisis: franja horaria, fin de semana, mes y día.

### 8.2 Variables geoespaciales

Se generaron variables espaciales a partir de latitud y longitud: punto geográfico del delito, punto geográfico de cada sede policial, polígono de barrio y polígono de jurisdicción policial.

### 8.3 Comisaría jurisdiccional

Cada delito fue asignado a una comisaría jurisdiccional mediante cruce espacial con la capa de jurisdicciones policiales.

### 8.4 Comisaría más cercana

Además de la jurisdicción formal, se calculó la sede policial físicamente más cercana a cada delito. Para ello se usaron las coordenadas de las sedes policiales y se consideraron sedes físicas únicas, evitando duplicar ubicaciones que aparecían más de una vez por motivos administrativos.

La base de comisarías contenía 75 registros administrativos, que se redujeron a 63 sedes físicas únicas.

### 8.5 Distancia a sede policial

Para cada delito se calculó la distancia en metros a la sede policial más cercana. Esta variable se convirtió en el eje del análisis posterior.

---

## 9. Técnica de minería de datos: K-Means

### 9.1 Justificación

Se utilizó K-Means como técnica de aprendizaje no supervisado para segmentar los delitos según su distancia a la sede policial más cercana.

La elección de K-Means se vincula con contenidos de minería de datos y aprendizaje no supervisado vistos en la materia: agrupamiento de observaciones, detección de estructuras sin etiqueta previa, evaluación mediante inercia, método del codo y silueta, e interpretación de clusters para generar valor.

### 9.2 Variable utilizada

```text
distancia_comisaria_metros
```

La finalidad no fue predecir una clase, sino obtener franjas de distancia analíticamente defendibles.

### 9.3 Evaluación de k

| k | Inercia | Silueta | Reducción de inercia |
| --- | --- | --- | --- |
| 2 | 9.389.405.424 | 0,612 | — |
| 3 | 4.642.921.249 | 0,560 | 50,55% |
| 4 | 2.677.490.302 | 0,551 | 42,33% |
| 5 | 1.857.795.511 | 0,530 | 30,61% |
| 6 | 1.268.787.185 | 0,538 | 31,70% |
| 7 | 938.131.384 | 0,543 | 26,06% |
| 8 | 745.268.307 | 0,537 | 20,56% |

La silueta favorecía soluciones más simples, especialmente k=2. Sin embargo, para un tablero de gestión k=2 resultaba demasiado grueso. El método del codo y la utilidad interpretativa llevaron a seleccionar k=4.

### 9.4 Franjas finales

| Franja | Interpretación |
|---|---|
| 0-500 m | Entorno inmediato |
| 501-900 m | Cercana |
| 901-1350 m | Intermedia |
| Más de 1350 m | Alejada |

---

## 10. Resultados preliminares: cantidades absolutas

| Franja de distancia | Delitos registrados | % del total |
| --- | --- | --- |
| ENTORNO INMEDIATO (0-500 m) | 47.871 | 31,34% |
| CERCANA (501-900 m) | 55.074 | 36,06% |
| INTERMEDIA (901-1350 m) | 31.953 | 20,92% |
| ALEJADA (MAS DE 1350 m) | 17.841 | 11,68% |

A simple vista, el resultado parecía indicar que dentro de 0-500 m hay menos delitos que entre 501-900 m, que el máximo absoluto se encuentra en la franja cercana y que luego la cantidad baja en las franjas más alejadas.

Esta lectura podía sugerir una hipótesis preliminar compatible con disuasión en el entorno inmediato de las comisarías.

![Cantidad absoluta de delitos por franja](reports/figures/cantidad_absoluta_delitos_por_franja_distancia.png)

Sin embargo, esta primera lectura comparaba cantidades absolutas sin considerar que cada franja ocupa distinta superficie y contiene distinta población.

---

## 11. Normalización territorial

Para corregir la lectura preliminar se calculó cuánta superficie de CABA queda dentro de cada franja de distancia. Luego se estimaron delitos por km².

| Franja de distancia | Superficie | Delitos | Delitos/km² | Índice vs. 0-500 |
| --- | --- | --- | --- | --- |
| ENTORNO INMEDIATO (0-500 m) | 43,05 km² | 47.871 | 1.112,1 | 1,00 |
| CERCANA (501-900 m) | 63,86 km² | 55.074 | 862,4 | 0,78 |
| INTERMEDIA (901-1350 m) | 53,11 km² | 31.953 | 601,6 | 0,54 |
| ALEJADA (MAS DE 1350 m) | 43,88 km² | 17.841 | 406,6 | 0,37 |

El resultado cambia la interpretación: la franja 0-500 m no es la de mayor cantidad absoluta, pero sí es la de mayor concentración territorial. La tasa de delitos por km² disminuye progresivamente al aumentar la distancia.

![Delitos por km² por franja](reports/figures/delitos_por_km2_por_franja_distancia.png)

Esto muestra que el pico absoluto entre 501 y 900 metros se explica en gran parte porque esa franja contiene más superficie total.

---

## 12. Normalización poblacional

La segunda corrección consistió en estimar la población dentro de cada franja. Para ello se cruzaron las franjas de distancia con los polígonos barriales y se distribuyó la población de cada barrio proporcionalmente a la superficie del barrio contenida en cada franja.

La estimación supone población uniforme dentro de cada barrio. Es una aproximación razonable, pero debe declararse como limitación.

| Franja de distancia | Población estimada | Hab./km² | Delitos cada 10.000 hab. | Índice vs. 0-500 |
| --- | --- | --- | --- | --- |
| ENTORNO INMEDIATO (0-500 m) | 694.805 | 16.140,4 | 689,0 | 1,00 |
| CERCANA (501-900 m) | 966.088 | 15.127,1 | 570,1 | 0,83 |
| INTERMEDIA (901-1350 m) | 706.593 | 13.303,3 | 452,2 | 0,66 |
| ALEJADA (MAS DE 1350 m) | 522.665 | 11.911,2 | 341,3 | 0,50 |

![Densidad poblacional estimada por franja](reports/figures/densidad_poblacional_estimada_por_franja_distancia.png)

La densidad poblacional estimada también disminuye con la distancia. La franja alejada tiene menor densidad poblacional que las franjas más cercanas.

Al calcular delitos cada 10.000 habitantes estimados, la disminución vuelve a aparecer:

![Delitos cada 10.000 habitantes por franja](reports/figures/delitos_cada_10k_habitantes_por_franja_distancia.png)

Esto refuerza la conclusión: la menor cantidad absoluta de delitos en el rango 0-500 m no prueba disuasión. Al normalizar por población, la concentración relativa sigue siendo mayor en el entorno inmediato.

---

## 13. Foco interpretativo en robos y hurtos

Aunque los notebooks de normalización reportan el total de delitos registrados, el foco interpretativo principal son robos y hurtos, por ser los delitos contra la propiedad más numerosos y más directamente vinculados con oportunidad territorial.

Al restringir el análisis a robos y hurtos, el patrón se mantiene:

| Franja de distancia | Robos + hurtos | Robos+hurtos/km² | Robos+hurtos cada 10.000 hab. |
| --- | --- | --- | --- |
| ENTORNO INMEDIATO (0-500 m) | 40.396 | 938,4 | 581,4 |
| CERCANA (501-900 m) | 46.318 | 725,3 | 479,4 |
| INTERMEDIA (901-1350 m) | 26.417 | 497,4 | 373,9 |
| ALEJADA (MAS DE 1350 m) | 14.071 | 320,7 | 269,2 |

La tasa de robos y hurtos por km² y cada 10.000 habitantes estimados también es mayor en el entorno inmediato y disminuye con la distancia. Por lo tanto, la conclusión central no depende de incluir o excluir otros tipos de delitos.

---

## 14. Discusión

### 14.1 Interpretación del cambio de resultados

La historia analítica del proyecto es uno de sus principales aportes:

1. En valores absolutos, parecía haber menos delitos cerca de las comisarías.
2. Al incorporar superficie, se observó que la concentración territorial era mayor cerca de las sedes.
3. Al incorporar población, se observó que la tasa por habitante estimado también era mayor cerca de las sedes.
4. La hipótesis preliminar de disuasión por proximidad no quedó respaldada.

Esto muestra la diferencia entre dato, información y conocimiento: el dato bruto era el conteo absoluto; la información apareció al normalizar; el conocimiento surge al corregir la interpretación inicial.

### 14.2 Causalidad inversa

El resultado no significa que las comisarías generen delitos. La interpretación más razonable es que las sedes policiales suelen ubicarse en zonas más densas, transitadas, comerciales o históricamente relevantes.

```text
No necesariamente:
comisaría cercana → más delitos

Sino posiblemente:
zona densa y con alta actividad urbana → ubicación de comisaría y mayor registro de delitos
```

Por eso, la conclusión debe formularse con cuidado:

> No se observa evidencia de un efecto disuasorio asociado exclusivamente con la proximidad física a sedes policiales.

No corresponde afirmar que la presencia policial en general no disuada, porque el dataset no mide patrullaje, cámaras, operativos, cantidad de agentes ni tiempos de respuesta.

### 14.3 Valor para la gestión

El valor del proyecto está en evitar una lectura equivocada basada solo en cantidades absolutas. Para la gestión urbana o policial, esto implica que los tableros deberían mostrar tasas normalizadas y no únicamente conteos.

---

## 15. Aplicación funcional y KPIs propuestos

Para cumplir con la consigna del TPO, el análisis debe acompañarse con una aplicación funcional o tablero interactivo. La app puede implementarse en Streamlit, Power BI, Looker Studio o una herramienta equivalente.

### 15.1 Filtros sugeridos

- Tipo de delito.
- Barrio.
- Comuna.
- Franja horaria.
- Día de semana / fin de semana.
- Uso de arma.
- Uso de moto.
- Comisaría jurisdiccional.
- Franja de distancia a sede policial.

### 15.2 Indicadores principales

| KPI | Descripción |
|---|---|
| Total de delitos | Cantidad de hechos filtrados |
| Robos + hurtos | Subconjunto principal del análisis |
| Delitos por km² | Indicador territorial normalizado |
| Delitos cada 10.000 habitantes | Indicador poblacional estimado |
| Distancia mediana a sede policial | Proximidad típica de los hechos |
| % de delitos alejados | Participación de hechos a más de 1.350 m |
| % con uso de arma | Indicador de gravedad |
| % con uso de moto | Indicador de modalidad |

### 15.3 Visualizaciones sugeridas

- Mapa de delitos.
- Barras por franja de distancia.
- Barras de delitos por km².
- Barras de delitos cada 10.000 habitantes.
- Ranking de barrios.
- Matriz barrio/franja horaria.
- Filtros por tipo, arma y moto.

---

## 16. Conclusiones

La conclusión principal del proyecto es:

> La cercanía física a una sede policial no muestra evidencia de un efecto disuasorio observable en la concentración relativa de delitos registrados en CABA durante 2023.

La lectura preliminar de cantidades absolutas sugería una posible baja en el entorno inmediato de las comisarías. Sin embargo, al incorporar superficie territorial y población estimada, la interpretación se revierte.

La franja de 0-500 m:

- registra menos delitos absolutos que la franja de 501-900 m;
- pero ocupa menos superficie total;
- contiene menos población total;
- presenta mayor concentración de delitos por km²;
- presenta mayor tasa de delitos cada 10.000 habitantes estimados.

Por lo tanto, la menor cantidad absoluta en el entorno inmediato no prueba disuasión. Se explica mejor por menor exposición territorial y poblacional.

El aporte metodológico del trabajo consiste en demostrar que una hipótesis razonable puede cambiar al enriquecer los datos y normalizar los indicadores. Esa es precisamente una práctica central de la ciencia de datos: no quedarse con el primer gráfico, sino controlar por variables relevantes antes de concluir.

---

## 17. Limitaciones

1. La población usada corresponde a 2010, mientras que los delitos son de 2023.
2. La estimación poblacional supone distribución uniforme dentro de cada barrio.
3. La población residencial no mide población flotante.
4. No se incorporaron variables de actividad comercial, transporte, turismo o uso del suelo.
5. La distancia a una sede policial no mide presencia policial efectiva.
6. No se cuenta con información sobre patrullajes, cámaras, agentes disponibles ni tiempos de respuesta.
7. La distancia utilizada es geográfica, no distancia por recorrido vial.
8. Los delitos analizados son delitos registrados; pueden existir sesgos de denuncia.

---

## 18. Trabajo futuro

Como continuación del proyecto podrían incorporarse:

- radios censales 2022 para estimar mejor población;
- datos de transporte público;
- densidad comercial;
- datos de espacios verdes, autopistas, playas ferroviarias y grandes predios;
- trazado de calles para calcular distancia caminable o vial;
- datos de cámaras o patrullajes;
- modelos predictivos supervisados para estimar riesgo relativo por zona y horario.

También podría compararse la distancia a la sede policial con la distancia a corredores comerciales, estaciones de subte, trenes, centros de transbordo y avenidas principales.

---

## 19. Organización del proyecto

### 19.1 Notebooks principales

| Notebook | Contenido |
|---|---|
| `01_data_cleaning.ipynb` | Limpieza, normalización de coordenadas y descarte de registros no georreferenciables |
| `02_exploratory_analysis.ipynb` | EDA general del dataset limpio |
| `03_enriquecimiento_comisarias_y_franjas.ipynb` | Enriquecimiento geoespacial, distancia a sede, K-Means y franjas |
| `04_normalizacion_territorial.ipynb` | Superficie por franja y delitos por km² |
| `05_normalizacion_poblacional.ipynb` | Población estimada por franja y delitos cada 10.000 habitantes |

### 19.2 Reportes generados

| Archivo | Descripción |
|---|---|
| `reports/tables/reporte_franjas_distancia_comisaria.csv` | Conteos absolutos por franja |
| `reports/tables/reporte_normalizacion_territorial.csv` | Superficie y delitos por km² |
| `reports/tables/reporte_normalizacion_poblacional.csv` | Población estimada y delitos cada 10.000 habitantes |
| `reports/tables/detalle_poblacion_estimada_barrio_franja.csv` | Detalle de población estimada por barrio y franja |
| `datasets/processed/zonas_distancia_comisarias.geojson` | Polígonos de franjas de distancia |

---

## 20. Roles sugeridos para la exposición

La exposición dura 15 minutos, por lo que conviene dividir roles:

| Rol | Contenido |
|---|---|
| Integrante 1 | Dominio, problema, hipótesis y fuentes |
| Integrante 2 | Limpieza, EDA y feature engineering |
| Integrante 3 | K-Means, normalización territorial/poblacional, conclusiones y demo del panel |

---

## 21. Referencias

- Gobierno de la Ciudad Autónoma de Buenos Aires. Dataset de delitos geolocalizados 2023.
- Gobierno de la Ciudad Autónoma de Buenos Aires. Dataset de comisarías de la Policía de la Ciudad.
- Gobierno de la Ciudad Autónoma de Buenos Aires. División de comisarías vecinales.
- Gobierno de la Ciudad Autónoma de Buenos Aires. Polígonos de barrios.
- Base de población por barrios de CABA 2010.
- Material de clase de Ciencia de Datos: análisis exploratorio, minería de datos, aprendizaje no supervisado, K-Means, validación y visualización.
- Consigna del Trabajo Práctico Obligatorio de Ciencia de Datos, 1.er cuatrimestre 2026.

---

## Anexo: formulación final para presentación

> El análisis inicial de cantidades absolutas sugería una posible reducción de delitos dentro de los primeros 500 metros de las sedes policiales. Sin embargo, esa interpretación cambió al incorporar la superficie territorial y la población estimada de cada franja. Al normalizar los datos, se observó que la densidad de delitos por km² y la cantidad de delitos por habitante son mayores cerca de las sedes y disminuyen progresivamente con la distancia. En consecuencia, la menor cantidad absoluta dentro de los primeros 500 metros no se explica por un efecto disuasorio evidente, sino por la menor superficie y población total comprendidas en esa franja.
