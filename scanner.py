'''
Sammy Tbeile - st2918
Program to scan the manifest file to see which permissions are requested

'''
import argparse
from pathlib import Path
import re

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description = "Program to generate the list of permissions requested")
    parser.add_argument("--manifest", action="store", default="./app/src/main/AndroidManifest.xml")
    parser.add_argument("-i", action="store", default="")
    arguments = parser.parse_args()

    #check that the manifest exists
    manifest_file = Path(arguments.manifest)
    if( not manifest_file.is_file()):
        print("Please specify a manifest file")
        exit(1)
    requested_permissions = []
    pattern = r'android.permission.*"'
    regex = re.compile(pattern)
    with open(arguments.manifest) as manifest:
        for line in manifest:
            if ("android.permission" in  line):
                result = regex.search(line)
                requested_permission  = result.group(0).lstrip("android.permission").rstrip("\"")
                requested_permissions.append(requested_permission)
    print("Requested permissions: " + str(requested_permissions))



if __name__ == "__main__":
    main()
