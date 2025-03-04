const vscode = require('vscode');

function provideHover(document, position, token) {
	const wordRange = document.getWordRangeAtPosition(position);
	const word = document.getText(wordRange);

	if (word === "linear") {
		return new vscode.Hover("Linear activation function", wordRange);
	} else if (word === "poly") {
		return new vscode.Hover("Polynomial activation function", wordRange);
	} else {
		return null;
	}
}

module.exports = function activate(context) {
	context.subscriptions.push(
		vscode.languages.registerHoverProvider("nadl", {
			provideHover: provideHover
		})
	);
};
