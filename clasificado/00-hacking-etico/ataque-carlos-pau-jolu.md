# Ataque Carlos/Pau/Jolu

Escaneo de red con netdiscover

```bash
sudo netdiscover -r 172.29.230.129/25
```

![CapturaNetdiscover.png](Ataque%20Carlos%20Pau%20Jolu/CapturaNetdiscover.png)

IP publica de Benimerda: `172.29.230.171` .

Escaneo de puertos típicos.

```bash
nmap -p 22,80,443 -sS -sC -sV --disable-arp-ping -vvv --open --min-rate 5000 172.29.230.171
```

![CapturaNmap.png](Ataque%20Carlos%20Pau%20Jolu/CapturaNmap.png)

Entro a la IP desde el navegador por el puerto 443 ya que usan https.

`https://172.29.230.171:443`

![CapturaLoginJSBach.png](Ataque%20Carlos%20Pau%20Jolu/CapturaLoginJSBach.png)

Veo el panel de su JSBach pero tienen login pruebo cosas típicas y entra con `admin:admin` .

![CapturaJSBachLosChichos.png](Ataque%20Carlos%20Pau%20Jolu/CapturaJSBachLosChichos.png)

Exploro todo el router para sacar información de provecho.

![CapturaVlansDHCP.png](Ataque%20Carlos%20Pau%20Jolu/CapturaVlansDHCP.png)

![CapturaWifiAyuntamientoBenimerda.png](Ataque%20Carlos%20Pau%20Jolu/CapturaWifiAyuntamientoBenimerda.png)

Ahora sabiendo sus vlans cambio mi tabla de enrutamiento para poder llegar a toda su infraestructura, ayuda de Joselu.

```bash
sudo ip r a 10.0.0.0/8 via 172.29.230.171
```

![CapturaIProutemodificado.png](Ataque%20Carlos%20Pau%20Jolu/CapturaIProutemodificado.png)

Sigo sin tener acceso a las Vlans.

Encontramos que la IP `172.29.230.170` también llega a otro router y tiene otras Vlans, entre ellas la vlan 99 la cual es la de los backups.

![CapturaVlans170.png](Ataque%20Carlos%20Pau%20Jolu/CapturaVlans170.png)

![CapturaVlans171.png](Ataque%20Carlos%20Pau%20Jolu/CapturaVlans171.png)

Ahora sabiendo como tienen configurada las vlans modificamos la tabla de enrutamiento de nuestro equipo para tener acceso a todas sus vlans.

```bash
sudo ip r a 10.0.0.0/16 via 172.29.230.170
```

```bash
sudo ip r a 10.1.0.0/16 via 172.29.230.171
```

![CapturaTablaEnrutamiento.png](Ataque%20Carlos%20Pau%20Jolu/CapturaTablaEnrutamiento.png)

Gracias a esto, ya vemos las vlans.

Intento de fichero de configuración de VPN, pero no tenemos la private key del cliente. Posible creación de fichero de VPN para nosotros y ganar acceso gracias a eso.

Ahora hemos visto en la configuración de VPN del cliente, hay un campo para la ruta del fichero y probamos ha hacer path traversal y leer ficheros internos pero nos tira *Forbidden* por falta de permisos ya que se ejecuta por www-data y no tiene permisos para ver el contenido de ficheros mas que los `cgi-bin`.

Investigando su red, en la vlan del SOC, localizamos la IP del Wazuh `10.0.3.2` , vemos el login basico.

![CapturaNmapVlanSOC.png](Ataque%20Carlos%20Pau%20Jolu/CapturaNmapVlanSOC.png)

![CapturaSOC.png](Ataque%20Carlos%20Pau%20Jolu/CapturaSOC.png)

Miramos otras rutas y vemos que tienen la versión de Apache expuesta.

![CapturaVersionApacheSOC.png](Ataque%20Carlos%20Pau%20Jolu/CapturaVersionApacheSOC.png)

Posibles ataques de denegación de servicios por esta versión 2.4.58 pero no conseguimos sacar nada de momento, en el login hemos reutilizado todas las credenciales que tenemos y no funciona ninguna, ya que sabemos que tienen las credenciales de la instalación.

