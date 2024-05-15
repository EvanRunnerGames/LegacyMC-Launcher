import requests
import os
import json

def fetch_version_manifest(version):
    # URL to the version manifest JSON
    manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    response = requests.get(manifest_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch version manifest: {response.text}")

    manifest = response.json()

    # Find the specified version in the manifest
    version_info = next((v for v in manifest['versions'] if v['id'] == version), None)
    if not version_info:
        raise Exception(f"Version {version} not found")

    # Fetch the version's detailed information
    version_url = version_info['url']
    response = requests.get(version_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch version details: {response.text}")

    return response.json()

def download_file(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {path}")
    else:
        raise Exception(f"Failed to download {url}: {response.text}")

def download_version_files(version_details, base_dir):
    # Download the client JAR file
    jar_info = version_details['downloads']['client']
    jar_url = jar_info['url']
    jar_path = os.path.join(base_dir, 'versions', version_details['id'], f"{version_details['id']}.jar")
    download_file(jar_url, jar_path)

    # Download the libraries
    for library in version_details['libraries']:
        if 'downloads' in library and 'artifact' in library['downloads']:
            artifact = library['downloads']['artifact']
            artifact_url = artifact['url']
            artifact_path = os.path.join(base_dir, artifact['path'])
            download_file(artifact_url, artifact_path)

def main():
    version = input("Enter the Minecraft version to download (e.g., 1.16.5): ")
    base_dir = "./minecraft"  # Base directory to save downloaded files

    try:
        version_details = fetch_version_manifest(version)
        download_version_files(version_details, base_dir)
        print(f"Minecraft {version} downloaded successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
