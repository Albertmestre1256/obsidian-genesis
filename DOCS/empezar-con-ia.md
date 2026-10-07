# Dale la carpeta a tu IA

El kit está pensado para que la IA prepare tu bóveda con tus respuestas. Una bóveda es una carpeta de notas que después abrís con Obsidian.

## Lo que hacés vos

1. Descargá el ZIP del repositorio y descomprimilo.
2. Abrí o seleccioná esa carpeta como carpeta de trabajo en un asistente que pueda leer y editar archivos. Elegí la que contiene `AI-INSTRUCTIONS.md`. Podés usar, por ejemplo, Codex o Claude Code si ya los usás. No necesitás una cuenta adicional por el kit.
3. Pegá este mensaje:

> Quiero que configures mi bóveda de Obsidian con este kit. Leé primero `00_CORE/atoms/00_vault-rules.md` y después `AI-INSTRUCTIONS.md`. Guiame con preguntas simples, de a una o dos por vez. No sé usar Obsidian: encargate vos de crear los archivos según mis respuestas. Antes de escribir, aclarame en qué carpeta vas a trabajar. Si no tenés acceso a ella, decímelo.

No hace falta abrir Obsidian todavía. La IA te preguntará qué querés organizar y si empezás de cero o tenés notas que conservar. Después te ayudará a definir un primer proyecto y su próximo paso. No necesitás elegir plantillas ni entender propiedades.

Podés responder «todavía no sé» o «no tengo una fecha». La IA te ofrecerá ideas sin inventar decisiones por vos. Si interrumpís la conversación, al volver decile «seguí con la configuración»: debe revisar lo guardado y retomar donde quedó. Cuando ya esté lista, podés pedir «sigamos con mi proyecto».

## Qué deberías recibir

- La carpeta de la bóveda preparada con las reglas del kit.
- Tu primer proyecto con una ficha que resuma objetivo y próximo paso.
- Un acceso a ese proyecto desde el Panel.
- Una explicación corta de cómo abrirlo y empezar a trabajar.

Si ya tenés una bóveda, dale acceso a esa carpeta también y aclará cuál es el destino. La IA debe conservar tus notas, reglas y ajustes; si hay archivos incompatibles, te explicará qué decisión falta.

## Si tu chat solo acepta adjuntos

Subir un ZIP no concede acceso a la carpeta de tu computadora. Si ese chat puede leer el ZIP y generar archivos, puede entregarte una copia configurada para descargar. Después descomprimís esa copia y la abrís como bóveda.

Si solo puede responder texto, puede hacerte las preguntas y preparar el contenido, pero no completar la instalación. Para que se encargue de los archivos, usá un asistente con acceso a la carpeta. Si preferís hacerlo vos, está la [alternativa manual](primer-proyecto.md).

## Cómo se orienta el asistente

El kit incluye `AGENTS.md` y `CLAUDE.md`, que remiten al mismo procedimiento en `AI-INSTRUCTIONS.md`. En Claude Code también podés pedir `/configurar`. Otros asistentes pueden seguir el mensaje anterior leyendo los archivos indicados. La carga automática depende del producto y su configuración.

Referencias de los puntos de entrada: [AGENTS.md en Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md) y [CLAUDE.md en Claude Code](https://code.claude.com/docs/en/memory). Las instrucciones orientan al asistente; no otorgan permisos de acceso.
