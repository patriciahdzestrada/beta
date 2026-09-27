select
    producto,
    sum(cantidad) as unidades_vendidas,
    sum(monto_total) as ingresos_totales
from {{ ref('stg_ventas') }}
group by producto
order by ingresos_totales desc