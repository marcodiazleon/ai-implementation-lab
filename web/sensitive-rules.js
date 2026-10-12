"use strict";
// R54g / D52: the same named formats as src/lab/sensitive.py, for the interface guards (exports and saved
// configurations). Spellings are split so that this file never matches itself. Pure: no DOM, loadable in Node.
(() => {
 const rules = [
  ["Anthropic key", new RegExp("\\bsk-" + "ant-[A-Za-z0-9_-]{20,}")],
  ["OpenAI key", new RegExp("\\bsk-" + "(?!ant-)(?:proj-|svcacct-|admin-)?[A-Za-z0-9_-]{20,}")],
  ["Context7-style key", new RegExp("\\bctx7" + "sk-[A-Za-z0-9_-]{16,}")],
  ["GitHub token", new RegExp("\\b(?:gh[pousr]_" + "[A-Za-z0-9]{30,}|github_pat_" + "[A-Za-z0-9_]{40,})")],
  ["AWS access key id", new RegExp("\\b(?:AKIA|ASIA)" + "[A-Z0-9]{16}\\b")],
  ["Slack token", new RegExp("\\bxox" + "[abprs]-[A-Za-z0-9-]{10,}")],
  ["Google API key", new RegExp("\\bAIza" + "[0-9A-Za-z_-]{35}\\b")],
  ["private key block", new RegExp("-----BEGIN " + "(?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY(?: BLOCK)?-----")],
  ["bearer token", new RegExp("\\bbearer" + "\\s+[A-Za-z0-9._~+/=-]{20,}", "i")],
  ["credential assignment", new RegExp("\\b(?:api[_-]?key|secret|passw" + "ord|token)\\b\\s*[=:]\\s*(?:\\\\?['\"][A-Za-z0-9._~+/-]{16,}\\\\?['\"]|(?=[A-Za-z0-9._~+/-]*\\d)[A-Za-z0-9._~+/-]{16,})", "i")],
  ["local personal path", new RegExp("[A-Za-z]:\\\\{1,2}Users\\\\{1,2}" + "[^\\\\\\s\"']+|(?<![\\w/.])/(?:Users|home)/" + "[A-Za-z0-9._-]+/", "i")],
 ];
 // Labels of every format found in the text and in its JSON serialization (escapes can hide a path or a quote).
 const findSecrets = (text) => {
  const serialized = JSON.stringify(text);
  return rules.filter(([, re]) => re.test(text) || re.test(serialized)).map(([label]) => label);
 };
 // R54g / D56: every string value of nested objects and arrays, raw, plus the serialized whole; nothing is evaluated.
 const findSecretsIn = (value) => {
  const found = new Set();
  const stack = [value];
  while (stack.length) {
   const item = stack.pop();
   if (typeof item === "string") for (const label of findSecrets(item)) found.add(label);
   else if (Array.isArray(item)) stack.push(...item);
   else if (item && typeof item === "object") { stack.push(...Object.keys(item)); stack.push(...Object.values(item)); }
  }
  let serialized = "";
  try { serialized = JSON.stringify(value) || ""; } catch { serialized = String(value); }
  for (const label of findSecrets(serialized)) found.add(label);
  return [...found];
 };
 const api = { findSecrets, findSecretsIn, rules: rules.map(([label]) => label) };
 if (typeof window !== "undefined") window.LabSensitive = api;
 if (typeof module !== "undefined" && module.exports) module.exports = api;
})();
