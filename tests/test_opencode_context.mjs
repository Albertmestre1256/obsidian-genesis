import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import plugin from '../00_CORE/schemas/opencode_context.mjs';

const index = '> [!info]- Índice de esta nota (líneas)\n> - Líneas 1–3: Este índice\n> - Líneas 5–6: Nota\n';
const body = '\n# Nota\nContenido conservado.\n';
const properties = '---\ntipo: apunte\n---\n';

async function system(text) {
  const hooks = await plugin({ directory: process.cwd() });
  const output = { system: [text] };
  await hooks['experimental.chat.system.transform']({}, output);
  return output.system[0];
}

test('filtra documentos precargados, conserva propiedades y el resto del sistema', async () => {
  const prefix = 'Instrucciones del agente.\nInstructions from: /vault/Nota.md\n';
  assert.equal(await system(prefix + properties + index + body), prefix + properties + body);
});

test('filtra varios documentos y conserva sus rutas y encabezados', async () => {
  const first = 'Instructions from: /vault/Uno.md\n';
  const second = 'Instructions from: /vault/Dos.md\n';
  assert.equal(await system(first + index + body + second + index + body), first + body + second + body);
});

test('muta el array del llamador, como requiere OpenCode', async () => {
  const hooks = await plugin({ directory: process.cwd() });
  const list = ['Instructions from: /vault/Nota.md\n' + index + body];
  const output = { system: list };
  await hooks['experimental.chat.system.transform']({}, output);
  assert.equal(output.system, list);
  assert.ok(!list[0].includes('Índice de esta nota'));
});

test('no altera un ejemplo de procedencia dentro de un bloque de código', async () => {
  const example = '\n```md\nInstructions from: /ejemplo/Nota.md\n' + index + body + '```\n';
  const prefix = 'Instructions from: /vault/Nota.md\n';
  assert.equal(await system(prefix + index + body + example), prefix + body + example);
});

for (const [name, text] of [
  ['otro aviso info', '> [!info] Aviso propio\n> Información útil.\n'],
  ['ejemplo en código', '```md\n' + index + '\n```\n'],
  ['índice incompleto', index.trimEnd()],
  ['entrada incompatible', '> [!info]- Índice de esta nota (líneas)\n> Otro texto.\n\n'],
  ['propiedades sin cierre', '---\ntipo: apunte\n' + index + body],
  ['texto sin procedencia', index + body],
]) {
  test('conserva ' + name, async () => {
    const prefix = name === 'texto sin procedencia' ? '' : 'Instructions from: /vault/Nota.md\n';
    assert.equal(await system(prefix + text), prefix + text);
  });
}

test('conserva BOM, CRLF, título y avisos después del índice', async () => {
  const prefix = 'Instructions from: C:\\Vault\\Nota.md\r\n';
  const suffix = '\n> [!info] Aviso propio\n> No quitar.\n';
  const text = '\ufeff' + properties + index + body + suffix;
  const expected = '\ufeff' + properties + body + suffix;
  assert.equal(await system(prefix + text.replaceAll('\n', '\r\n')), prefix + expected.replaceAll('\n', '\r\n'));
});

test('read conserva los números de las líneas originales y la metadata', async () => {
  const hooks = await plugin({ directory: process.cwd() });
  const original = (properties + index + body).split('\n').map((line, i) => `${i + 1}: ${line}`).join('\n');
  const output = { output: '<path>/vault/Nota.md</path>\n<content>\n' + original + '\n</content>', metadata: { original: true } };
  await hooks['tool.execute.after']({ tool: 'read', args: { filePath: '/vault/Nota.md' } }, output);
  assert.ok(output.output.includes('1: ---\n2: tipo: apunte\n3: ---'));
  assert.ok(output.output.includes('8: # Nota\n9: Contenido conservado.'));
  assert.ok(!output.output.includes('Índice de esta nota'));
  assert.deepEqual(output.metadata, { original: true });
});

test('no transforma otros resultados ni un read sin bloque completo', async () => {
  const hooks = await plugin({ directory: process.cwd() });
  for (const input of [
    { tool: 'grep', args: { filePath: '/vault/Nota.md' } },
    { tool: 'read', args: { filePath: '/vault/fuente.py' } },
    { tool: 'read', args: { filePath: '/vault/Nota.md' } },
  ]) {
    const output = { output: index + body };
    await hooks['tool.execute.after'](input, output);
    assert.equal(output.output, index + body);
  }
});

