const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

const panels = new Map();

function activate(context) {
  context.subscriptions.push(vscode.workspace.onDidOpenTextDocument(doc => {
    if (doc.fileName.endsWith('.norm')) showLogo(doc, context);
  }));

  vscode.workspace.textDocuments.forEach(doc => {
    if (doc.fileName.endsWith('.norm')) showLogo(doc, context);
  });
}

function showLogo(doc, context) {
  const key = doc.uri.toString();
  if (panels.has(key)) return;
  const panel = vscode.window.createWebviewPanel('norimaLogo', 'Norima Logo', { viewColumn: vscode.ViewColumn.Beside, preserveFocus: true }, { enableScripts: false });
  panels.set(key, panel);
  panel.onDidDispose(() => panels.delete(key));
  try {
    const svgPath = path.join(context.extensionPath, '..', 'logos.norm', 'norm file logo.svg');
    const svg = fs.readFileSync(svgPath, 'utf8');
    panel.webview.html = `<html><body style="display:flex;align-items:center;justify-content:center;padding:12px;background:#ffffff">${svg}</body></html>`;
  } catch (e) {
    panel.webview.html = `<html><body><h3>Norima Logo</h3><p>Logo not found at ../logos.norm/norm file logo.svg</p></body></html>`;
  }
}

function deactivate() {
  panels.forEach(p => p.dispose());
  panels.clear();
}

module.exports = { activate, deactivate };
