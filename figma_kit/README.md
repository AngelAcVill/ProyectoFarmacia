# Kit de Figma — Dashboards Farmacia Yza

Este kit es la fuente de verdad visual de las vistas implementadas en
`login_diseno/templates/dashboard.html` y `login_diseno/static/dashboard.css`.
Los colores salen del login original (`#19C3A5`, `#0E8F87`, `#0D2B2E`, `#1B6FD1`,
`#FFD45C`, `#FF8FA3`), por lo que el dashboard y el login comparten identidad.

> No se importó nada desde Figma: no había `FIGMA_TOKEN` ni un archivo compartido.
> Esta guía permite montar el archivo de Figma idéntico al código, o revisar el
> diseño antes de moverlo a Figma. Los tokens en `tokens.json` se pueden cargar
> con el plugin *Figma Tokens / Tokens Studio* (Import → JSON) o crear como
> Color/Text/Effect styles manualmente.

## 1. Styles y Variables

1. Crea un archivo nuevo en Figma con **1440 × 1024** como frame base.
2. Importa `tokens.json`: pestaña **Variables → Import**, o el plugin
   *Tokens Studio* → `Settings → Load from JSON`.
3. Convierte `colors` en **Color styles**, `typography.styles` en **Text styles**
   y `effects` en **Effect styles**. Usa la tipografía **Poppins** (Google Fonts).
4. Fija el frame de fondo con `UI/Fondo #F4F8F7` y un radial suave de menta
   arriba a la derecha y azul abajo a la izquierda (opacidad 10–16%).

## 2. Componentes (Auto layout)

| Componente | Medida / propiedades |
| --- | --- |
| `Sidebar` | 264 px de ancho, alto 1024, gradiente sidebar, padding 26/18. Contenedor vertical: brand, label "MENÚ PRINCIPAL", lista de ítems, tarjeta de perfil, footer de usuario. |
| `NavItem` | Alto 40, radio 11, ícono 20 + texto 13.5, gap 12. Variantes `default` (blanco 82%) y `active` (blanco 20% + punto amarillo). |
| `Topbar` | Alto 72, fondo blanco 88% + blur 14, borde inferior `UI/Linea`. Migas a la izquierda; chips de sucursal/rol, campana y avatar a la derecha. |
| `KpiCard` | 4 columnas, gap 18, radio 18, padding 20, barra superior de 3 px degradada. Ícono 38×38 con fondo tintado, valor 23/700, pie 10. |
| `Panel` | Radio 18, borde `UI/Linea`, sombra `shadow-panel`, padding 22. Header: título 15/700 + subtítulo 11 + chip opcional. |
| `ChartBars` | Alto 186, 7 barras, radio 8 arriba, degradado `Barras gráfica`, líneas guía cada 44 px. |
| `Table` | Header fondo `#F5FAF8`, texto 10/600, filas 11 px de padding, hover `#F8FCFA`. |
| `Chip` | Radio 999, padding 4–10, texto 10/600. Variantes: Operación, Crítico, Libre, Receta, Rol. |
| `AlertItem` | Punto amarillo 9 px + nombre + detalle + chip "Reponer". |
| `NodeCard` | Radio 15, degradado blanco→#F3FBF8, 3 métricas en columna, enlace "Ver detalle →". |
| `HeroPOS` | Radio 22, gradiente hero, orbe radiente y píldora amarilla decorativa, botón "Nueva venta". |
| `BtnPrimary` | Radio 12, degradado `Botón principal`, alto 40, texto 13/600. |
| `Icon` | 20×20, stroke 1.8, redondo. Mismos paths que los `<symbol>` de `dashboard.html`. |

## 3. Frames por puesto/rol

Cada frame usa el mismo shell (sidebar + topbar) y cambia el contenido.
Seis roles mapeados en `login_diseno/perfiles.py`:

### `01_Administrador` — "Centro de control" (acceso total)
1. KPIs: Ventas hoy (red), Pedidos hoy, Empleados, Alertas de stock.
2. Panel **Estado de la red**: 3 `NodeCard` (Norte / Centro / Sur) con punto
   verde "Operativo" y métricas por nodo.
3. Fila 2fr/1fr: `ChartBars` + lista de alertas.
4. Fila 1fr/2fr: ranking de medicamentos + tabla de bitácora de auditoría.
5. Panel **Accesos rápidos**: Ver nodos, Auditoría, Usuarios.

### `02_Gerente` — "Resumen de sucursal"
1. KPIs: Ventas de hoy, Pedidos, Clientes, Stock bajo.
2. Fila 2fr/1fr: gráfica semanal + alertas.
3. Fila 1fr/2fr: productos favoritos (mini barras de progreso) + ventas recientes.
4. Fila 1fr/1fr: accesos rápidos + panel "Tu sucursal" con datos del nodo.

### `03_Operador` — "Punto de venta" (cajero)
1. `HeroPOS` con saludo, turno activo y CTA "Nueva venta".
2. KPIs compactos: Ventas hoy, Ticket promedio, Medicamentos, Stock bajo.
3. Panel **Buscar medicamento**: campo con lupa y tabla filtrable.
4. Fila 1fr/1fr: últimas ventas + accesos rápidos.

### `04_Auditor` — "Panel de auditoría"
1. Banner de aviso con ícono ojo, borde azul claro y chip "Monitoreo".
2. KPIs: Movimientos, Inventarios, Alertas, Ventas hoy.
3. Panel ancho **Bitácora de auditoría** (tabla de operaciones).
4. Fila 1fr/1fr: control de stock + inventario actual con chips de estado.
5. Accesos rápidos con "Exportar reporte".

### `05_Consulta` — "Consultas y catálogo" (solo lectura)
1. Banner "Modo solo lectura" + chip `Consulta`.
2. Panel **Catálogo de medicamentos** con buscador y tabla de 5 columnas.
3. Fila 1fr/1fr: disponibilidad (ranking con estado) + accesos rápidos.

### `06_Vistas_secundarias`
Frame por cada opción del menú (`Ventas`, `Inventario`, `Clientes`,
`Usuarios y roles`, `Auditoría`, `Recetas`, `Red y sucursales`, `Reportes`,
`Ayuda`). Todas comparten un banner de sección con ícono, título, descripción
y chip del rol, seguido de la tabla correspondiente.

## 4. Reglas de consistencia

- Un solo acento principal: `--yz-teal #19C3A5`; el azul y el amarillo solo
  en estados, chips y decoración (igual que en el login).
- Radio 18 para tarjetas grandes, 11–12 para botones e íconos, 999 para chips.
- Sombra siempre suave (`0 12px 30px rgba(13,43,46,.06)`), sin bordes duros.
- Los íconos son componentes con `stroke=currentColor`; en Figma usa variables
  de color para que hereden el color del contenedor.
- Los estados de alerta usan amarillo `#FFD45C` (stock) y rosa `#FF8FA3`
  (notificaciones), nunca rojo puro.
- Diseño responsive: breakpoint 1180 px → KPIs en 2 columnas y paneles en 1;
  960 px → sidebar se convierte en drawer; 620 px → KPIs en 1 columna.

## 5. Correspondencia código ↔ Figma

| Figma | Código |
| --- | --- |
| Color/Text/Effect styles | `figma_kit/tokens.json` y `:root` de `static/dashboard.css` |
| Componentes | `templates/partials/_macros.html` |
| Frames por rol | `templates/partials/resumen_*.html` |
| Variantes de menú | `login_diseno/perfiles.py` (`PERFILES`) |
| Iconos | `<symbol>` en `templates/dashboard.html` |
