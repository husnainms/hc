import streamlit as st
# from scraper import scrape_company_data, scrape_email_from_url
# import json

# def main():
#     st.title("Company Data Scraper")
#     usdot_code = st.number_input("Enter US DOT Code", value=0, step=1)
#     if st.button("Fetch Company Details"):
#         if usdot_code:
#             company_details = scrape_company_data(usdot_code)
#             email = scrape_email_from_url(usdot_code)
#             if company_details:
#                 st.write("Company Details:")
#                 st.write(f"Name: {company_details['legal_name']}")
#                 st.write(f"Email: {email}")
#                 st.write(f"Physical Address: {company_details['physical_address']}")
#                 st.write(f"Mailing Address: {company_details['mailing_address']}")
#                 st.write(f"Phone: {company_details['phone']}")
#                 st.write(f"Operational Status: {company_details['operating_status']}")
#                 st.write("United States Inspections:")
#                 us_inspections = company_details['us_inspections']
#                 for inspection_type, inspection_data in us_inspections.items():
#                     st.write(f"- {inspection_type.capitalize()}:")
#                     st.write(f"  Out of Service: {inspection_data['out_of_service']}")
#                     st.write(f"  Inspections: {inspection_data['inspections']}")
#                     st.write(f"  Out of Service Percent: {inspection_data['out_of_service_percent']}")
#                     st.write(f"  National Average: {inspection_data['national_average']}")
#                 st.write("United States Crashes:")
#                 us_crashes = company_details['united_states_crashes']
#                 st.write(f"- Injury: {us_crashes['injury']}")
#                 st.write(f"- Total: {us_crashes['total']}")
#                 st.write(f"- Fatal: {us_crashes['fatal']}")
#                 st.write(f"- Tow: {us_crashes['tow']}")
#                 st.write(f"URL: {company_details['url']}")
#                 st.write(f"Latest Update: {company_details['latest_update']}")
#                 # Display more details
#             else:
#                 st.write("Company not found or an error occurred.")

# if __name__ == "__main__":
#     main()

# import streamlit as st
# import pandas as pd
# from scraper import scrape_company_data, scrape_email_from_url

import streamlit as st
import pandas as pd
import json
import aiohttp
import asyncio
from scraper import scrape_company_data, scrape_email_from_url
from datetime import datetime  # Import datetime for date parsing

async def fetch_data(usdot_code, session):
    try:
        company_details = scrape_company_data(usdot_code)
        email = scrape_email_from_url(usdot_code)
        return usdot_code, company_details, email
    except Exception as e:
        # Handle the exception (e.g., log it, display an error message)
        return usdot_code, None, None

async def main():
    st.title("Company Data Scraper")

    # Step 1: Load DOT numbers from an Excel file
    uploaded_file = st.file_uploader("Upload an Excel file containing DOT numbers", type=["xlsx"])
    dot_numbers = []

    if uploaded_file is not None:
        df_input = pd.read_excel(uploaded_file)
        dot_numbers = df_input["USDOT Number"].tolist()

        # Initialize df_output for storing fetched data
        df_output = pd.DataFrame(columns=["USDOT Number", "Company Name", "Email", ...])

        # Initialize a flag to check if data has already been fetched and saved
        data_fetched_and_saved = False

        # Check if the "Download Updated Excel" button has been clicked
        if st.button("Download Updated Excel") and not data_fetched_and_saved:
            async with aiohttp.ClientSession() as session:
                tasks = [fetch_data(usdot_code, session) for usdot_code in dot_numbers]
                results = await asyncio.gather(*tasks)

            for usdot_code, company_details, email in results:
                if company_details:
                    operational_status = company_details.get('operating_status', '')
                    if operational_status == 'AUTHORIZED FOR Property':
                        data = {
                            "USDOT Number": [usdot_code],
                            "Company Name": [company_details["legal_name"]],
                            "Email": [email],
                            # Add more columns as needed
                        }
                        df_output = pd.concat([df_output, pd.DataFrame(data)], ignore_index=True)
                        st.success(f"Data for DOT {usdot_code} fetched and saved.")
                    else:
                        st.warning(f"DOT {usdot_code} is not 'AUTHORIZED FOR Property' and will be ignored.")

            data_fetched_and_saved = True  # Set the flag to True after data is fetched and saved

        # Allow users to download the updated Excel file
        if data_fetched_and_saved:
            updated_excel_file = "updated_company_data.xlsx"
            df_output.to_excel(updated_excel_file, index=False)
            st.success(f"Data saved to '{updated_excel_file}'")

if __name__ == "__main__":
    asyncio.run(main())






# Input range for MC/MX Number and also handling for null data. Skip null in this
# Fetch in batches of 10k


# Entity Type:	CARRIER  
# Operating Status:	AUTHORIZED FOR Property	Out of Service Date:	None
# Legal Name:	IRELAND SOLUTION INC 
# DBA Name:	JT GLOBAL LOAD TRUCKING 
# Physical Address:	8383 WILSHIRE BLVD SUITE 800
# BEVERLY HILLS , CA   90211  
# Phone:	(213) 278-7120  
# Mailing Address:	8383 WILSHIRE BLVD SUITE 800
# BEVERLY HILLS , CA   90211  
# USDOT Number:	3423627 	State Carrier ID Number:	 
# MC/MX/FF Number(s):	MC-1107367
#  	DUNS Number:	-- 
# Power Units:	1 	Drivers:	1 
# MCS-150 Form Date:	07/27/2022 	MCS-150 Mileage (Year):	600 (2021) 

# Other information for this carrier
# SMS Results (Carrier Registration) -----> Carrier registration details ------> Email