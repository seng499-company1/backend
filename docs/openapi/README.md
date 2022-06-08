# Documentation
This documentation may be a good example of overengineering a simple problem. Currently you must run the documentation locally to view it. Eventually it will be hosted somewhere. 
## How to view documentation locally
1. Navigate to /openapi folder
2. Run
    ```
    redocly preview-docs bundled.yaml
    ```
3. Navigate to http://127.0.0.1:8080 to view documentation. 

## Things to Know
- Located in /paths there are folders for each API endpoint [admins, professors, courses, schedules]
    - There are yaml files for each endpoint
    - All posts, gets, puts, deletes for the same URI are located in the same YAML file.
- Components are located in /components/schemas and are used to model what input/output data the API is looking for.
- There should be documentation for each endpoint. Currently we are just missing documentation for some of the /schedules endpoints as I assume this will change in the next couple days. 

## How to edit the documentation
1. Make edits in whatever files you need to
2. From the /openapi folder, run
    ```
    redocly bundle openapi.yaml --output bundled.yaml
    ```
    fix any issues this detects, if none continue

3. Run
    ```
    redocly lint bundled.yaml
    ```
    fix any issues this detects, if non continue

4. Run
    ```
    redocly preview-docs bundled.yaml
    ```

5. Navigate to http://127.0.0.1:8080 to view documentation


