# Quorum-interview

### Instructions for Running the Script

#### 1. **Ensure Python is Installed**

-   Install Python version **3.11 or higher**. To check the version, run:
    ```bash
    python --version
    ```
-   If Python is not installed, download it from the [official website](https://www.python.org/downloads/) and follow the installation instructions.

#### 2. **Install Dependencies**

-   Navigate to the `project` directory:
    ```bash
    cd path/to/project
    ```
-   No additional dependencies are required as the script uses only standard Python libraries.

#### 3. **Verify the File Structure**

-   Ensure the project structure matches the following:
    ```
    project/
    ├── data/
    │   ├── bills.csv
    │   ├── legislators.csv
    │   ├── votes.csv
    │   ├── vote_results.csv
    ├── output/
    ├── src/
    │   ├── reader.py
    │   └── main.py
    ```

#### 4. **Add Files to the `data` Directory**

-   Place the following files in the `data/` directory:
    -   `bills.csv`
    -   `legislators.csv`
    -   `votes.csv`
    -   `vote_results.csv`

#### 5. **Run the Script**

-   Execute the following command to run the script:
    ```bash
    python src/main.py
    ```
-   The script will:
    1.  Read the data from the files in the `data/` directory.
    2.  Process the data.
    3.  Create two output files in the `output/` directory:
        -   `legislators-support-oppose-count.csv`
        -   `bills-support-oppose-count.csv`

#### 6. **Check the Output Files**

-   Open the `output/` directory and verify that the output files are created:
    ```
    project/output/
    ├── legislators-support-oppose-count.csv
    ├── bills-support-oppose-count.csv
    ```

---

### Common Issues and Solutions

1. **Python is not installed or accessible**:

    - Install Python or add it to the system PATH variable.

2. **Error: `ModuleNotFoundError: No module named 'reader'`**:

    - Ensure the current working directory is set to the root of the `project/`. If not, run:
        ```bash
        cd path/to/project
        ```

3. **Error accessing files in `data/*.csv`**:

    - Verify that `bills.csv`, `legislators.csv`, `votes.csv`, and `vote_results.csv` exist and contain valid data.

4. **The `output/` folder is missing**:
    - The script will automatically create the `output/` folder if it does not exist. Ensure you have write permissions for the `project` directory.

---

Now you are ready to run the script and process the data! 🎉
