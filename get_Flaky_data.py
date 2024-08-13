import os
import requests
import pandas as pd
import time

# Configuration
output_dir = 'dataset/project/'
flaky_methods_dir = os.path.join(output_dir, 'flakyMethods')

# GitHub API configuration
github_token = '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'
headers = {'Authorization': f'token {github_token}'}

# Ensure directories exist
os.makedirs(flaky_methods_dir, exist_ok=True)

# Load quantum flakiness dataset
dataset_path = 'Flakiness Dataset - ESEM.csv'
dataset = pd.read_csv(dataset_path)

# Create PR URL column
base_url = "https://github.com/"
dataset['Repo URL'] = base_url + dataset['Repo']
dataset['Fix'] = dataset['Fix'].str.replace('#', '')  # Remove '#' from Fix
dataset['PR URL'] = dataset['Repo URL'] + "/pull/" + dataset['Fix']

# Function to get the base commit SHA of a pull request
def get_base_commit_sha(repo_name, pr_number):
    api_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}"
    for attempt in range(3):
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            pr_details = response.json()

            # Log base commit and merge commit (if any)
            base_commit_sha = pr_details['base']['sha']
            merge_commit_sha = pr_details.get('merge_commit_sha', 'None')
            print(f"Base commit for PR {pr_number}: {base_commit_sha}")
            print(f"Merge commit (if any): {merge_commit_sha}")

            return base_commit_sha
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Wait before retrying
    raise Exception(f"Failed to get base commit SHA for PR {pr_number} after 3 attempts")

# Function to list files in a given commit
def list_files_in_commit(repo_name, commit_sha):
    api_url = f"https://api.github.com/repos/{repo_name}/git/trees/{commit_sha}?recursive=1"
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    tree = response.json()
    return [file['path'] for file in tree['tree'] if file['type'] == 'blob']

# Function to fetch and save the file content with retry logic, including repo name, PR number, and commit SHA in the file name
def fetch_and_save_file(repo_name, pr_number, commit_sha, file_path, url, save_dir):
    file_name = f"{repo_name.replace('/', '_')}_PR{pr_number}_{commit_sha}_{file_path.replace('/', '_')}"
    save_path = os.path.join(save_dir, file_name)
    for attempt in range(3):
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            return
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error while fetching file {url}: {http_err}")
            if attempt < 2:  # Retry for the first two attempts
                print("Retrying...")
                time.sleep(2)
            else:
                errors.append(f"Failed to fetch file {url}: {http_err}")

# Function to extract flaky methods from the base commit and print their URLs
def extract_flaky_methods(dataset, flaky_methods_dir):
    errors = []
    added_files = []
    records = []  # List to store records for the Excel file
    for index, row in dataset.iterrows():
        pr_url = row['PR URL']
        if not pd.isna(pr_url):
            print(f"Processing {pr_url}...")
            repo_name = row['Repo']
            pr_number = row['Fix']
            try:
                base_commit_sha = get_base_commit_sha(repo_name, pr_number)
                files_in_commit = list_files_in_commit(repo_name, base_commit_sha)
                api_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"
                response = requests.get(api_url, headers=headers)
                response.raise_for_status()
                files = response.json()
                for file in files:
                    if file['filename'].endswith('.py'):
                        file_path = file['filename']
                        if file['status'] == 'added':
                            added_files.append(f"File added in pull request: {file_path} at {pr_url}")
                            continue
                        if file['status'] == 'renamed':
                            old_path = file['previous_filename']
                            new_path = file['filename']
                            if old_path not in files_in_commit:
                                errors.append(f"Renamed file not found in base commit: {old_path} at {pr_url}")
                            continue
                        if file_path not in files_in_commit:
                            errors.append(f"File not found in base commit: {file_path} at {pr_url}")
                            continue
                        raw_url = f"https://raw.githubusercontent.com/{repo_name}/{base_commit_sha}/{file_path}"
                        try:
                            fetch_and_save_file(repo_name, pr_number, base_commit_sha, file_path, raw_url, flaky_methods_dir)
                            # Record data for Excel file
                            records.append({
                                'Repo Name': repo_name,
                                'PR URL': pr_url,
                                'PR Number': pr_number,
                                'Commit SHA': base_commit_sha
                            })
                        except requests.exceptions.HTTPError as http_err:
                            errors.append(f"Failed to fetch file {file_path} at {pr_url}: {http_err}")
            except Exception as e:
                errors.append(f"Failed to process {pr_url}: {e}")

    if added_files:
        print("\nFiles added in pull requests (skipped):")
        for file in added_files:
            print(file)

    if errors:
        print("\nErrors encountered during processing:")
        for error in errors:
            print(error)
    
    # Return the collected records
    return records

# Extract flaky methods and collect data for Excel
records = extract_flaky_methods(dataset, flaky_methods_dir)

# Step 2: Create an Excel file from the collected data
df = pd.DataFrame(records)
output_excel_path = os.path.join(output_dir, 'repo_pr_commit_data.xlsx')
df.to_excel(output_excel_path, index=False)

print(f"Excel file created: {output_excel_path}")