Exploro otra vlan, y localizamos el AD por los servicios abiertos, y sé también que en el equipo del AD esta el Odoo. Reutilizamos la cuenta de su funcionario1, y consigo entrar.

![CapturaNmapAD.png](Ataque%20Carlos%20Pau%20Jolu/63ba0185-0d74-43a4-b8b3-b9b322b2a4e6.png)

![CapturaNmapAD.png](Ataque%20Carlos%20Pau%20Jolu/6c658546-e985-4bb4-9d79-ca816c8c1620.png)

![CaputuraEmpleadosOdoo.png](Ataque%20Carlos%20Pau%20Jolu/CaputuraEmpleadosOdoo.png)

A la par, Jose Luis se incorpora a ayudar al Red Team y sigue los pasos de Carlos. Una de las cosas que pruebo es añadirme las rutas hacia la subred de Benimerda al igual que hizo Carlos.
Me pongo a investigar el SOC y me doy cuenta de que tiene los puertos 80 y 443. Se me ocurre correrle un gobuster para ver porqué wazuh tiene el puerto 80 abierto y encontramos un sistema de monitorización empresarial llamado Zabbix.

![imagen.png](Ataque%20Carlos%20Pau%20Jolu/imagen.png)

Al acceder a la URL encuentro esto:

![imagen.png](Ataque%20Carlos%20Pau%20Jolu/imagen%201.png)

Al ser un software empresarial, se me ocurre buscar por sus credenciales por defecto:

![imagen.png](Ataque%20Carlos%20Pau%20Jolu/imagen%202.png)

Al probarlas en la web, funcionan:

![imagen.png](Ataque%20Carlos%20Pau%20Jolu/imagen%203.png)

Más allá de aqui, no he encontrado nada de valor. Me he fijado en que configuraron en su momento el JSBach del ayuntamiento en este sistema de monitorización con la IP 10.0.1.1, pero ahora es inaccesible y apenas hay información sobre el equipo.

Hemos seguido probando cosas escaneando el resto de la red en busca de otros equipos vulnerables.

Sabemos que el JSBach de ambos lados están muy bastionados para bloquear ataques como Path Traversal o XSS, por lo que no tenemos la opción de ver o modificar algo de la web.
Por tanto, vulnerar los JSBach queda descartado.

Sabemos que tienen el SOC con unas credenciales no acordes a lo acordado (usuario del ejercicio de OSINT) ya que nos lo han dicho explícitamente ellos. A sabiendas de que podría ser una mentira para que nos rindamos, hemos probado igualmente las credenciales sin éxito.

Sabiendo esto, lo único que nos queda es la contraseña del usuario por defecto “admin”, que se genera en la instalación. Según lo que nos ha dicho el otro equipo, esa contraseña la tienen guardada en alguno de los equipos en texto plano y que es una contraseña considerablemente larga, por lo que es inviable sacarla por fuerza bruta.

También hemos detectado que el SOC tiene expuesto el puerto 22 y parece que se puede iniciar sesión a través de él mediante contraseña. Dado que probablemente tampoco han cambiado las credenciales de todos los equipos, tanto de los servicios como localmente, no podemos utilizar las contraseñas conseguidas por OSINT para intentar un ataque por fuerza bruta.

Aun con esas, Jose Luis ha lanzado un ataque con hydra con usuario “admin” usando el diccionario “rockyou.txt” en caso de que hubiera suerte, pero sin éxito.

También hemos identificado un ordenador en el que se realizan backups con IP 10.0.99.2 y que, hasta donde sabemos, tiene el puerto 22 expuesto pero SOLO acepta conexiones mediante par de claves pública/privada.

Probablemente este par de claves se encuentra o en el SOC o en los JSBach, y estas opciones ya han quedado descartadas, asi que tampoco podemos seguir escalando por aqui.

Podríamos modificar su Gateway ya que tenemos acceso a la web de los JSBach y hacer un MiTM para intentar sacar alguna credencial o par de claves del ordenador de backups, pero eso afectaría al correcto funcionamiento de su red y tampoco tenemos la garantía de que obtendremos credenciales, ya que solo podríamos capturar el tráfico que vaya o vuelva de Internet, el cuál probablemente irá cifrado.

