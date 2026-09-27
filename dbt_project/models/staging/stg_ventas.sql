select
    id as venta_id,
    fecha,
    producto,
    cantidad,
    precio_unitario,
    monto_total,
    cliente_id
from raw_data.ventas