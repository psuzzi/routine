# Python scripts

Set of python scripts to manage the application

## Setup

1. Ensure you have Python 3.6+ installed.

2. Set up a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Unix or MacOS:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
   I had issues with the requirements due to the new version of Cython. To solve them, I did:
   ```
   PIP_CONSTRAINT="Cython<3" pip install -r requirements.txt

   

Note:
If you have issues with the requirements, it could be related to the new version of Cython

```
❯ echo "Cython<3" > cython_constraint.txt
❯ PIP_CONSTRAINT=cython_constraint.txt pip install -r requirements.txt
```