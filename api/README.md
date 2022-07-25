# How to Populate Prof Prefs
You must do this everytime you restart the Docker DB!

1. Run api either locally or with docker
2. call the GET `/courses` and GET `/professors` endpoints. This creates two files curr_courses.json and curr_professors.json in /populate_prof_prefs.
3. Navigate to the `populate_prof_prefs` folder
4. Run `python3 prof_pref_inputter.py`
5. Now all professors should have preferences!

## Generate historical preferences
By default it will generate prof prefs for 2022 and 2021
Run step 4 command according to this template:
`python3 prof_pref_inputter.py <latest year> <num history preferences>`
For example:
`python3 prof_pref_inputter.py 2022 2`
This will produce 2022 and 2021 prefs for all profs


