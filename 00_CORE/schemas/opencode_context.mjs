// Integración opcional de OpenCode 1.19.4; sin dependencias ni escrituras.
import fs from 'node:fs/promises';
import path from 'node:path';

const headers = new Set(['> [!info]- Índice de esta nota (líneas)', '> [!info] Índice de esta nota (líneas)']);
const entry = /^> - Líneas \d+–\d+: .+$/;
const credit = /^> \*\*(?:Crédito principal|Main credit|Besonderer Dank|主要致谢)/;

function fenceAfter(text, fence) {
  for (const line of text.split(/\r?\n/)) {
    const mark = /^ {0,3}(`{3,}|~{3,})(.*)$/.exec(line);
    if (!mark) continue;
    if (fence) {
      if (mark[1][0] === fence[0] && mark[1].length >= fence.length && !mark[2].trim()) fence = null;
    } else if (mark[1][0] !== '`' || !mark[2].includes('`')) fence = mark[1];
  }
  return fence;
}

function withoutIndex(text, numbered = false) {
  const lines = text.match(/[^\n]*\n|[^\n]+$/g) || [];
  const value = i => {
    let line = (lines[i] || '').replace(/\r?\n$/, '');
    if (numbered) line = line.replace(/^\d+: ?/, '');
    return line.replace(/^\ufeff/, '');
  };
  let start = 0;
  if (value(0) === '---') {
    start = 1;
    while (start < lines.length && value(start) !== '---') start++;
    if (start === lines.length) return text;
    start++;
  } else if (credit.test(value(0))) {
    start = 1;
  }
  while (start < lines.length && !value(start).trim()) start++;
  if (!headers.has(value(start))) return text;
  let end = start + 1;
  while (end < lines.length && entry.test(value(end))) end++;
  // Sin separador final puede ser un fragmento de read: conservarlo íntegro.
  if (end === start + 1 || end === lines.length || value(end).trim()) return text;
  return lines.slice(0, start).concat(lines.slice(end)).join('');
}

function relativeFile(value) {
  if (typeof value !== 'string' || !value || /[\\:*?\x00-\x1f]/.test(value) || path.isAbsolute(value)) throw new Error('readPaths requiere archivos relativos explícitos.');
  const parts = value.split('/');
  if (parts.some(part => !part || part === '.' || part === '..' || /[. ]$/.test(part) || /^(CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])(\.|$)/i.test(part))) {
    throw new Error('Ruta no portable en readPaths.');
  }
  return value;
}

const key = value => process.platform === 'win32' ? value.toLowerCase() : value;
const inside = (root, target) => {
  const relative = path.relative(root, target);
  return relative && relative !== '..' && !relative.startsWith('..' + path.sep) && !path.isAbsolute(relative);
};

export default async function genesisContext({ directory }, options = {}) {
  const root = path.resolve(directory);
  const restricted = Object.hasOwn(options, 'readPaths');
  let allowed;
  if (restricted) {
    if (!Array.isArray(options.readPaths) || !options.readPaths.length) throw new Error('readPaths no puede estar vacío.');
    allowed = new Map(options.readPaths.map(value => {
      const target = path.resolve(root, relativeFile(value));
      return [key(target), target];
    }));
  }

  async function authorize(filePath) {
    if (typeof filePath !== 'string' || filePath.split(/[\\/]/).includes('..')) throw new Error('Consulta: ruta rechazada.');
    const target = path.resolve(root, filePath);
    if (!inside(root, target) || !allowed.has(key(target))) throw new Error('Consulta: archivo fuera de la lista autorizada.');
    for (let current = target; ; current = path.dirname(current)) {
      const info = await fs.lstat(current);
      if (info.isSymbolicLink()) throw new Error('Consulta: no seguir enlaces ni junctions.');
      if (key(current) === key(root)) break;
    }
    const realRoot = await fs.realpath(root);
    const realTarget = await fs.realpath(target);
    if (!inside(realRoot, realTarget) || !(await fs.stat(target)).isFile()) throw new Error('Consulta: destino no autorizado.');
  }

  const hooks = {
    'experimental.chat.system.transform': async (_, output) => {
      const filtered = [];
      for (const text of output.system) {
        // OpenCode identifica los documentos precargados con esta procedencia.
        const chunks = text.split(/(^Instructions from: [^\r\n]+\r?\n)/m);
        let fence = fenceAfter(chunks[0], null);
        for (let i = 1; i < chunks.length; i += 2) {
          const source = chunks[i].replace(/^Instructions from: /, '').trim();
          if (restricted) await authorize(source);
          const original = chunks[i + 1];
          if (!fence && /\.md$/i.test(source)) chunks[i + 1] = withoutIndex(original);
          fence = fenceAfter(original, fence);
        }
        filtered.push(chunks.join(''));
      }
      // OpenCode conserva la referencia del array: reasignarla no cambia la petición.
      output.system.splice(0, output.system.length, ...filtered);
    },
    'tool.execute.after': async (input, output) => {
      if (input.tool !== 'read' || typeof input.args?.filePath !== 'string' || !/\.md$/i.test(input.args.filePath)) return;
      if (Object.hasOwn(input.args, 'offset') || Object.hasOwn(input.args, 'limit')) return;
      const match = /^([\s\S]*?<content>\r?\n)([\s\S]*?)(<\/content>[\s\S]*)$/.exec(output.output);
      if (match) output.output = match[1] + withoutIndex(match[2], true) + match[3];
    },
  };
  if (restricted) {
    hooks.config = async config => {
      for (const source of config.instructions || []) {
        if (typeof source !== 'string' || !allowed.has(key(path.resolve(root, source))) || /[:*?]/.test(source)) {
          throw new Error('Consulta: precarga fuera de la lista autorizada.');
        }
      }
      const permission = { '*': 'deny', external_directory: 'deny', read: { '*': 'deny' } };
      for (const target of allowed.values()) {
        // V1 pide permisos con rutas relativas al worktree; el hook verifica además la ruta real.
        permission.read[path.relative(root, target)] = 'allow';
        permission.read[path.relative(root, target).replaceAll('\\', '/')] = 'allow';
        permission.read[target] = 'allow';
      }
      config.permission = permission;
      for (const agent of Object.values(config.agent || {})) agent.permission = permission;
    };
    hooks['tool.execute.before'] = async (input, output) => {
      if (input.tool !== 'read') throw new Error('Consulta: herramienta bloqueada.');
      await authorize(output.args?.filePath);
    };
  }
  return hooks;
}
