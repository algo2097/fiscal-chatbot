import openai

secret_key = "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"

openai.api_key = secret_key


def generate_gpt_response(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content


def get_total_revenue(data, company, year):
    records = data[(data['Company'] == company) &
                   (data['Year'] == year)]['Total Revenue'].reset_index(drop=True)

    if not records.empty:
        if len(records) == 1:
            prompt = (
                f"Provide me a brief statement as response for Revenue of {company} "
                f"for the year {year}. Where the revenues are {records[0]} million dollars respectively. Also make "
                f"the figures readable")
            print(prompt)

            response = generate_gpt_response(prompt)
            return response
    else:
        return "No data found"


def get_revenue_change(data, company):
    records = data[data['Company'] == company].sort_values(by='Year', ascending=False).head(3)
    prompt = "Provide a brief Analysis for the following, "
    if not records.empty:
        records = records[records['Revenue Growth(%)'] != 0].reset_index(drop=True)
        for index, record in records.iterrows():
            year = record["Year"]
            revenue = record["Total Revenue"]
            revenue_growth = record["Revenue Growth(%)"]
            sub_prompt = fr"For year {year}, revenue was {revenue} and change from last year i.e ({year - 1}) was {revenue_growth}. "
            prompt = prompt + sub_prompt
        prompt = prompt + "Make the figures more readable."
        response = generate_gpt_response(prompt)
        return response
    return "No data found"


def get_net_income(data, company, year):
    records = data[(data['Company'] == company) &
                   (data['Year'] == year)]['Net Income'].reset_index(drop=True)
    if not records.empty:
        prompt = (
            f"Provide me a brief statement as response for Net Income of {company} "
            f"for the year {year}. Where the Income is {records[0]} million dollars respectively. Also make "
            f"the figures readable")
        response = generate_gpt_response(prompt)
        return response
    else:
        return "No data found"


def get_income_change(data, company):
    records = data[data['Company'] == company].sort_values(by='Year', ascending=False).head(3)
    prompt = "Provide a brief Analysis for the following, "
    if not records.empty:
        records = records[records['Revenue Growth(%)'] != 0].reset_index(drop=True)
        for index, record in records.iterrows():
            year = record["Year"]
            income = record["Net Income"]
            income_change = record["Income Growth(%)"]
            sub_prompt = fr"For year {year}, income was {income} and change from last year i.e ({year - 1}) was {income_change}. "
            prompt = prompt + sub_prompt
        prompt = prompt + "Make the figures more readable."
        response = generate_gpt_response(prompt)
        return response
    return "No data found"


def get_total_assets(data, company, year):
    records = data[(data['Company'] == company) &
                   (data['Year'] == year)]['Total Assets'].reset_index(drop=True)
    if not records.empty:
        prompt = (
            f"Provide me a brief statement as response for Total Assets Value of {company} "
            f"for the year {year}. Where the Assets Values is {records[0]} million dollars respectively. Also make "
            f"the figures readable")
        response = generate_gpt_response(prompt)
        return response
    return "No data found"


def get_total_liabilities(data, company, year):
    records = data[(data['Company'] == company) &
                   (data['Year'] == year)]['Total Liabilities'].reset_index(drop=True)
    if not records.empty:
        prompt = (
            f"Provide me a brief statement as response for Total Liabilities Value of {company} "
            f"for the year {year}. Where the Liabilities Values is {records[0]} million dollars respectively. Also make "
            f"the figures readable")
        response = generate_gpt_response(prompt)
        return response
    return "No data found"


def get_cash_flow(data, company, year):
    records = data[(data['Company'] == company) &
                   (data['Year'] == year)]['Cash Flow from Operations'].reset_index(drop=True)
    if not records.empty:
        prompt = (
            f"Provide me a brief statement as response for Total Cash Flow from Operations Value of {company} "
            f"for the year {year}. Where the Cash Flow Values is {records[0]} million dollars respectively. Also make "
            f"the figures readable")
        response = generate_gpt_response(prompt)
        return response
    return "No data found"


def get_revenue_to_assets_ratio(data, company, year):
    records = data[(data['Company'] == company) &
                   (data['Year'] == year)]['RevToAssets'].reset_index(drop=True)
    if not records.empty:
        prompt = (
            f"Provide me a brief statement as response for Revenue to Assets Ratio Value i.e. {records[0]} of {company} "
            f"for the year {year}. Also make the figures readable")
        response = generate_gpt_response(prompt)
        return response
    return "No data found"


def get_income_to_liabilities_ratio(data, company, year):
    records = data[(data['Company'] == company) &
                   (data['Year'] == year)]['IncToLiabilities'].reset_index(drop=True)
    if not records.empty:
        prompt = (
            f"Provide me a brief statement as response for Income to Liabilities Ratio Value i.e. {records[0]} of {company}"
            f"for the year {year}. Also make the figures readable")
        response = generate_gpt_response(prompt)
        return response
    return "No data found"


def compare_revenue(data, company_a, company_b, year):
    records_a = data[data['Company'] == company_a][['Year', 'Total Revenue']]
    records_b = data[data['Company'] == company_b][['Year', 'Total Revenue']]
    if not records_a.empty and not records_b.empty:
        merged = records_a.merge(records_b, on='Year', suffixes=(f'_{company_a}', f'_{company_b}'))
        target_record = merged[merged['Year'] == year].reset_index(drop=True)
        revenue_a = target_record[f'Total Revenue_{company_a}'].values[0]
        revenue_b = target_record[f'Total Revenue_{company_b}'].values[0]
        prompt = (
            f"Provide me a snippet of statements as response for comparing the Revenue of companies {company_a} and {company_b} "
            f"for the year {year}. Where the revenues are {revenue_a} and {revenue_b} million dollars respectively. Also make the figures readable")

        response = generate_gpt_response(prompt)
        return response
    return "No data found"
