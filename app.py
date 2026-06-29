import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Customer Retention Analytics",
    layout="wide"
)


st.title("🏦 Customer Engagement & Product Utilization Analytics")
st.subheader("Bank Customer Retention Strategy Dashboard")


# ==========================
# DATA UPLOAD
# ==========================

st.sidebar.header("📂 Dataset Upload")


uploaded_file = st.sidebar.file_uploader(
    "Upload Customer CSV",
    type=["csv"]
)


if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.sidebar.success(
        "Custom Dataset Loaded"
    )

else:

    df = pd.read_csv(
        "data/European_Bank.csv"
    )

    st.sidebar.info(
        "Using Default Dataset"
    )



# ==========================
# FILTERS
# ==========================

st.sidebar.header("🔎 Filters")


country = st.sidebar.multiselect(

    "Geography",

    df["Geography"].unique(),

    default=df["Geography"].unique()

)



product_count = st.sidebar.slider(

    "Minimum Products",

    min_value=int(df["NumOfProducts"].min()),

    max_value=int(df["NumOfProducts"].max()),

    value=1

)



df = df[

(df["Geography"].isin(country))

&

(df["NumOfProducts"] >= product_count)

]



# ==========================
# CUSTOMER RISK SCORE
# ==========================


def risk_score(row):

    score = 0


    # inactive
    if row["IsActiveMember"] == 0:
        score += 40


    # only one product
    if row["NumOfProducts"] == 1:
        score += 25


    # high balance
    if row["Balance"] > 100000:
        score += 25


    # old customer but inactive
    if row["Tenure"] >= 5 and row["IsActiveMember"] == 0:
        score += 10


    return score



df["Risk_Score"] = df.apply(
    risk_score,
    axis=1
)



def risk_category(x):

    if x >= 70:
        return "High Risk"

    elif x >= 40:
        return "Medium Risk"

    else:
        return "Low Risk"



df["Risk_Level"] = df["Risk_Score"].apply(
    risk_category
)



# ==========================
# CUSTOMER OFFER
# ==========================


def offer(row):


    if row["Risk_Level"]=="High Risk" and row["Balance"]>100000:

        return "Premium Loyalty Program + Personal Banker"


    elif row["NumOfProducts"]==1:

        return "Offer Credit Card / Additional Products"


    elif row["IsActiveMember"]==0:

        return "Cashback + Engagement Campaign"


    else:

        return "Reward Points"



df["Recommended_Offer"] = df.apply(
    offer,
    axis=1
)



# ==========================
# TABS
# ==========================


tab1,tab2,tab3,tab4,tab5 = st.tabs(

[
"📊 Overview",
"👥 Engagement",
"🏦 Product Usage",
"🚨 Risk Customers",
"🎁 Retention Offers"
]

)



# ==========================
# OVERVIEW
# ==========================


with tab1:


    st.header("Bank Overview")


    c1,c2,c3,c4 = st.columns(4)



    c1.metric(
        "Total Customers",
        len(df)
    )


    c2.metric(
        "Customers Left",
        int(df["Exited"].sum())
    )


    c3.metric(
        "Active Customers",
        len(df[df["IsActiveMember"]==1])
    )


    c4.metric(
        "Inactive Customers",
        len(df[df["IsActiveMember"]==0])
    )



    st.subheader(
        "Customer Data"
    )


    st.dataframe(df)



# ==========================
# ENGAGEMENT
# ==========================


with tab2:


    st.header(
        "Customer Engagement Analysis"
    )



    fig,ax = plt.subplots()


    sns.countplot(

        data=df,

        x="IsActiveMember",

        hue="Exited",

        ax=ax

    )


    ax.set_xticklabels(

        [
        "Inactive",
        "Active"
        ]

    )


    st.pyplot(fig)



    st.info(

    "Inactive customers have higher churn risk"

    )


    st.subheader(
        "Long Term Customers"
    )


    long_customers = df[
        df["Tenure"]>=5
    ]


    st.dataframe(

        long_customers[

        [
        "CustomerId",
        "Tenure",
        "Balance",
        "IsActiveMember"

        ]

        ]

    )



# ==========================
# PRODUCT
# ==========================


with tab3:


    st.header(
        "Product Utilization Analysis"
    )



    product = (

        df.groupby(
            "NumOfProducts"
        )
        ["Exited"]
        .mean()

    )



    st.bar_chart(product)



    st.write(

    """
    Insight:

    More products usually create stronger
    customer relationship.

    """

    )



# ==========================
# RISK CUSTOMERS
# ==========================


with tab4:


    st.header(
        "🚨 Customers Who May Leave"
    )



    sort_option = st.radio(

        "Risk Sorting",

        [
        "High Risk → Low Risk",
        "Low Risk → High Risk"
        ]

    )



    if sort_option=="High Risk → Low Risk":


        risk_df=df.sort_values(

            "Risk_Score",

            ascending=False

        )


    else:


        risk_df=df.sort_values(

            "Risk_Score",

            ascending=True

        )



    st.dataframe(

        risk_df[

        [

        "CustomerId",
        "Surname",
        "Balance",
        "Tenure",
        "NumOfProducts",
        "IsActiveMember",
        "Risk_Score",
        "Risk_Level"

        ]

        ]

    )



# ==========================
# OFFERS
# ==========================


with tab5:


    st.header(
        "🎁 Recommended Retention Strategy"
    )



    st.dataframe(

        df[

        [

        "CustomerId",
        "Surname",
        "Risk_Level",
        "Recommended_Offer"

        ]

        ]

    )



st.success(
"Customer retention analysis completed successfully"
)