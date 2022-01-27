# SETUP INSTRUCTIONS
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `brew install --cask wkhtmltopdf` (M1 Mac)

# TO RUN: 

- `python3 buildletter.py --filepath='my_big_subscription_csv.csv'`

This will dump all pdfs into the `final_pdfs/` directory. This will also dump several csvs into the `csv/` directory. These csvs are named according to the order types in `my_big_subscription_csv.csv`. 

This takes quite a while to run, so just hit enter and come back later. If for whatever reason you want to stop it, you have to kill the entire terminal window (so sorry)