Debido a que su ayuntamiento no lo tienen prácticamente acabado, la DMZ no se encuentra disponible, y no tenemos la capacidad o el conocimiento suficiente para buscar otros vectores de ataque, descartamos los posibles que les podamos llegar a hacer y procedemos a intentar atacarnos a nosotros mismos.

A partir de este punto nos encargamos de hacer un reconocimiento de la red con:

```jsx
nmap 172.29.230.128/25
```

 e identificamos las POSIBLES IPs del ayuntamiento de guarroman: 172.29.230.160 y 172.29.230.161

```jsx
Nmap scan report for 172.29.230.161
Host is up (0.00062s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT     STATE SERVICE
80/tcp   open  http
443/tcp  open  https
5001/tcp open  commplex-link
```

![CapturaNmap161.png](Ataque%20Carlos%20Pau%20Jolu/CapturaNmap161.png)

Hacemos un escaneo más profundo con:

```bash
nmap -sC -sV -p 80,443,5001 --open -vvv -oX ports.xml 172.29.230.161
```

![CapturaServicios161.png](Ataque%20Carlos%20Pau%20Jolu/CapturaServicios161.png)

```bash
xsltproc ports.xml -o ports.html
```

Y encontramos la siguiente información:

```jsx
Nmap scan report for 172.29.230.161
Host is up, received syn-ack (0.00034s latency).
Scanned at 2026-05-19 09:51:04 CEST for 93s

PORT     STATE SERVICE        REASON  VERSION
80/tcp   open  http           syn-ack Apache httpd
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache
| http-title: Ayto_Guarroman &#8211; Pagina Principal del Ayuntamiento de Gu...
|_Requested resource was http://172.29.230.161/webguarroman/
|_http-generator: WordPress 4.7.33
|_http-favicon: Unknown favicon MD5: 3A3BC0025057AA424AE742581D3C2B15
443/tcp  open  http           syn-ack Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: 403 Forbidden
5001/tcp open  commplex-link? syn-ack
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.0.1 Python/3.12.3
|     Date: Tue, 19 May 2026 07:51:20 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 50259
|     Connection: close
|     ...
```

![CapturaHTMLPorts.png](Ataque%20Carlos%20Pau%20Jolu/CapturaHTMLPorts.png)

Con esto podemos ver la página web principal del ayuntamiento, corriendo en http://172.29.230.161/webguarroman/

![imagen.png](Ataque%20Carlos%20Pau%20Jolu/imagen%204.png)

Le ejecutamos un gobuster para encontrar posibles directorios vulnerables:

```jsx
jose@ubuntu:~$ gobuster dir -u http://172.29.230.161/ --wordlist /usr/share/wordlist/dirbuster-wordlist/directory-list-2.3-medium.txt --exclude-length 954
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.29.230.161/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlist/dirbuster-wordlist/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] Exclude Length:          954
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/phpmyadmin           (Status: 301) [Size: 241] [--> http://172.29.230.161/phpmyadmin/]
Progress: 220560 / 220561 (100.00%)
===============================================================
Finished
===============================================================
jose@ubuntu:~$
```

Encontramos el directorio phpmyadmin.

A partir de aqui, Carlos procede a acceder a la web [http://172.29.230.161/phpmyadmin](http://172.29.230.161/phpmyadmin) a ver qué encuentra. Encontramos el panel de login de phpmyadmin expuesto.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image.png)

Para hacer el ataque más realista, hemos pedido al equipo de Benimerda las credenciales que han obtenido mediante OSINT, de las cuáles tienen todas menos las de concejal.guarroman, funcionario1guarroman y funcionario4guarroman.

A excepción de estas 3 cuentas, hemos probado con todas nuestras credenciales para probar a acceder (como se acordó).

Al primer intento, probando con user: funcionario2guarroman y pass: MiaNube98Trini hemos conseguido acceder al panel de phpmyadmin. Es una cuenta que solo tiene permisos de lectura, por lo que habrá que buscar otra cuenta que tenga permisos de administrador.

Desconocemos cuál podría ser, pero identificamos una tabla llamada wp_users con las contraseñas usables en wordpress:

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%201.png)

