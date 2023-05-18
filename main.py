import requests
import os
import git
import shutil
from base64 import b64encode
from tqdm import tqdm

# Personal Access Token from Azure DevOps
personal_access_token = 'your_personal_access_token_here'
organization = 'your_organization_name_here'
projects = ['project1', 'project2', 'project3']  # Add your project names here

# Prepare the request
headers = {
    'Authorization': 'Basic ' + b64encode((':{}'.format(personal_access_token)).encode()).decode(),
    'Content-Type': 'application/json'
}

# Specify the file to modify and the strings to replace
file_to_modify = 'Dockerfile'
strings_to_replace = {
    'old_string1': 'new_string1',
    'old_string2': 'new_string2'
    # Add more strings to replace as needed
}

for project in projects:
    # Get the list of repos in the project
    url = f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories?api-version=6.0'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f'Failed to get the list of repos for {project}')
        continue

    repos = response.json()['value']

    # Start the progress bar
    with tqdm(total=len(repos), desc=f"Processing repos in {project}", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
        for repo in repos:
            repo_name = repo['name']
            clone_url = repo['remoteUrl']

            # Clone the repo
            print(f'\nCloning {repo_name}...')
            os.system(f'git clone {clone_url}')

            # Perform a recursive search through each directory in the repository
            for root, dirs, files in os.walk(repo_name):
                if file_to_modify in files:
                    # Make modifications to the specified file
                    print(f'Modifying {file_to_modify} in {root}...')
                    with open(os.path.join(root, file_to_modify), 'r+') as f:
                        file_contents = f.read()
                        for old_string, new_string in strings_to_replace.items():
                            file_contents = file_contents.replace(old_string, new_string)
                        f.seek(0)
                        f.write(file_contents)

            # Use git to commit the change and push it to a new branch
            print(f'Committing changes and pushing to new branch in {repo_name}...')
            repo = git.Repo(repo_name)
            repo.git.checkout('HEAD', b='new_branch')
            repo.git.add('--all')
            repo.git.commit('-m', f'Modified {file_to_modify}')
            repo.git.push('origin', 'new_branch')

            # Create a pull request
            print(f'Creating a pull request for {repo_name}...')
            url = f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repo_name}/pullrequests?api-version=6.0'
            data = {
                "sourceRefName": "refs/heads/new_branch",
                "targetRefName": "refs/heads/main",
                "title": f"Modification to {file_to_modify}",
                "description": f"This is a modification to the {file_to_modify}.",
            }
            response = requests.post(url, headers=headers, json=data)

            if response.status_code != 200:
                print(f'Failed to create a pull request for {repo_name}')
            else:
                print(f'Successfullycreated a pull request for {repo_name}')

            # Clean up the cloned repo
            shutil.rmtree(repo_name)

            # Update the progress bar
            pbar.update(1)
