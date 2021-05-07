# Cowin Tracker

This tool has been created to monitor cowin web-site to check for the availability of vaccination slots. 

To use this tool, follow the below steps:

1.  Download **cowin_tracker.exe** & **district_code.json** from **executables** directory.
2.  Double click on the exe file to start cowin_tracker. 
3.  You will be prompted to enter your **district_id**. Select the appropriate id for your district from the list shown in the console.
4.  Now you will be asked to enter the **minimum age limit** for your search. Enter either **18 or 45** based on your requirement.
5.  Hit enter and wait. 
6.  If there are any slots available then the details for that slot with the center name, pincode, vaccine type etc. will be displayed in the console and a beep sound will be played to alert you that an available slot has been found.
7.  If no slot is found then the tool will keep on monitoring the cowin website at a constant interval of time.
8.  You can close the tool at any time by pressing **CTRL+C**.

### Note:
1.  This tool will work on Windows X64. It has not been tested on other operating systems.
2.  **district_code.json** file has information for all districts in Assam, INDIA. I have additionally included json files for Karnataka and West Bengal in **additional_district_codes** directory.
3.  To search for Karnataka or West Bengal or for any other state, the correct json file should be placed in the same directory where **cowin_tracker.exe** is present
and the json file should be named as **district_code.json**.
