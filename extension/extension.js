const vscode = require('vscode');

function activate(context) {
    let disposable = vscode.commands.registerCommand('extension.helloWorld', function () {
        vscode.window.showInformationMessage('Hello World!');
    });
    context.subscriptions.push(disposable);
    console.log('Extension activated');
}

function deactivate() {
    console.log('Extension deactivated');
}

module.exports = {
    activate,
    deactivate,
};