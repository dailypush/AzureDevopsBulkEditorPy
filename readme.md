

# Azure DevOps Bulk Pull Request Creator

This script automates the process of creating pull requests for multiple repositories in Azure DevOps. It clones each repository, modifies the Dockerfile, commits the changes, pushes the changes to a new branch, and creates a pull request. The script also includes a progress bar and status updates to track its progress.

## Requirements

- Python 3.7 or higher
- The `requests`, `gitpython`, `tqdm`, and `shutil` Python libraries
- A personal access token from Azure DevOps

## Usage

1. Clone this repository and navigate to the project directory.

```bash
git clone https://github.com/<your-username>/azure-devops-bulk-pr-creator.git
cd azure-devops-bulk-pr-creator
```

2. Install the required Python libraries.

```bash
pip install -r requirements.txt
```

3. Replace `'your_personal_access_token_here'`, `'your_organization_name_here'`, and `['project1', 'project2', 'project3']` with your Azure DevOps personal access token, your organization name, and your list of project names, respectively, in the `main.py` file.

4. Run the script.

```bash
python main.py
```

## Disclaimer

Please use this script responsibly. Creating a large number of pull requests in a short period of time can be disruptive to your team's workflow.
