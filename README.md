# Insider Career Page Test Automation

## Introduction

This project is designed to automatically test the career page of Insider. Developed using Selenium and Python 3.11, this test automation checks the following core functionalities:

- Correct loading of the career page
- Presence and content of the job list
- Filtering of Quality Assurance positions in Istanbul location
- Functionality of "View Role" buttons
- Creates and processes LOG files on a daily basis

## Usage

Follow these steps to run the project on your local machine:

1. Clone the repository:
```
git clone https://github.com/ac0z/InsiderTestCase.git
```
2. Navigate to the project directory:

```
cd InsiderTestCase
```
3. Install the required Python packages:
```
pip install -r requirements.txt
```

4. Run the test:
```
python -m unittest tests/test_insider_careers.py
```

Note: You need to have Python and Chrome browser installed on your system to run this test.

## Results

This test automation verifies the core functionalities of Insider's career page. When the test is successful, the following checks are confirmed:

- The career page loaded correctly
- The job list is present and not empty
- Quality Assurance positions in Istanbul are correctly filtered
- All "View Role" buttons are working and redirecting to the correct page

In case of any errors, the test will provide detailed error messages. These messages help in quickly identifying and rectifying issues.

---

For more information about this project, please [contact us](mailto:alicemozkara@gmail.com).
