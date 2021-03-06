##D0xBase Information

-------------------------------------------
| Name      | Version      | Release Date |
-------------------------------------------
| `D0xBase` | `0.1`        | `2011.07.20` |
-------------------------------------------
| `D0xBase` | `0.2+(beta)` | `2012.09.26` |
-------------------------------------------

Started on: `2011.07.20`  
Original Authors: `Kulverstukas && Factionwars`  

####Contributors
* Polyphony (2014.10.29)  

Release date: `2012.09.26`  
Project name: `D0xBase`  
Version: 0.4+alpha  
Copyright (C) 2011 Kulverstukas, Factionwars  

*******************************************************************

###License

D0xBase is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 3
D0xBase is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with D0xBase.  If not, see http://www.gnu.org/licenses/  

*******************************************************************

###SYSTEM PREREQUISITES
[Python 2.7.x](https://www.python.org/downloads/)  
[Urwid version >= 1.0]()

Included "Urwid" version is slightly modified
to display regular symbols instead of UTF8 for
lines around text blocks and little modification
to the buttons. This was done to provide better
compatability with most of the Linux terminals.

 @Linux:
   * CURSES/NCURSES
   * (Optional) SSH for remote usage
 @Windows:
   * Cygwin (see below for details)


INSTALLATION AND USAGE NOTES
 D0xBase now comes with few features that allows faster navigation
 and operation of the program.
 Command line arguments to access different screens, such as
 main (default), adding and searching.
 To access these screens instantly, run D0xBasewith --screen=main/add/search
 argument.
 Run with -h or --help to see the explanation.
 You can also make this permanent by setting it into configuration
 file, which is now also one of the few features.
 You can setup several things about how D0xBase looks and acts
 in the configuration file.
 Open the file to get more details and explanation on how to
 set values manually.
 Configuration wizard script has also been created to generate
 correct file in correct format. You can run this wizard by issuing
 "./D0xConfigWizard.py"
 D0xBase can also be ran from a smartphone running Android or iOS.
 This has been tested and works in an Emulator, "HTC Wildfire" and
 "HTC Galaxy S". See below for details on running it on smartphones.
 For quick-import your record to the database, you can use the
 --import command line argument and provide the file you want to import.

 Since version 0.3 D0xBase provides an export and import feature where
 you can backup and trade records. You can export in plain text or XML.
 Importing a record can only be from XML.
 Exports are places in "resources/exports" folder, and imports must be
 placed in "recourses/imports" folder.

 @Linux:
   Extract the archive where ever you want and navigate to that folder
   in your terminal. Run "./start.py" to begin and follow
   instructions on the screen to work.

 @Windows:
   To make it work on Windows systems, you will have to run it with
   Cygwin (http://cygwin.com/setup.exe).
   For Cygwin to run it, install the Python and Curses packages by
   selecting them at the Package selection screen. After Cygwin is
   finished, there should be an icon on the desktop. If not, then
   go to Cygwin installation folder and run "Cygwin.bat". Then navigate
   to where you have extracted D0xBase and run it by executing
   "./start.py".

 @Android:
   Usage on Android devices are a bit complicated. So far you can only
   view records by searching. Adding is not yet supported (unless your
   phone has an F2 key :) ). To use it you will need a copy of the latest
   issue (will work since version 0.2) and SL4A (Scripting Layer for Android)
   which can be found here: http://code.google.com/p/android-scripting/
   Install SL4A and Python using packages from the website above. Extract
   D0xBase to /mnt/sdcard/sl4a/scripts/d0xb (or other folder). Go to your SL4A
   application, touch/press on "start.py" and select first selection
   (black Terminal icon). D0xBase will now start to run. Might take little time
   to compile the classes and initiate the database.
   If the screen appears very small, open up the menu and select "Force size",
   leave default values and press "Resize".
   To open up a keyboard, touch the screen and touch an icon that appears in
   lower-right corner.
   That is it. You can now use D0xBase on your phone.


KNOWN ISSUES
 * D0xConfigWizard must be run with Python 2.7. Otherwise config file
   produced will be gibberish.
 * Browsing through records with arrow keys will produce an exception if
   abused (maximum recursion will be reached). There is no fix at this time.


FUTURE PLANS
 * Multilingual support
 * Logfile and selection in config file how to log and if to log
 * Online synchronization of the database
 * Database and export encryption with a key


TROUBLESHOOTING
 * If you can't seem to run D0xBase, make sure that you are running it
   with "Python 2.7" and not "Python 3.0" or lower than "Python 2.7" version.
 * See "How_to_report_errors" document to know how to help us troubleshoot and
   fix the problem.
 * If you cannot see the giant text in the main screen, then it is because you are
   running D0xBase in a terminal without UTF8 support. To see giant text, make sure
   you are running it in UTF8 mode. To do that issue a command: export LANG=en_us.UTF8


CONTRIBUTORS
 I have to mention the names that really helped us creating this project and
 here they are. Very big Thank You to all of you :)
   * nytephenix - testing the software and giving in-depth feedback
   * ceSar - for creating an awesome website
   * Satori - for some good ideas and moral support
   * namespace7 - for testing the software
   * Daemon - for helping develop pieces of software


CHANGELOG

D0xBase version 0.3, 2012.09.02:
 * Cleaned up the code file structure
 * Fixed a bug in Configuration wizard
 * Figure a way to set colors in XTerm to what it was after quiting
 * Export/Import XML files of records for trading and backup
 * Replaced static fields with dynamic ones by providing free-edit instead of just typed fields
 * Implemented a browsing function with arrow keys in the Info screen


D0xBase version 0.2, 2011.11.30:
 * Bug fix: Crash when a non-existing ID was entered in an interval 1..NumberOfPeople
 * Big chunks of text from d0xbasefront.py was put in a separate class
 * Birth date is now not required
 * Record index is now displayed in Add/Edit/Viewing screens
 * Blank lines now will not be replaced with "Not filled". Looked like it was annoying
 * Command line arguments has been added for faster navigation
 * Configuration file and a script to generate it has been added
 * Duplicate and unnecessary code has been removed
 * Unicode exception has been handled. Now it will work with ANSI terminals as well
 * Some buttons has been re-mapped, such as TAB to go to a new field when adding
   and ENTER instead of ESC to close a popup.
 * Warning screen when the last record in the database has been deleted

D0xBase version 0.1, 2011.10.02:
 * SQLite support
 * Uses CURSES, can be ran over SSH
 * Lots of people can use it at once
 * Works on Linux and Windows (Cygwin is needed to run on Windows)
 * Easy and interactive TUI (Text User Interface)
 * Written in Python. Completely opensource.
