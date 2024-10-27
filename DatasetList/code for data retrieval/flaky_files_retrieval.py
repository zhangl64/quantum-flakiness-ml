import os
import requests
import pandas as pd
import time
import shutil  # Import shutil for zipping the directory

# Configuration
output_dir = 'project/dataset/'  # Main directory for storing data
flaky_methods_dir = os.path.join(output_dir, 'flakyMethods')  # Subdirectory for saving flaky methods

# GitHub API configuration
github_token = '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'  # GitHub token for API authentication
headers = {'Authorization': f'token {github_token}'}  # HTTP headers with authorization

# Ensure the directory for flaky methods exists
os.makedirs(flaky_methods_dir, exist_ok=True)

# Load quantum flakiness dataset
dataset_path = 'Flakiness Dataset - ESEM.csv'  # Path to the CSV file containing the dataset
dataset = pd.read_csv(dataset_path)  # Load the dataset into a pandas DataFrame

# Add columns to the dataset for constructing GitHub PR URLs
base_url = "https://github.com/"
dataset['Repo URL'] = base_url + dataset['Repo']  # Construct the repository URL
dataset['Fix'] = dataset['Fix'].str.replace('#', '')  # Remove '#' from Fix column
dataset['PR URL'] = dataset['Repo URL'] + "/pull/" + dataset['Fix']  # Construct the PR URL

# Function to get the base commit SHA of a pull request
def get_base_commit_sha(repo_name, pr_number):
    api_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}"
    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            pr_details = response.json()
            return pr_details['base']['sha']  # Return the base commit SHA
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Wait before retrying
    raise Exception(f"Failed to get base commit SHA for PR {pr_number} after 3 attempts")

# Function to fetch and save a file's content from a GitHub repository
def fetch_and_save_file(repo_name, pr_number, file_path, url, base_dir):
    repo_dir = os.path.join(base_dir, repo_name.replace('/', '_'))
    pr_dir = os.path.join(repo_dir, f"PR_{pr_number}")
    os.makedirs(pr_dir, exist_ok=True)

    file_name = file_path.replace('/', '_')
    save_path = os.path.join(pr_dir, file_name)

    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"Saved file: {save_path}")  # Log the saved file path
            return
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {file_path} (Attempt {attempt + 1}): {e}")
            time.sleep(2)  # Wait before retrying
    print(f"Failed to fetch {file_path} after 3 attempts.")

# Function to extract flaky methods from PRs and save relevant files
def extract_flaky_methods(dataset, flaky_methods_dir):
    errors = []  # List to track any errors encountered
    added_files = []  # List to track files added in PRs (that are skipped)
    records = []  # List to store data for each processed file

    for _, row in dataset.iterrows():
        pr_url = row['PR URL']
        if not pd.isna(pr_url):
            print(f"Processing {pr_url}...")
            repo_name = row['Repo']
            pr_number = row['Fix']
            try:
                base_commit_sha = get_base_commit_sha(repo_name, pr_number)  # Get the base commit SHA
                api_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"
                response = requests.get(api_url, headers=headers)
                response.raise_for_status()
                files = response.json()  # Get the list of files modified in the PR

                for file in files:
                    if file['filename'].endswith('.py'):  # Process only Python files
                        file_path = file['filename']
                        if file['status'] == 'added':  # Skip files added in the PR
                            added_files.append(f"File added in pull request: {file_path} at {pr_url}")
                            continue

                        raw_url = f"https://raw.githubusercontent.com/{repo_name}/{base_commit_sha}/{file_path}"

                        fetch_and_save_file(repo_name, pr_number, file_path, raw_url, flaky_methods_dir)

                        records.append({
                            'Repo Name': repo_name,
                            'PR URL': pr_url,
                            'PR Number': pr_number,
                            'Commit SHA': base_commit_sha,
                            'File Path': file_path
                        })
            except Exception as e:
                errors.append(f"Failed to process {pr_url}: {e}")  # Log errors

    if added_files:
        print("\nFiles added in pull requests (skipped):")
        for file in added_files:
            print(file)

    if errors:
        print("\nErrors encountered during processing:")
        for error in errors:
            print(error)

    return records

# Extract flaky methods and collect data for Excel
records = extract_flaky_methods(dataset, flaky_methods_dir)

# Step 2: Save the collected records to an Excel file for documentation
df = pd.DataFrame(records)
output_excel_path = os.path.join(output_dir, 'flaky_links.xlsx')
df.to_excel(output_excel_path, index=False)

print(f"Excel file created: {output_excel_path}")

# Step 3: Zip the flaky methods directory
zip_file_path = os.path.join(output_dir, 'flaky_methods.zip')
shutil.make_archive(zip_file_path.replace('.zip', ''), 'zip', flaky_methods_dir)

print(f"Flaky methods directory zipped: {zip_file_path}")
