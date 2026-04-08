#!/usr/bin/env node
// scripts/compare-with-js.js
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const TARGET_DIR = process.argv[2] || '.';
const PY_OUTPUT_FILE = path.join(__dirname, 'py_results.json');
const JS_OUTPUT_FILE = path.join(__dirname, 'js_results.json');

console.log('🔄 Running py-mdlint (JSON mode)...');
try {
  execSync(`py-mdlint --batch --report json ${TARGET_DIR} > ${PY_OUTPUT_FILE}`, { stdio: 'inherit' });
} catch (e) {
  console.warn('⚠️  py-mdlint returned non-zero (expected if violations exist)');
}

console.log('🔄 Running markdownlint-cli2...');
try {
  execSync(`npx markdownlint-cli2 ${TARGET_DIR} --json > ${JS_OUTPUT_FILE}`, { stdio: 'inherit' });
} catch (e) {
  console.warn('⚠️  markdownlint-cli2 returned non-zero');
}

const pyResults = JSON.parse(fs.readFileSync(PY_OUTPUT_FILE, 'utf8'));
const jsResults = JSON.parse(fs.readFileSync(JS_OUTPUT_FILE, 'utf8'));

const normalize = (results) => {
  const map = new Map();
  for (const file in results) {
    for (const v of results[file]) {
      const key = `${v.ruleId || v.rule_id}:${v.lineNumber || v.line}`;
      map.set(key, v);
    }
  }
  return map;
};

const pyMap = normalize(pyResults);
const jsMap = normalize(jsResults);

const matches = [], pyOnly = [], jsOnly = [];
const allKeys = new Set([...pyMap.keys(), ...jsMap.keys()]);

for (const key of allKeys) {
  const py = pyMap.get(key);
  const js = jsMap.get(key);
  if (py && js) matches.push(key);
  else if (py) pyOnly.push({ key, rule: py });
  else jsOnly.push({ key, rule: js });
}

console.log(`\n📊 Résultat comparaison:`);
console.log(`✅ Correspondances : ${matches.length}`);
console.log(`🐍 py-mdlint uniquement : ${pyOnly.length}`);
console.log(`🟢 markdownlint JS uniquement : ${jsOnly.length}`);

if (pyOnly.length > 0) {
  console.log('\n⚠️  Violations py-mdlint non détectées par JS:');
  pyOnly.slice(0, 5).forEach(x => console.log(`  - ${x.key}: ${x.rule.message || x.rule.reason}`));
}
if (jsOnly.length > 0) {
  console.log('\n⚠️  Violations JS non détectées par py-mdlint:');
  jsOnly.slice(0, 5).forEach(x => console.log(`  - ${x.key}: ${x.rule.reason || x.rule.message}`));
}
