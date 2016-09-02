Project Migration Checklist
===========================
This project is a migration and refactoring of an old project, the files of which are listed below and the functionality of which will all need to be migrated

File List
=========
* (done) Interface.py - For external interaction
* Model.py - Endpoint helper
    * ModelGoogle.py - Interact with the Google API
    * ModelHere.py - Interact with the Interface
    * ModelSims.py - Interact with the Sims CLR
        * *.RptDef - Sims report definition files
* Arc2Sync.py - Controller
    * sync.bat - For easy provision of arguments
* (done) Sync.py - Item helper
    * SyncCourses.py - Course Item
    * SyncStaff.py - Staff Item
    * SyncStudents.py - Student Item
    * SyncUsers.py - User Item
        * swearwords.txt - A list of naughty words, for password & username filtering
* (done) Settings.py - For the gathering of settings
* (done) notes.txt - just a brain dump file
* (done) usernames.txt - just a brain dump file
* (done) client_secret.json - API keys from Google
* (done) readme.txt - instructions on install and use