# Pruebas de conectividad en equipos del dominio

👤 Persona: kike

Se inició una nueva jornada de pruebas de conectividad desde los equipos que forman parte del dominio. En un primer momento, todo parecía estar correctamente configurado en **pfSense**, pero se detectaban problemas al recibir respuesta a las peticiones realizadas.

Inicialmente, se consideró que el origen del problema estaba relacionado con la configuración de NAT. Sin embargo, tras realizar múltiples pruebas y verificar diferentes configuraciones, se descartó esta hipótesis.

Finalmente, se identificó que la causa del problema era mucho más simple de lo esperado: el correcto funcionamiento se restablecía al deshabilitar el cortafuegos y el NAT.

Tras aplicar este cambio, el tráfico hacia Internet se restableció correctamente y la VPN volvió a funcionar con normalidad.

### Conclusión

El incidente pone de manifiesto la importancia de comprobar también las configuraciones más básicas antes de centrarse en problemas más complejos.