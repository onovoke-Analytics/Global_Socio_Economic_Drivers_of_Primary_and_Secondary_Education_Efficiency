#!/usr/bin/env python
# coding: utf-8

# In[13]:


#Global Primary & Secondary Education Indicators Analysis


# In[14]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# In[15]:


df = pd.read_csv(r"C:\Users\Samson\Desktop\Education Indicators Analysis.csv")
df.columns = df.columns.str.strip()


# In[16]:


df["GDP_per_Capita"] = df["GDP"] / df["Population"]
df["Secondary_to_Primary_Ratio"] = (
    df["Enrolment in Secondary Education"]
    / df["Enrolment in Primary Education"]
)
df["Out_of_School_Rate"] = (
    df["Out-of-School Children of Primary School"] / df["Population"]
) * 100


# In[17]:


# Drop rows where ALL columns are empty
df_cleaned = df.dropna(how="all")


# In[18]:


df


# In[20]:


#Top 10 Countries with Highest Primary Repetition Rates

top_repeaters = df.nlargest(10, "% of Repeaters in Primary Education")[
    ["Country Name", "% of Repeaters in Primary Education"]
]
print(top_repeaters)


# In[21]:


#Visualization

plt.figure(figsize=(10, 5))
sns.barplot(
    data=top_repeaters,
    x="% of Repeaters in Primary Education",
    y="Country Name",
    hue="Country Name",
    palette="Reds_r",
    legend=False,
)

plt.title("Top 10 Countries by Primary Education Repetition Rate")
plt.xlabel("Repetition Rate (%)")
plt.ylabel("Country")
plt.tight_layout()
plt.show()


# In[25]:


#Secondary-to-Primary Enrolment Transition Ratio

df["Secondary_to_Primary_Ratio"] = (
    df["Enrolment in Secondary Education"]
    / df["Enrolment in Primary Education"]
)
clean_data = df["Secondary_to_Primary_Ratio"].replace(
    [np.inf, -np.inf], np.nan
).dropna()


# In[26]:


#Visualization

plt.figure(figsize=(8, 5))
sns.histplot(clean_data, kde=True, bins=20, color="teal")

plt.axvline(
    clean_data.median(),
    color="red",
    linestyle="--",
    label=f"Median: {clean_data.median():.2f}",
)

plt.title("Distribution of Secondary-to-Primary Enrolment Ratio")
plt.xlabel("Ratio (Secondary Enrolment / Primary Enrolment)")
plt.ylabel("Count")
plt.legend()
plt.tight_layout()
plt.show()


# In[31]:


#Out-of-School Children Ratio per Capita

top_out_of_school = df.nlargest(10, "Out_of_School_Rate")[
    ["Country Name", "Out_of_School_Rate"]
]
print(top_out_of_school)


# In[38]:


#Visualization

plt.figure(figsize=(10, 5))
sns.barplot(
    data=top_out_of_school,
    x="Out_of_School_Rate",
    y="Country Name",
    hue="Country Name",
    palette="Oranges_r",
    legend=False,
)

plt.title("Top 10 Countries by Out-of-School Children per 100 Population")
plt.xlabel("Out-of-School Rate (%)")
plt.ylabel("Country")
plt.tight_layout()
plt.show()


# In[41]:


#Unemployment vs. Primary Grade Repetition

df["Unemployment_Quartile"] = pd.qcut(
    df["Unemployment"],
    q=4,
    labels=["Q1 (Lowest)", "Q2 (Low-Mid)", "Q3 (Mid-High)", "Q4 (Highest)"],
)


# In[43]:


#Aggregate average repetition rate

grouped_df = (
    df.groupby("Unemployment_Quartile", observed=False)[
        "% of Repeaters in Primary Education"
    ]
    .mean()
    .reset_index()
)


# In[44]:


#Visualization

plt.figure(figsize=(8, 5))
sns.barplot(
    data=grouped_df,
    x="Unemployment_Quartile",
    y="% of Repeaters in Primary Education",
    palette="Blues_r",
)

plt.title("Mean Primary Repetition Rate across Unemployment Quartiles")
plt.xlabel("Unemployment Level")
plt.ylabel("Average Repetition Rate (%)")
plt.tight_layout()
plt.show()


# In[48]:


#Primary Enrolment Coverage Rate

df["Primary_Enrolment_Pct"] = (
    df["Enrolment in Primary Education"] / df["Population"]
) * 100


# In[50]:


top_coverage = df.nlargest(10, "Primary_Enrolment_Pct")[
    ["Country Name", "Primary_Enrolment_Pct"]
]
print(top_coverage)


# In[51]:


#Visualization

plt.figure(figsize=(10, 5))
sns.barplot(
    data=top_coverage,
    x="Primary_Enrolment_Pct",
    y="Country Name",
    hue="Country Name",
    palette="Greens_r",
    legend=False,
)

plt.title("Top 10 Countries by Primary Enrolment relative to Population")
plt.xlabel("Primary Enrolment Rate (%)")
plt.ylabel("Country")
plt.tight_layout()
plt.show()


# In[52]:


#Out-of-School Children vs. Life Expectancy

df["Out_of_School_Rate"] = (
    df["Out-of-School Children of Primary School"] / df["Population"]
) * 100


# In[54]:


#Life Expectancy logical tiers

df["Life_Expectancy_Tier"] = pd.cut(
    df["Life Expectancy at Birth"],
    bins=[0, 60, 70, 75, 100],
    labels=["< 60 Yrs", "60-70 Yrs", "70-75 Yrs", "> 75 Yrs"],
)


# In[55]:


#Visualization

plt.figure(figsize=(9, 5))
sns.boxplot(
    data=df,
    x="Life_Expectancy_Tier",
    y="Out_of_School_Rate",
    palette="Reds",
)

plt.title("Out-of-School Children Rate by Life Expectancy Bracket")
plt.xlabel("Life Expectancy Tier")
plt.ylabel("Out-of-School Rate (%)")
plt.tight_layout()
plt.show()


# In[58]:


#Socio-Economic & Educational Correlation Heatmap

df["Out_of_School_Rate"] = (
    df["Out-of-School Children of Primary School"] / df["Population"]
) * 100


# In[60]:


#numeric features for compute correlation matrix

numeric_cols = [
    "GDP_per_Capita",
    "% of Repeaters in Primary Education",
    "Unemployment",
    "Life Expectancy at Birth",
    "Secondary_to_Primary_Ratio",
    "Out_of_School_Rate",
]
corr_matrix = df[numeric_cols].corr()
print(numeric_cols)


# In[61]:


#Visualization

plt.figure(figsize=(9, 7))
sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5,
    vmin=-1,
    vmax=1,  # Normalizes correlation scale between -1 and +1
)

plt.title("Correlation Matrix: Socio-Economic & Education Metrics")
plt.xticks(rotation=45, ha="right")  # Prevents label clipping on X-axis
plt.tight_layout()
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




