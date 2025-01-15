### 1. **Discuss your solution’s time complexity. What tradeoffs did you make?**

#### Time Complexity:

-   **`process_legislators_data`**:

    -   Initial dictionary creation: \(O(L)\), where \(L\) is the number of legislators.
    -   Mapping votes to results: \(O(V_r)\), where \(V_r\) is the number of vote results.
    -   Iterating through votes: \(O(V)\), where \(V\) is the number of votes.
    -   Overall: \(O(L + V_r + V)\).

-   **`process_bills_data`**:
    -   Initial dictionary creation: \(O(B)\), where \(B\) is the number of bills.
    -   Mapping votes to results: \(O(V_r)\).
    -   Iterating through votes: \(O(V)\).
    -   Overall: \(O(B + V_r + V)\).

#### Tradeoffs:

-   The solution prioritizes **readability and maintainability** over absolute optimization. For instance:
    -   We used dictionaries for quick lookups, which increases memory usage but improves performance for large datasets.
    -   Processing votes for legislators and bills separately avoids interdependencies, making the logic modular and easier to debug, but it duplicates the work of mapping votes to their results.

---

### 2. **How would you change your solution to account for future columns that might be requested, such as “Bill Voted On Date” or “Co-Sponsors”?**

#### Approach:

1. **Use Data Classes or Objects**:

    - Introduce `Legislator` and `Bill` data classes to encapsulate attributes like "Bill Voted On Date" or "Co-Sponsors."

2. **Dynamic Field Handling**:

    - Store additional fields dynamically using a generic dictionary or a configuration file to specify expected columns.

3. **Leverage SQL/ORMs**:

    - Transition from CSV processing to a database where adding columns is trivial.
    - Use an ORM like SQLAlchemy or Django ORM to model data and fetch necessary fields dynamically.

4. **Adapt the CSV Writing Logic**:
    - Dynamically generate `field_names` based on the attributes of objects.

---

### 3. **How would you change your solution if instead of receiving CSVs of data, you were given a list of legislators or bills that you should generate a CSV for?**

#### Approach:

1. **Convert CSV Parsing to List Input**:

    - Assume the input is directly passed as Python objects (e.g., lists of dictionaries or data classes).

2. **Adapt `DataReader`**:

    - Replace `DataReader.read_csv()` with a function that accepts a list and validates its structure.

3. **Update Writing Logic**:

    - Adjust the `write_csv` function to accept lists of dictionaries or objects directly.

---

### 4. **How long did you spend working on the assignment?**

-   Approximately **1.5–2 hours**:
    -   Understanding the requirements and designing the solution: **30 minutes**.
    -   Writing the initial implementation with type hints and comments: **30–45 minutes**.
    -   Testing, debugging, and refining the solution: **30 minutes**.
