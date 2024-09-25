import streamlit as st
import pandas as pd


federal_income_tax_brackets = {
    11600: 0.10,
    47150: 0.12,
    100525: 0.22,
    191950: 0.24,
    243725: 0.32,
    609350: 0.35,
    float("inf"): 0.37,
}


def federalTaxAdjustedInvestmentReturn(investment_return, annual_income):
    total_income = investment_return + annual_income
    total_taxes = 0
    left_over_income_to_tax = total_income

    for key in sorted(federal_income_tax_brackets.keys()):
        if left_over_income_to_tax > key:
            tax = key * federal_income_tax_brackets[key]
            left_over_income_to_tax -= key
            total_taxes += tax
        else:
            total_taxes += left_over_income_to_tax * federal_income_tax_brackets[key]
            break

    return total_taxes * (investment_return / (investment_return + annual_income))


california_income_tax_brackets = {
    10412: 0.01,
    24784: 0.02,
    38959: 0.04,
    54081: 0.06,
    68350: 0.08,
    349137: 0.093,
    418961: 0.103,
    698271: 0.113,
    float("inf"): 0.123,
}


def stateTaxAdjustedInvestmentReturn(investment_return, annual_income):
    total_income = investment_return + annual_income
    total_taxes = 0
    left_over_income_to_tax = total_income

    for key in sorted(california_income_tax_brackets.keys()):
        if left_over_income_to_tax > key:
            tax = key * california_income_tax_brackets[key]
            left_over_income_to_tax -= key
            total_taxes += tax
        else:
            total_taxes += left_over_income_to_tax * california_income_tax_brackets[key]
            break

    return total_taxes * (investment_return / (investment_return + annual_income))


def show():
    annual_income = st.number_input("Annual Income", value=100000)
    principal_amount = st.number_input("Principal Amount", value=10000)
    number_of_years = st.number_input("Number of Years", value=10)

    taxes = [
        "Federal Income Tax",
        "Federal Income Tax",
        "Federal Income Tax",
        "Federal Income Tax",
        "Federal Income Tax",
        "State and Federal Income Tax",
        "State and Federal Income Tax for interest and capital gains for appreciation",
        "State and Federal Income Tax for interest and capital gains for appreciation",
        "State Income tax",
        "State Income tax",
        "State Income tax",
        "State and Federal Income Tax for interest and capital gains for appreciation",
        "State and Federal Income Tax for interest and capital gains for appreciation",
        "State and Federal Income Tax for interest and capital gains for appreciation",
        "State and Federal Income Tax for interest and capital gains for appreciation",
    ]

    bonds = {
        "Type": [
            "3 month Treasury bills",  # https://www.bloomberg.com/markets/rates-bonds/government-bonds/us
            "6 month Treasury bills",
            "10 year Treasury notes",
            "30 year Treasury bonds",
            "Series I Savings Bonds",  # https://www.treasurydirect.gov/savings-bonds/i-bonds/i-bonds-interest-rates/#:~:text=The%20composite%20rate%20for%20I,through%20October%202024%20is%204.28%25.
            "CDs (Alto bank)",  # https://www.bankrate.com/banking/cds/cd-rates/
            "Money-market funds (SNAXX)",  # https://www.schwab.com/money-market-funds
            "Mortgage debt/mortgage-backed securities(MBS)",  # https://www.ishares.com/us/products/239465/ishares-mbs-etf
            "1-yr Municipal bonds",
            "5-yr Municipal bonds",
            "10-yr Municipal bonds",
            # "Preferred stock",
            'High-yield ("junk") bonds (JNK)',  # https://finance.yahoo.com/quote/JNK/ or FRED https://fred.stlouisfed.org/series/BAMLH0A0HYM2EY
            "Emerging-markets debt",
            # BTC Lending
            "USDC Lending",
            # REIT returns
            "VTEB",
        ],
        "Yield": [
            4.65,
            4.46,
            3.74,
            4.08,
            4.28,
            4.5,
            5.09,
            5.08,
            2.45,
            2.39,
            3.54,
            6.66,
            3.95,
            5.20,
            3.26,
        ],
        "Total Return": [],
        "Total Return after Taxes": [],
        "Price": [
            4.54,
            4.31,
            101.09,
            102.86,
            None,
            None,
            None,
            96.21,
            None,
            None,
            None,
            97.74,
            None,
            1,
            51.04,
        ],
        "Expense Ratio": [
            None,
            None,
            None,
            None,
            None,
            None,
            0.0019,
            None,
            None,
            None,
            None,
            0.0040,
            None,
            None,
            0.005,
        ],
        "Source": [
            "https://www.bloomberg.com/markets/rates-bonds/government-bonds/us",
            "https://www.bloomberg.com/markets/rates-bonds/government-bonds/us",
            "https://www.bloomberg.com/markets/rates-bonds/government-bonds/us",
            "https://www.bloomberg.com/markets/rates-bonds/government-bonds/us",
            "https://www.treasurydirect.gov/savings-bonds/i-bonds/i-bonds-interest-rates/#:~:text=The%20composite%20rate%20for%20I,through%20October%202024%20is%204.28%25.",
            "https://www.bankrate.com/banking/cds/cd-rates/",
            "https://www.schwab.com/money-market-funds",
            "https://www.ishares.com/us/products/239465/ishares-mbs-etf",
            "https://www.bloomberg.com/markets/rates-bonds/government-bonds/us",
            "https://www.bloomberg.com/markets/rates-bonds/government-bonds/us",
            "https://www.bloomberg.com/markets/rates-bonds/government-bonds/us",
            # "Preferred stock",
            "https://finance.yahoo.com/quote/JNK/",  # or FRED https://fred.stlouisfed.org/series/BAMLH0A0HYM2EY
            "https://fred.stlouisfed.org/series/BAMLEMHBHYCRPIOAS",
            "https://www.coinbase.com/usdc",
            "https://investor.vanguard.com/investment-products/etfs/profile/vteb",
        ],
    }

    for i in range(len(bonds["Type"])):
        apr: float = bonds["Yield"][i]
        if bonds["Expense Ratio"][i] != None:
            apr = bonds["Yield"][i] - bonds["Expense Ratio"][i]

        total_return_on_investment = principal_amount
        cumulative_taxes_paid = 0

        for year in range(1, number_of_years + 1):
            annual_return = total_return_on_investment * (apr / 100)

            federal_tax = federalTaxAdjustedInvestmentReturn(
                annual_return, annual_income
            )
            state_tax = stateTaxAdjustedInvestmentReturn(annual_return, annual_income)

            if taxes[i] == "Federal Income Tax":
                annual_return_after_tax = annual_return - federal_tax
            elif taxes[i] == "State Income tax":
                annual_return_after_tax = annual_return - state_tax
            elif taxes[i] in [
                "State and Federal Income Tax",
                "State and Federal Income Tax for interest and capital gains for appreciation",
            ]:
                annual_return_after_tax = annual_return - federal_tax - state_tax

            total_return_on_investment += annual_return_after_tax
            cumulative_taxes_paid += federal_tax + state_tax

        final_return = total_return_on_investment - principal_amount
        bonds["Total Return"].append(
            (principal_amount * (1 + apr / 100) ** number_of_years) - principal_amount
        )

        # Subtract the taxes from the total return
        bonds["Total Return after Taxes"].append(final_return)

    df = pd.DataFrame(bonds)
    df.index = df.index + 1

    st.dataframe(df, use_container_width=True)