Pero con los hashes de las contraseñas cifrados con bcrypt no podemos hacer gran cosa si no sabemos la contraseña original. Es bastante improbable que las contraseñas se puedan romper con hashcat, ya que por el patrón que tienen nuestras contraseñas, es raro que aparezca alguna de ellas en algún diccionario conocido.

Si prestamos atención, encontramos una tabla llamada wp_pass. Aqui vemos una tabla con las contraseñas en texto plano (wp_pass).

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%202.png)

Con estas credenciales intentamos entrar a el webguarroman/login.php, y después de probar con varios usuarios damos con el que es valido: funcionario1guarroman.
Una vez dentro vamos a ejecutar un ataque ya estudiado, vamos a instalar un plugin vulnerable llamado “File Manager” a través del cuál tendremos acceso a ver el sistema de archivos del sitio web. 

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%203.png)

En él también tenemos la posibilidad de subir /modificar un archivo de la web, por lo que intentaremos subir y ejecutar una revshell.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%204.png)

Con la revShell subida al servidor, cuando un usuario acceda a http://172.29.230.161/index.php, el archivo se interpretará y se ejecutará la revShell.

Solo queda ponerse en escucha por el puerto 1234 y…

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%205.png)

Se ha ejecutado la revShell correctamente. Aquí se muestra el usuario con el que hemos accedido y información básica inicial:

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%206.png)

Gracias al escaneo de nmap previo que hemos hecho, sabemos que el servidor tiene python3 instalado. Probamos a ver si el binario es ejecutable con el usuario “daemon”.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%207.png)

Y vemos que es la misma versión que hemos obtenida del escaneo de nmap.

Al ver que podemos ejecutar código python, con el siguiente código, podemos ejecutar una /bin/bash, la cual es mucho más estable que sh:

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%208.png)

Intento excalar privilegios desde este usuarios con linPEAS pero no tenemos permisos para poder hacerlo.

[PEASS-ng/linPEAS at master · peass-ng/PEASS-ng](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS)

![image.png](Ataque%20Carlos%20Pau%20Jolu/13ee49ae-cb7b-491a-bf8c-cb2ac3c03f4e.png)

Y ahora viendo que no funciona, intento explotar una vulnerabilidad llamada CopyFail, que esta en todos los sistemas Linux desde 2017, que consiste en un explotación de la paginación de la memoria.

[Copy Fail — 732 Bytes to Root](https://copy.fail/#exploit)

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%209.png)

Copy fail no funciona.
Veo el contenido de `/etc/passwd` .

![image.png](Ataque%20Carlos%20Pau%20Jolu/605f38e7-7da8-49c7-8418-9155ca84d5d2.png)

Viendo que existe en funcionario1guarroman pruebo a cambiar a ese usuario reutilizando la contraseña.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2010.png)

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2011.png)

Y viendo que tengo permisos ALL y grupo de sudo, intento escalar a root.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2012.png)

Y veo que ya soy root.

ATAQUE A EL AYT BENIMERDA (por fin)

Escaneo de su maquina.

```jsx
nmap -sC -sV -p 22,80,443 -sS --open -vvv --disable-arp-ping 172.29.230.171
```

