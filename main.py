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

            # Make a modification to the Dockerfile
            print(f'Modifying Dockerfile in {repo_name}...')
            with open(f'{repo_name}/Dockerfile', 'a') as f:
                f.write('\n# This is a modification\n')

            # Use git to commit the change and push it to a new branch
            print(f'Committing changes and pushing to new branch in {repo_name}...')
            repo = git.Repo(repo_name)
            repo.git.checkout('HEAD', b='new_branch')
            repo.git.add('--all')
            repo.git.commit('-m', 'Modified Dockerfile')
            repo.git.push('origin', 'new_branch')

            # Create a pull request
            print(f'Creating a pull request for {repo_name}...')
            url = f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repo_name}/pullrequests?api-version=6.0'
            data = {
                "sourceRefName": "refs/heads/new_branch",
                "targetRefName": "refs/heads/main",
                "title": "Modification to Dockerfile",
                "description": "This is a modification to the Dockerfile.",
            }
            response = requests.post(url, headers=headers, json=data)

            if response.status_code != 200:
                print(f'Failed to create a pull request for {repo_name}')
            else:
                print(f'Successfully created a pull request for {repo_name}')

            # Delete the cloned repo from local machine
            print(f'Deleting cloned repo {repo_name}...')
            shutil.rmtree(repo_name)

            # Update the progress bar
            pbar.update(1)
