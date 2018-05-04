# Permission Slip
### A utility for detecting unnecessary privileges in Android applications
By Sammy Tbeile

## Description:
This is a tool that is meant to scan an Android application and output: a list of permissions that were declared but not needed and a report of used permissions.
This report details all classes used that contain sensitive API calls and also what those calls do in a simple Markdown file.
A run of the tool proceeds as follows:
1. The manifest file is loaded and then scanned for declared permissions. These will be output
2. A list of source code files is then loaded
3. A dictionary of sensitive permissions, classes that use them, and a preliminary description is built up from the sensitive_api_calls.txt file (or the one specified by the -d permission)
4. The source code is then scanned for those permissions that match the dictionary
5. Any unnecessary permissions are outputted
6. A report of used permissions is generated and stored in report.md (or the output file specified)

## Dependencies:
- Python3

## Usage
The application can be used as follows:

```
python3 PermissionSlip.py [-m] [-f] [-d] [-o]
```

### Arguments
- \-m or \-\-manifest

    The path to the manifest file for the application

- \-f or \-\-files

    A file containing a list of source code directories

- \-d or \-\-dictionary

    A list of classes which use sensitive API calls. See below

- \-o or \-\-output

    The name of a file to store the report of used permissions in

The application assumes a simple default AndroidStudio layout by default. If your application adheres to this layout, you will not need to specify a manifest file (./app/src/main/AndroidManifest.xml is assumed) or a list of source code directories. If the sensitive_api_calls.txt file is in the same directory as the tool is run from, it need not be specified. By default, the output will be placed in a file called report.md in the same directory as the tool is run from.

## Sensitive API List
I manually compiled a list of classes that contain sensitive API calls (sensitive_api_calls.txt). This list is probably not exhaustive as it was compiled manually and much of the Android documentation is incomplete. Feel free to add to it with a pull request!
The descriptions were extracted from the first sentence of the documentation. Feel free to update these as well with a pull request.

If you choose to use your own list, the format is:
\<sensitive class\>|\<permission it uses\>|\<description\>

## Sample Usage
I have included the demo app provided from: https://github.com/codepath/intro_android_demo in the repository as a sample application. I have slightly modified it to request unneeded Bluetooth permissions.

Assuming that the application is in a folder titled demo_app2 in the Permission Slip directory. It can be run as follows:

[run]: https://github.com/SammyTbeile/PermissionSlip/blob/master/sample_usage.png "Example run"

Note: the `-d` flag is used to specify a dictionary file from the directory above. Also the Bluetooth permission is listed as unneeded. The generated report is:

[report]: https://github.com/SammyTbeile/PermissionSlip/blob/master/sample_report.png "Example report"
