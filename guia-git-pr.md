# Guía de Trabajo: Ramas (Branches) y Pull Requests (PRs)

Trabajar con ramas (branches) y *Pull Requests* (PRs) es el estándar en la industria para colaborar en proyectos de software.

# Objetivo
La idea principal es que **nunca trabajes directamente sobre la rama principal** (`main`), sino que crees un entorno aislado (un *branch*) para hacer tus cambios de forma segura.
Posteriormente se suben a github para ser revisados por otros compañeros mediante *Pull Requests* para asegurar que no haya conflictos con los trabajos de otros compañeros.

## ¿Por qué usar Pull Requests en primer lugar?
En un proyecto conjunto con varias personas, si todos escribieran directamente en `main`, el código se volvería caótico rápidamente: los errores pasarían a producción sin filtros y nadie sabría exactamente qué ha modificado su compañero.

El **Pull Request (PR)** es, literalmente, una "Petición de Integración". Es una manera de decirle al equipo: *"He terminado esta tarea en mi entorno aislado. Aquí está el código. Revisadlo, comentad si hay errores y, si está todo correcto, dadme permiso para integrarlo en el proyecto principal"*.<br><br>
Es, básicamente, un mecanismo de control.

### Pull Request (GitHub) vs. `git merge` (Local)
Hay 2 formas de juntar el código de tu entorno aislado junto con el código "en producción":

- La primera es, directamente en local, hacer lo que se conoce como un **`git merge`:** Une dos ramas en tu ordenador LOCAL de forma inmediata.
<br><br>
Te da la posibilidad de, antes de fusionarlas, comprobar conflictos que puedan haber con los cambios realizados en local, pero nadie es conocedor de estos cambios, salvo la persona que esté trabajando con esa rama en ese momento. Si haces un merge a `main` y haces push a github, el cambio es definitivo.

> [!WARNING]
> No hay paso intermedio de revisión por parte del resto del equipo. Se pide **NO USAR** esta función, solo se explica como dato informativo.

- La segunda opción es mediante un **Pull Request:** No es un comando de Git persé, es una característica de plataformas como GitHub.
<br><br>
Antes de fusionar las ramas, se hace una solicitud que puede ser revisada por el resto del equipo para ver qué ha cambiado. Especialmente útil para que no haya conflicto si 2 personas modifican el mismo fichero.
Básicamente, **lo pausa** en una interfaz web amigable donde el equipo puede ver un "Antes y Después" del código, dejar comentarios línea por línea, y requerir aprobaciones explícitas antes de que el merge ocurra realmente.<br><br>
Cuando el request es aceptado, simplemente se hace un `git merge` por debajo.

> [!WARNING]
> Para esta opción, es necesario subir previamente los cambios a github.

---

## Fase 1: Preparación (Partir de una base limpia)

Antes de crear tu nueva rama, debes asegurarte de que tu rama principal local está sincronizada.

**1. Cambia a la rama principal:**
```bash
git switch main
```

**2. Descarga tus últimos cambios de la rama actual:**
```bash
git pull
```
> [!NOTE]
> `git pull` solo actualiza la rama en la que estás actualmente (`main`). No descarga las diferentes ramas en las que puedan estar trabajando tus compañeros. Si necesitas ver las ramas de otros, usarías `git fetch --all`.

---

## Fase 2: Crear tu nueva rama de trabajo

Ahora creas una copia aislada donde harás tu trabajo.<br>
Asegúrate de ponerle un **nombre distinguible** y que refleje el cambio que quieres hacer.<br>
> [!IMPORTANT]
> Los cambios deberían de ser sustanciales (no solo cambiar un par de líneas) pero tampoco se deben de alargar mucho en el tiempo (preferiblemente, que se puedan acabar el mismo día).<br><br>Ese es el baremo recomendado a seguir para establecer el nombre de la rama.<br><br>

Algunos ejemplos podrían ser:
- feat/telegram-bot
- fix/wazuh-alerts
- refactor/iptables-rules
- docs/modifyReadme


**3. Crea y muévete a la nueva rama:**
```bash
# Recuerda sustituir docs/ por lo que sea más conveniente dependiendo del cambio
git branch docs/modifyReadme
git switch docs/modifyReadme
```

---

## Fase 3: Trabajar y guardar tus cambios

En este punto, estás en tu burbuja aislada.<br>
Modifica los documentos a tu antojo en base al cambio que has definido que vas a hacer al crear la rama.<br>
Cuando estés listo para subirlos a github:

**4. Añade los archivos al "área de preparación" (Staging):**
```bash
git add .
```
> [!IMPORTANT]
> El comando `git add .` añade todos los archivos modificados o creados en el directorio actual. Sin embargo, **es inteligente**: ignora automáticamente cualquier archivo o carpeta que esté especificado dentro del archivo `.gitignore`. Si usas `git add .`, no tienes que preocuparte por subir archivos temporales o compilados por accidente, siempre que el `.gitignore` esté bien configurado.

> [!TIP]
> **¿Has añadido algo por error?** Si ejecutas `git add .` y te das cuenta de que has metido un archivo que no tocaba, puedes sacarlo del "área de preparación" ejecutando: `git restore --staged nombre-archivo`.

**5. Guardas los cambios creando un "Commit" (Convención de Commits):**
Es obligatorio seguir la estructura *Conventional Commits*: `<tipo>: <descripción del cambio>`.
```bash
git commit -m "docs: added git and pull request workflow guide"
```
Ejemplos de prefijos comunes:
*   `feat:` (Nueva característica o funcionalidad)
*   `fix:` (Solución de un error o bug)
*   `docs:` (Cambios exclusivos de documentación)
*   `style:` (Cambios de formato, espacios, que no afectan al código)

---

## Fase 4: Subir tu rama y preparar el Pull Request

Tus cambios están guardados en tu ordenador. Tienes que enviarlos a GitHub.

**6. Sube tu rama al servidor remoto:**
```bash
git push -u origin docs/modifyReadme
```
> [!NOTE]
> **¿Qué hace el `-u`?**
> El flag `-u` significa `--set-upstream`. Lo que hace es vincular tu rama local (`docs/modifyReadme`) con la rama equivalente que se acaba de crear en el servidor de GitHub. Es importante porque le enseña a Git dónde tiene que mirar a partir de ahora. Gracias al `-u`, las próximas veces que quieras subir o bajar cambios en esta rama, te bastará con escribir simplemente `git push` o `git pull`, sin necesidad de especificar el nombre del remoto ni de la rama.

**7. Crear el Pull Request (PR):**
Ve a GitHub. Usa el botón "Compare & pull request" para solicitar la fusión con `main`.

> [!WARNING]
> **Ojo con los conflictos (Merge Conflicts):** Si tú y otro compañero habéis modificado exactamente la misma línea de código en el mismo archivo, GitHub bloqueará el botón verde de "Merge pull request". Te avisará de que hay un conflicto y te obligará a decidir con qué versión te quedas (o a fusionarlas manualmente en local) antes de dejarte continuar.

---

## Fase 5: Limpieza (Post-Merge)

> [!WARNING]
> Si el PR va a tardar en poder ser revisado, puedes saltarte el **paso 11** que viene a continuación.
> Mientras esperas a que se apruebe el PR, puedes crear una nueva feature volviendo al **paso 2**.

Una vez que tu PR ha sido aprobado y fusionado en `main` desde GitHub, tu rama de trabajo ya ha cumplido su propósito y es "basura". Hay que limpiar tanto el servidor de GitHub como tu ordenador.

**8. Borra la rama remota en GitHub:**
Justo después de pulsar el botón verde de "Merge pull request" en la web de GitHub, aparecerá un botón morado que dice **"Delete branch"**. Púlsalo siempre. Esto elimina la rama del servidor remoto (github) para que no se acumulen cientos de ramas finalizadas en el proyecto.

**9. Vuelve a la rama principal local (en tu PC):**
```bash
git switch main
```

**10. Actualiza tu main local:**
```bash
git pull origin main
```

**11. Borra tu rama local:**
```bash
git branch -d docs/modifyReadme
```

**12. Limpia y actualiza las ramas remotas en tu PC:**
```bash
git fetch --prune
```
Este comando tiene una doble función vital: por un lado, limpia tu ordenador eliminando las referencias locales a ramas que ya borraste en el paso 8 en GitHub; y por otro, **descarga todas las ramas nuevas que hayan creado tus compañeros**. 
Al finalizar este paso 12, tendrás en tu ordenador la versión más actualizada de todo el código y de todas las ramas, dejándote en la posición perfecta para volver al Paso 1 y empezar una nueva *feature* en ese mismo momento.

---

## Resumen Rápido (Cheat Sheet)

```bash
# 1. Empieza desde main actualizado
git switch main
git pull origin main

# 2. Crea tu rama y trabaja
git branch feat/mi-nueva-tarea
git switch feat/mi-nueva-tarea
git add .
git commit -m "feat: descripción clara del cambio"

# 3. Sube y crea PR
git push -u origin feat/mi-nueva-tarea
# -> Vas a GitHub, creas el PR y se fusiona

# 4. Limpieza final (Post-Merge)
git switch main
git pull origin main
git branch -d feat/mi-nueva-tarea
git fetch --prune
```
