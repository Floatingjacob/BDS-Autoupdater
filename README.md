# BDS-Autoupdater
This python script will automatically update your Minecraft: Bedrock Editon Dedicated Server

NOTE(S)
If for any reason your pc blocks the download, open up command prompt and type (or paste) (curl -o BDS-Autoupdater.zip https://codeload.github.com/Floatingjacob/BDS-Autoupdater/zip/refs/heads/main) into it and hit enter. then, extract the zip folder's contents into your bedrock server folder.

YOU MUST HAVE AN EXISTING DEDICATED SERVER SET UP AND RUNNING BEFORE YOU RUN THS SCRIPT, OTHERWISE THIS SCRIPT WILL NOT WORK.

REQUIREMENTS
1. Python (i have only tested it on python 3 but slightly older versions should work.)
2. Selenium python library (pip install selenium)
3. Requests python library (pip install requests)
4. A windows machine running a Minecraft: Bedrock Editon Dedicated Server
5. The Google Chrome web browser installed on your windows machine.

HOW TO USE
1. Download the source code and extract the entire contents of the folder to your Minecraft: Bedrock Editon Dedicated Server folder.
2. There should be an empty folder named updatetemp DO NOT DELETE THIS FOLDER.
3. Create a task in the Task Scheduler program to run the script at 3:00AM (or whenever you want it to check for updates)
4. That is it (well besides make sure your computer is on to run this script).
