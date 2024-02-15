# DiffParser by Krishika

import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from typing import Optional
import subprocess
from FileParse import split_code
import * as vscode from 'vscode';


# def get_latest_commit() -> Optional[str]:
#     try:
#         # Get the path to the current workspace
#         workspace_folders = vscode.workspace.workspace_folders
#         if workspace_folders:
#             workspace_path = workspace_folders[0].uri.fs_path
#         else:
#             vscode.window.showErrorMessage("No workspace found.")
#             return None

#         # Run git command to get the hash of the latest commit
#         latest_commit_hash = run_git_command(workspace_path, 'rev-parse', 'HEAD').strip()
#         return latest_commit_hash
#     except Exception as e:
#         vscode.window.showErrorMessage(f"Failed to retrieve the latest commit: {str(e)}")
#         return None

def run_git_command(repo_path: str, *args: str) -> str:
    try:
        result = subprocess.run(['git', *args], cwd=repo_path, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to run git command: {e.stderr}")

def activate(context: vscode.ExtensionContext) -> None:
    def command_handler() -> None:
        latest_commit = get_latest_commit()
        if latest_commit:
            vscode.window.showInformationMessage(f"Latest commit: {latest_commit}")

    context.subscriptions.append(vscode.commands.register_command('extension.getLatestCommit', command_handler))


activate()

def startUp():
    githubUrl = input("Please enter your GitHub repo url: \n")
    accessToken = input("Please enter your GitHub Access Token: \n")
    listen_for_commits(githubUrl,accessToken)

def get_code_to_process(commit):
    return commit.get('commit', {}).get('message', '')

class WebhookHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code):
        self.send_response(status_code)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        payload = self.rfile.read(content_length).decode('utf-8')
        payload_data = json.loads(payload)

        # Process the webhook payload
        self.process_webhook_payload(payload_data)

        # Respond with 200 OK
        self._send_response(200)

    def process_webhook_payload(self, payload):
        # Implement your logic to handle the webhook payload here
        print("Webhook payload received:", payload)

        # Extract repository URL from payload (adjust this based on your payload structure)
        # repo_url = payload.get('repository', {}).get('html_url')
        
        # Check if the repository URL is available
        # if repo_url:
        #     # Listen for commits and process them
        #     listen_for_commits(repo_url)



def listen_for_commits(githubUrl, accessToken):
    # Authentication to GitHub API
    headers = {
        'Authorization': 'Bearer {accessToken}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Extracting owner and repo name from the URL
    parts = githubUrl.strip('/').split('/')
    owner = parts[-2]
    repo_name = parts[-1]

    #testing to see if I have access to the repo
    print(owner)

    # Get commits for the repository
    commits_url = f'{githubUrl}/commits'
    req = urllib.request.Request(commits_url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 200:
                data = response.read().decode('utf-8')
                try:
                    commits = json.loads(data)
                    for commit in commits:
                        print(commit['sha'])  # Access the commit SHA or other details

                        #split code into chunks
                        code_to_process = get_code_to_process(commit)
                        chunks = split_code(code_to_process, token_limit=500)
                        print("Chunks: ", chunks)

                        # if len(code_to_process) <= gpt3_5:
                        #     model = " GPT 3.5"
                        #     chunk_size = gpt3_5
                        # else:
                        #     model = "GPT 4.0"
                        #     chunk_size = gpt4
                        # code_chunks = split_code(code_to_process, chunk_size)


                        # Perform diff parsing and test case generation for each commit
                except json.decoder.JSONDecodeError as e:
                    print(f'Failed to parse JSON data: {e}')
            else:
                print(f'Failed to fetch commits: {response.getcode()} - {response.reason}')

    except urllib.error.HTTPError as e:
        print(f'Failed to fetch commits: {e.code} - {e.reason}')

def run(server_class=HTTPServer, handler_class=WebhookHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Webhook server listening on port {port}")
    httpd.serve_forever()

startUp()
run()