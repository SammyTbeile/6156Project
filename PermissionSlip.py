'''
Sammy Tbeile - st2918
Program to scan the manifest file to see which permissions are requested

'''
import argparse
from pathlib import Path
import re
import os

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description = "Program to generate the list of permissions requested")
    parser.add_argument("-m", "--manifest", action="store", default="./app/src/main/AndroidManifest.xml")
    parser.add_argument("-f", "--files", action="store", default="")
    parser.add_argument("-d", "--dictionary", action="store", default="./")
    parser.add_argument("-o", "--output", action="store", default="report.md")
    arguments = parser.parse_args()

    #check that the manifest exists
    manifest_file = Path(arguments.manifest)
    if( not manifest_file.is_file()):
        print("Please specify a manifest file")
        exit(1)
    package_name = ""
    requested_permissions = []
    pattern = r'android.permission.*"'
    regex = re.compile(pattern)
    with open(arguments.manifest) as manifest:
        for line in manifest:
            if ("package=" in line):
                package_pattern = r'package=".*"'
                package_regex = re.compile(package_pattern)
                res = package_regex.search(line)
                package_name = res.group(0).lstrip("package=").strip("\"")
            if ("android.permission" in  line):
                result = regex.search(line)
                requested_permission  = result.group(0).lstrip("android.permission").rstrip("\"")
                requested_permissions.append(requested_permission)

    print("Your application requests the following permissions: ")
    for perm in requested_permissions:
        print(perm)
    # print(package_name)

    #if no input files specified use the default path
    default_path = "./app/src/main/java/"
    for part in package_name.split("."):
        default_path += str(part) + "/"

    # get source files
    source_files = []
    if(arguments.files == ""):
        for name in os.listdir(default_path):
            source_files.append(default_path + name)
    else:
        with open(argument.files, "r") as source_list:
            for directory in soruce_list:
                for name in os.listdir(directory.strip()):
                    source_files.append(directory.strip() + name)
    print("We have detected the following source files: ")
    for s in source_files:
        print(s)

    # build dictionary of permissions
    permissions = dict()
    with open(arguments.dictionary +"sensitive_api_calls.txt", "r") as perm_file:
        for line in perm_file:
            # structure of each line <class>|<permission>|<description>
            line_list = line.split("|")
            this_class =line_list[0].strip()
            permissions[this_class] = dict()
            permissions[this_class]["permissions"] = []
            for p in line_list[1].strip().split(","):
                permissions[this_class]["permissions"].append(p)
            permissions[this_class]["description"] = line_list[2].strip()

    #build list of classes and permissions used
    used_permissions = dict()
    for source in source_files:
        with open(source, "r") as source_file:
            for line in source_file:
                #currently only check import lines
                line = line.strip()
                if(line.startswith("import")):
                    line_parts = line.lstrip("import ").rstrip(";").split(".")
                    for part in line_parts:
                        if (part in permissions):
                            recorded_permissions = permissions[part]["permissions"]
                            for permission in recorded_permissions:
                                if(permission not in used_permissions):
                                    used_permissions[permission] = set()
                                used_permissions[permission].add(part)

    # Check to see if over privileged
    unneeded_permissions = set()
    for permission in requested_permissions:
        if(permission not in used_permissions):
            unneeded_permissions.add(permission)
    if(len(unneeded_permissions) >0):
        print("Your application requests unneeded permissions:")
        for perm in unneeded_permissions:
            print(perm)
    else:
        print("You use all requested permissions. Good job!")

    # Output report of used permissions
    out_name = arguments.output
    with open(out_name, "w") as output:
        output.write("# Report of Permission Usage:\n")
        for permission in used_permissions:
            output.write("## " + str(permission) + ":\n")
            for c in used_permissions[permission]:
                output.write("  - " + str(c) + "\n")
                output.write("      Description: " + str(permissions[c]["description"]) + "\n")
    print("Output written to: " + out_name)


if __name__ == "__main__":
    main()
