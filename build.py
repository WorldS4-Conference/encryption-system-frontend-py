import os
import subprocess

# Step 1: Install PyInstaller
subprocess.call(['pip', 'install', 'pyinstaller'])

# Step 2: Create a spec file
subprocess.call(['pyinstaller', '--name=CipherHorizon', 'main.py'])

# Step 3: Edit the spec file (optional)

# Step 4: Build the executable
subprocess.call(['pyinstaller', 'CipherHorizon.spec'])

# Step 5: Test the executable
os.chdir('dist')
subprocess.call(['./CipherHorizon'])

# Step 6: Create a .deb package (optional)
subprocess.call(['dpkg-deb', '--build', 'CipherHorizon'])
