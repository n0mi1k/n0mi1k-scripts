# Author github.com/n0mi1k
# This script is created to grab the IPA file before deletion by Apple Configurator after downloading
import os
import shutil

"""
Steps to retrieve the IPA file from the Configurator app:

1. Install Apple Configurator from the Mac App Store and sign in to Apple ID
2. Connect your IOS device to your Mac
3. Select "Add > Apps..." and search for the app you want to install, click "Add"
4. The newer Apple Configurator deletes the IPA after installing it, so you'll need to use this tool to grab it
5. Run this script and wait for the app to be installed
6. The IPA will be quickly copied to ipaDir before it is deleted by Apple Configurator

IPAs can be used for analysis later on =)

NOTE: Remember to modify appsDir and ipaDir accordingly below
"""

appsDir = "/Users/user/Library/Group Containers/K36BKF7T3D.group.com.apple.configurator/Library/Caches/Assets/TemporaryItems/MobileApps" # Configurator app directory
ipaDir = "/Users/user/Desktop/IPAs" # Directory to extract to

if not os.path.exists(ipaDir):
    os.makedirs(ipaDir)

print("[+] Waiting for new IPA...")
ipaList = []
while True:
    for root, dirs, files in os.walk(appsDir):
        for file in files:
            if file.endswith(".ipa"):
                if os.path.join(root, file) in ipaList:
                    continue
                ipaPath = os.path.join(root, file)
                print(ipaPath)
                ipaList.append(ipaPath)
                shutil.copy2(ipaPath, os.path.join(ipaDir, file))
                print(f"[+] Extracted new IPA {file} to {ipaDir}")