# AI Phishing Email Detector
This is a small cybersecurity project that uses machine learning to detect whether an email looks like a phishing email or a legitimate email.
I built this project using Python and Scikit-learn. The application has a simple Streamlit interface where an email subject and body can be entered and analyzed.

## What it does
- Takes an email subject and body as input
- Cleans the email text
- Converts the text into numerical features using TF-IDF
- Uses Logistic Regression to classify the email
- Shows a phishing risk score
- Shows some common warning signs found in the email

## How it works
Email
  ↓
Text Cleaning
  ↓
TF-IDF
  ↓
Logistic Regression
  ↓
Phishing / Legitimate
  ↓
Risk Score + Warning Signs

## Technologies Used
* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Joblib
* Streamlit

## Project Structure
```text
AI-Phishing-Email-Detector/
│
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
│
├── data/
│   └── emails.csv
│
└── models/
    ├── phishing_model.joblib
    ├── metrics.json
    ├── confusion_matrix.png
    └── test_predictions.npy
```

## How to Run
First install the required packages:
```bash
pip install -r requirements.txt
```
Train the model:
```bash
python train_model.py
```
Run the application:
```bash
streamlit run app.py
```
The application will then open in the browser.

## Example

### Phishing email
**Subject:**
```text
Urgent account verification
```
**Body:**
```text
Your account will be suspended immediately.
Verify your password by clicking the link.
```
The application should identify this as a phishing email and show the warning signs it found.

### Legitimate email
**Subject:**
```text
Team meeting
```
**Body:**
```text
Hello team, please review the agenda for tomorrow's meeting.
```
This should normally be classified as a legitimate email.

## Model
The project uses TF-IDF to convert email text into numerical features.
A Logistic Regression model is then trained on these features to classify emails.
The model is evaluated using:
* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix
The current dataset gives very high results because it is a small synthetic dataset with relatively simple examples. These results should not be considered representative of real-world phishing detection.

## Limitations
This is a basic project and it mainly looks at the text of the email.
It does not currently check:
* Email headers
* Sender reputation
* Actual URL reputation
* Attachments
* SPF/DKIM/DMARC
* Domain age
A real phishing detection system would need more information than just the email text.

## Future Improvements
Some improvements I would like to make later:
* Use a larger real-world dataset
* Add URL and domain analysis
* Analyze email headers
* Detect suspicious attachments
* Improve the explanation of predictions
* Add email file upload
* Explore Gmail API integration

## Disclaimer
This project is made for learning and demonstration purposes.
It should not be used as the only method for deciding whether a real email is safe.