test('una lectura por rangos conserva el índice y sus números', async () => {
  const hooks = await plugin({ directory: process.cwd() });
  for (const range of [{ offset: 1 }, { limit: 20 }]) {
    const text = '<content>\n' + (index + body).split('\n').map((line, i) => `${i + 1}: ${line}`).join('\n') + '\n</content>';
    const output = { output: text };
    await hooks['tool.execute.after']({ tool: 'read', args: { filePath: '/vault/Nota.md', ...range } }, output);
    assert.equal(output.output, text);
  }
});

async function fixture(t) {
  const base = await fs.mkdtemp(path.join(os.tmpdir(), 'genesis-opencode-'));
  const root = path.join(base, 'boveda');
  await fs.mkdir(root);
  await fs.mkdir(path.join(root, 'Notas'));
  await fs.writeFile(path.join(root, 'Notas/permitida.md'), '# Permitida\n');
  await fs.writeFile(path.join(root, 'Notas/privada.md'), 'NO_LEER\n');
  const outside = path.join(base, 'fuera.md');
  await fs.writeFile(outside, 'FUERA_NO_LEER\n');
  t.after(async () => {
    assert.equal(path.dirname(base), path.resolve(os.tmpdir()));
    assert.ok(path.basename(base).startsWith('genesis-opencode-'));
    await fs.rm(base, { recursive: true, force: true });
  });
  return { root, outside };
}

test('consulta habilita solo archivos explícitos y conserva modelo y proveedor', async t => {
  const { root } = await fixture(t);
  const hooks = await plugin({ directory: root }, { readPaths: ['Notas/permitida.md'] });
  const config = { model: 'proveedor/modelo', agent: { consulta: { mode: 'primary' } } };
  await hooks.config(config);
  assert.equal(config.model, 'proveedor/modelo');
  assert.equal(config.permission['*'], 'deny');
  assert.equal(config.permission.external_directory, 'deny');
  assert.equal(config.permission.read['*'], 'deny');
  assert.equal(config.permission.read[path.join(root, 'Notas/permitida.md')], 'allow');
  assert.equal(config.permission.read[path.join('Notas', 'permitida.md')], 'allow');
  await hooks['tool.execute.before']({ tool: 'read' }, { args: { filePath: path.join(root, 'Notas/permitida.md') } });
});

test('rechaza otras herramientas, rutas internas ajenas, externas y escapes', async t => {
  const { root, outside } = await fixture(t);
  const hooks = await plugin({ directory: root }, { readPaths: ['Notas/permitida.md'] });
  for (const tool of ['bash', 'edit', 'write', 'grep', 'glob', 'task', 'webfetch']) {
    await assert.rejects(hooks['tool.execute.before']({ tool }, { args: {} }));
  }
  for (const filePath of [path.join(root, 'Notas/privada.md'), outside, 'Notas/../Notas/permitida.md', 'Notas/inexistente.md']) {
    await assert.rejects(hooks['tool.execute.before']({ tool: 'read' }, { args: { filePath } }));
  }
});

test('la precarga no acepta instrucciones fuera de la lista', async t => {
  const { root } = await fixture(t);
  const hooks = await plugin({ directory: root }, { readPaths: ['Notas/permitida.md'] });
  for (const instructions of [['Notas/privada.md'], ['https://example.com/reglas.md'], ['Notas/*.md']]) {
    await assert.rejects(hooks.config({ instructions }));
  }
  await assert.rejects(hooks['experimental.chat.system.transform']({}, {
    system: ['Instructions from: ' + path.join(root, 'Notas/privada.md') + '\nNO_LEER'],
  }));
});

test('rechaza junctions o symlinks incluso si su nombre está autorizado', async t => {
  const { root, outside } = await fixture(t);
  const link = path.join(root, 'Redireccion');
  await fs.symlink(path.dirname(outside), link, process.platform === 'win32' ? 'junction' : 'dir');
  const hooks = await plugin({ directory: root }, { readPaths: ['Redireccion/fuera.md'] });
  await assert.rejects(hooks['tool.execute.before']({ tool: 'read' }, { args: { filePath: path.join(link, 'fuera.md') } }));
});

for (const readPaths of [[], null, ['../fuera.md'], ['/fuera.md'], ['C:/fuera.md'], ['Notas/*.md'], ['Notas/CON.md'], ['Notas/nota.md:ads'], ['Notas/nota.']]) {
  test('rechaza una lista inválida: ' + JSON.stringify(readPaths), async () => {
    await assert.rejects(plugin({ directory: process.cwd() }, { readPaths }));
  });
}
