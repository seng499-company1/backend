# How to Populate Prof Prefs
You must do this everytime you restart the Docker DB!

- Run api either locally or with docker
- call the GET `/courses` and GET `/professors` endpoints. This creates two files curr_courses.json and curr_professors.json in /populate_prof_prefs.
- Navigate to the `populate_prof_prefs` folder
- Run `python3 prof_pref_inputter.py`
- Now all professors should have preferences!
