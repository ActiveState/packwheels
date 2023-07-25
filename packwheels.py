import os
import tarfile
import requests
import argparse
from urllib.parse import urljoin

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)

def get_package_wheels(package_name, package_version):
    base_url = f"https://pypi.org/pypi/{package_name}/{package_version}/json"
    response = requests.get(base_url)
    data = response.json()

    os.makedirs(package_name, exist_ok=True)

    for release_file in data['urls']:
        if release_file['packagetype'] == 'bdist_wheel':
            file_url = release_file['url']
            file_name = os.path.join(package_name, file_url.split('/')[-1])
            download_file(file_url, file_name)

    with tarfile.open(f"{package_name}.tar.gz", "w:gz") as tar:
        tar.add(package_name, arcname=os.path.basename(package_name))

def main():
    parser = argparse.ArgumentParser(description='Download wheels for a package from PyPI.')
    parser.add_argument('package_name', type=str, help='The name of the package to download.')
    parser.add_argument('package_version', type=str, help='The version of the package to download.')

    args = parser.parse_args()
    get_package_wheels(args.package_name, args.package_version)

if __name__ == '__main__':
    main()
