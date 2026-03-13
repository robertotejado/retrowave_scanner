# retrowave_scanner
escáner en Python (Tkinter + Nmap + Nping)

# 🌴🕶️ RETROWAVE ICS & IT SECURITY SCANNER 📼✨

¿Estás cansado de que tus auditorías de red parezcan un aburrido documento de texto plano? ¿Quieres buscar vulnerabilidades en un PLC industrial mientras te sientes como Ryan Gosling conduciendo de noche en *Drive*? **Has llegado al repo indicado.**

Este proyecto es una interfaz gráfica (GUI) desarrollada en Python (Tkinter) que actúa como un *wrapper* vitaminado para **Nmap**, **Nping** y **Netcat**. Está diseñado específicamente para identificar y auditar protocolos tanto de entornos **IT** (Sistemas de Información) como **OT / ICS** (Sistemas de Control Industrial), todo envuelto en una gloriosa paleta de colores neón cian y magenta.

---

## 🚀 ¿Qué hace esta maravilla? (Features)

* **Aesthetic UI:** Colores neón, fuentes retro y botones que dan ganas de pulsar fuerte. Todo asíncrono gracias a `threading` (¡la interfaz no se congela mientras escaneas!).
* **Escaneo IT con *Esteroides*:** No solo busca si el puerto está abierto, sino que lanza scripts automatizados de Nmap según el protocolo:
* `FTP (21)`: Busca accesos anónimos y backdoors conocidos (vsftpd, proftpd).
* `SSH (22)`: Enumera algoritmos y métodos de autenticación.
* `HTTP/HTTPS (80/443)`: Enumera directorios, busca inyecciones SQL y revisa vulnerabilidades SSL (hola, Heartbleed 💔).
* `RDP (3389)`: Revisa cifrado y vulnerabilidades críticas (como ms12-020).


* **Ataques de Precisión OT (Industrial):** Aquí es donde la cosa se pone seria. Si seleccionas protocolos industriales, la herramienta baja al barro:
* `Modbus (502) & S7 (102)`: Usa Nmap (`s7-info`, `modbus-discover`) y luego inyecta un payload hexadecimal específico con `nping` (`000100000006010600010002`) para forzar una respuesta del PLC.
* `OPC UA (4840)`: Lanza peticiones TCP crudas y envía el paquete "HEL" vía Netcat para interactuar con el endpoint.


* **Auto-Logging:** Todo lo que escupe la consola se guarda automáticamente en un archivo `.log` con la fecha y hora. Porque los hackers *aesthetics* también tienen que redactar informes al final del día. 📝
* **Botón de Pánico (ABORT OPERATION):** Por si acaso ves que estás escaneando la IP de la NSA por error. Detiene todos los subprocesos de golpe.

---

## 🛠️ Requisitos Previos (Prerequisites)

Para que esta máquina del tiempo funcione, tu sistema necesita algunas herramientas instaladas a nivel de sistema operativo:

1. **Python 3.x** y la librería `tkinter` (suele venir preinstalada en Windows, en Linux puedes necesitar `sudo apt install python3-tk`).
2. **Nmap:** El rey indiscutible del escaneo.
3. **Nping:** Normalmente se instala junto con Nmap.
4. **Netcat (`nc`):** La navaja suiza de las redes.

**💡 Nota para usuarios de Linux:** El script invoca `sudo` para `nping` porque la inyección de paquetes a bajo nivel requiere privilegios de root. ¡Asegúrate de correr el script desde una cuenta con permisos o prepárate para meter la contraseña en la terminal de fondo! (En Windows, el script omite el `sudo` automáticamente).

---

## 💻 Instalación y Uso

1. Clona este repositorio para robarme el código (es broma, es Open Source):
```bash
git clone https://github.com/robertotejado/retrowave_scanner.git
cd retrowave-scanner

```


2. Ejecuta el script:
```bash
python3 retrowave_scanner.py

```


3. Introduce tu objetivo (Ej: `192.168.1.30` o `10.0.0.0/24`), marca tus casillas como si estuvieras en los 80s y dale a **INITIATE NEON SCAN**.
4. Ponte unas gafas de sol (opcional, pero fuertemente recomendado) y observa la lluvia de paquetes.

---

## ⚠️ Disclaimer (El momento aguafiestas)

**Por favor, usa el sentido común.** Este software automatiza el envío de paquetes de red y payloads de descubrimiento industrial. Escanear redes y, sobre todo, equipos OT/ICS de los que no eres propietario (o no tienes autorización explícita y por escrito para auditar) es **ILEGAL**.

Además, los entornos industriales (PLCs, RTUs, SCADAs) son extremadamente frágiles. Lanzar un Nmap agresivo o inyectar paquetes malformados puede causar una Denegación de Servicio (DoS), tirar abajo una línea de producción, o peor.

*El creador de este script no se hace responsable si terminas en una prisión federal o si accidentalmente apagas una turbina en una planta eléctrica. Úsalo solo en CTFs, laboratorios propios o entornos controlados.* 👨‍⚖️

---

*Stay Radical. Hack the Planet.* 👾

---
 