```jsx
80/tcp  open  http     syn-ack ttl 63 Apache httpd 2.4.46 ((Unix) OpenSSL/1.1.1h PHP/7.2.34 mod_perl/2.0.11 Perl/v5.32.0)
|_http-generator: WordPress 4.7.29
|_http-server-header: Apache/2.4.46 (Unix) OpenSSL/1.1.1h PHP/7.2.34 mod_perl/2.0.11 Perl/v5.32.0
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Benimerda &#8211; Just another WordPress site
443/tcp open  ssl/http syn-ack ttl 64 Apache httpd
| http-title: 403 Forbidden
|_Requested resource was https://172.29.230.171/cgi-bin/main.cgi
| tls-alpn: 
|_  http/1.1
|_http-server-header: Apache
| ssl-cert: Subject: commonName=127.0.0.1
| Issuer: commonName=127.0.0.1
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2026-04-28T06:51:03
| Not valid after:  2027-04-28T06:51:03
| MD5:     8e0b 63c9 3d0b 8d9d da96 2b3d 86a8 bca4
| SHA-1:   1926 5818 f52c 6114 d89d e07d 2283 64d2 1755 b754
| SHA-256: 0b4c 2ef6 a241 777a ee45 dcd1 14a9 8365 a1a7 a885 58c8 56e9 d806 948b bd65 53c4
| -----BEGIN CERTIFICATE-----
| MIIDCTCCAfGgAwIBAgIUeLciEQunuWhRU5+fsnYM9QL9E3kwDQYJKoZIhvcNAQEL
| BQAwFDESMBAGA1UEAwwJMTI3LjAuMC4xMB4XDTI2MDQyODA2NTEwM1oXDTI3MDQy
| ODA2NTEwM1owFDESMBAGA1UEAwwJMTI3LjAuMC4xMIIBIjANBgkqhkiG9w0BAQEF
| AAOCAQ8AMIIBCgKCAQEA20eQN142mxpEH8U1C5kbJPc00B1aQmlSNqpNm7YDOQMB
| jknL0rgDiKzRqPgKyBjQrKletXAmY8arcFFM17mJtrgxaH3d9L/AycBXyKm5RkYW
| HL4+aJYZTxpy1Ptwvow9CtrNYZGI1LKovgLGCy+j8L+FN0eWmEcBleljvsE3qSUe
| SRr11aj2cmlG/EtJDpQwr6PywclK9o+FnA6s5nB+47UHNwriIXJ8CDfxxwD0+4i4
| mIk/m2rGX9ahTDlTsHu3WKhwWKIiyGikjg933EtXaX+Bn35dOB2oz4o4L2APE556
| DvVBCIYL8MkfKwBNAMH7Ire+lpfWgu6hp+UtcLuCJQIDAQABo1MwUTAdBgNVHQ4E
| FgQU5EWGaU5prc5AZC2N3roywLTBsfQwHwYDVR0jBBgwFoAU5EWGaU5prc5AZC2N
| 3roywLTBsfQwDwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAwEJU
| uRhslcSDDkwKHr8FSLXmYf1Vwj0HrG0xyaAFHibHc3FnRqNpL/2qMynbPqyuG5BE
| i5IyZJ8W42fvm1bTZNpNvjXwY9DLb2i/LmV4akYQsxKEiKhyYI5/STkCcvQo4+9u
| g3CJfcqBuLQ6NgdGTOvs0QUQz9vyeWaYsF9ETgDQaH/qnbCtHmYfcLUFYpHNISjX
| syDhN5ckdIZnh987U9IHfvBwTASzQwBihs3RkbW+lmLtU7aLS+tfAOtpVYAQ1oZE
| eS2p6NbiTfsoBpc5WbL78BNAzi75XciZfn1R4H/o5mvUG9ycKb3jJ8hOUF9x+l8C
| SjlvRkJWZrC83+xeAw==
|_-----END CERTIFICATE-----
|_ssl-date: TLS randomness does not represent time
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
MAC Address: 00:00:40:01:1D:F0 (Applicon)
```

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2013.png)

Sabiendo que es un wordpress, accedo al login.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2014.png)

Con su funcionario1, logro acceder.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2015.png)

Añadimos el plugin de “FileManager”.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2016.png)

Con este plugin, a parte de ver los ficheros del wordpress, tenemos la posibilidad de subir/modificar un archivo de la web, por lo que intentaremos subir y ejecutar una revshell.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2017.png)

Modificamos el `index.php` para subir la revshell.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2018.png)

Me pongo a escuchar por ese puerto.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2019.png)

Cargamos el recurso desde el navegador y ya tenemos la shell.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2020.png)

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2021.png)

Estando en una sh y sabiendo que tienen `python` , me cargo una bash.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2022.png)

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2023.png)

Miramos que permisos tiene este usuario, pero vemos que no tiene permisos.

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2024.png)

Intentamos pivotar mirando el fichero `passwd` para saber que usuarios tienen, pero vemos que no tienen funcionario, entronces sabiendo el formato de contraseñas que usan que es nombre del `[usuario]+#+[numPC]` .

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2025.png)

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2026.png)

![image.png](Ataque%20Carlos%20Pau%20Jolu/image%2027.png)