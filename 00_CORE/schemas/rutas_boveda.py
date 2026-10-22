#!/usr/bin/env python3
"""Raíz de bóveda y comprobación de rutas sin seguir enlaces. Python estándar 3.8+."""
import os
from pathlib import Path
import stat

# Marcas de una bóveda del kit: el ancestro más externo que las tiene es el límite de la revisión.
_MARCAS = ('INDICE.md', '00_CORE/atoms/00_vault-rules.md')


def es_enlace(info):
    """Symlink, junction u otro enlace de Windows (etiqueta de tipo name surrogate)."""
    if stat.S_ISLNK(info.st_mode):
        return True
    if getattr(info, 'st_file_attributes', 0) & 0x400:
        tag = getattr(info, 'st_reparse_tag', None)
        # Nube, deduplicación o compresión no redirigen; 0 es un reanálisis que lstat ya atravesó.
        return tag is None or bool(tag & 0x20000000)
    return False


def raiz_boveda(path):
    """Ancestro más externo con las marcas del kit, o None si no hay una bóveda reconocible."""
    path = Path(os.path.abspath(str(path)))
    raiz = None
    for part in (path,) + tuple(path.parents):
        # INDICE.md primero: la mayoría de los ancestros no lo tienen y basta una consulta.
        if (part / _MARCAS[0]).is_file() and (part / _MARCAS[1]).is_file():
            raiz = part
        # Un checkout en .claude/worktrees es una copia propia, no una parte de la bóveda que lo contiene.
        if part.parent.name.casefold() == 'worktrees' and part.parent.parent.name.casefold() == '.claude':
            break
    return raiz


def ruta_real(path, raiz=None):
    """Rechazar enlaces desde la ruta hasta la raíz de la bóveda, inclusive; sin raíz, hasta el disco."""
    path = Path(os.path.abspath(str(path)))
    raiz = raiz_boveda(path) if raiz is None else Path(os.path.abspath(str(raiz)))
    tope = os.path.normcase(str(raiz)) if raiz is not None else None
    for part in (path,) + tuple(path.parents):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if es_enlace(info):
            raise ValueError('No seguir enlaces ni junctions: ' + str(part))
        if os.path.normcase(str(part)) == tope:
            break
    return path
