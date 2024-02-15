// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import { spawn } from "child_process";
import * as vscode from "vscode";

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
  // Use the console to output diagnostic information (console.log) and errors (console.error)
  // This line of code will only be executed once when your extension is activated
  console.log('Congratulations, your extension "bahar" is now active!');

  // The command has been defined in the package.json file
  // Now provide the implementation of the command with registerCommand
  // The commandId parameter must match the command field in package.json
  let disposable = vscode.commands.registerCommand("bahar.helloWorld", () => {
    // The code you place here will be executed every time your command is executed
    // Display a message box to the user
    vscode.window.showInformationMessage("Hello World from Bahar!");
  });

  context.subscriptions.push(disposable);

  let pythonDisposable = vscode.commands.registerCommand("bahar.runPythonScript", () => {
    // Path to your Python script
    const pythonScriptPath = '/path/to/your/python/script.py';

    // Spawn a child process to execute the Python script
    const pythonProcess = spawn('python', [pythonScriptPath]);

    // Listen for output from the Python script
    pythonProcess.stdout.on('data', (data) => {
      console.log(`Python script output: ${data}`);
    });

    // Listen for errors from the Python script
    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python script error: ${data}`);
    });
  });

  context.subscriptions.push(pythonDisposable);


}

// This method is called when your extension is deactivated
export function deactivate() {}
