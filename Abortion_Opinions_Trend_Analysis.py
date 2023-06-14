#Import libraries 
import numpy as np 
import pandas as pd 
from matplotlib import pyplot as plt
import seaborn as sns

#load data into pandas dataframe 
df = pd.read_csv(r'general_social_survey_abortion.csv')

#check for missing values 
df.isnull().sum()
#There are a lot of missing values 

#Data preprocessing 
df.drop('Unnamed: 0', axis=1, inplace=True)
df['age'].fillna(df['age'].median(), inplace=True)
df['educ'].fillna(df['educ'].mode()[0], inplace=True)
df['partyid'].fillna(df['partyid'].mode()[0], inplace=True)
df['pid'].fillna(df['pid'].mode()[0], inplace=True)
df['relactiv'].fillna('Not applicable', inplace=True)
df['hispaniccat'].fillna('Not Hispanic', inplace=True)
df['hispanic'].fillna('Not Hispanic', inplace=True)
df[['abany', 'abdefect', 'abnomore', 'abhlth', 'abpoor', 'abrape', 'absingle']] = \
df[['abany', 'abdefect', 'abnomore', 'abhlth', 'abpoor', 'abrape', 'absingle']].fillna(0)

#View data 
df.head()

#view statistical measures 
df.describe()

#Check - propertion of respondents who support abortion 
abany_counts = df["abany"].value_counts(normalize=True)
plt.figure(figsize=(4,4))
plt.bar(x=abany_counts.index, height=abany_counts.values, color=["red", "purple"])
plt.xticks([0, 1], ["No", "Yes"])
plt.title("Proportion of Respondents Who Support Abortion")
plt.xlabel("Support for Abortion")
plt.ylabel("Proportion of Respondents")
plt.show()

#Distribution of respondent age 
sns.set_style('whitegrid')
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(14,6))
sns.histplot(data=df, x='age', kde=False, ax=ax1, color='#4d4d4d')
ax1.set_xlabel('Age', fontsize=14)
ax1.set_ylabel('Count', fontsize=14)
ax1.set_title('Distribution of Respondent Age', fontsize=16)
sns.kdeplot(data=df, x='age', fill=True, ax=ax2, color='#4d4d4d')
ax2.set_xlabel('Age', fontsize=14)
ax2.set_ylabel('Density', fontsize=14)
ax2.set_title('Distribution of Respondent Age', fontsize=16)
fig.suptitle('Distribution of Respondent Age', fontsize=18, fontweight='bold')
plt.show()

#Relationship between age and support for abortion 
age_grouped = df.groupby('age')['abany'].mean()
sns.regplot(x=age_grouped.index, y=age_grouped, color='blue', scatter_kws={'s': 50})
sns.despine()
plt.xlabel('Age', fontsize=12)
plt.ylabel('Proportion Supporting Abortion', fontsize=12)
plt.title('Relationship between Age and Support for Abortion', fontsize=14)
plt.grid(axis='both', alpha=0.3)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.show()

#Proportion of respondents supporting abortion over time 
abortion_prop = df.groupby('year')['abany'].mean()
fig, ax = plt.subplots(figsize=(16,6))
ax.plot(abortion_prop.index, abortion_prop.values, marker='o', markersize=8, linewidth=2, color='blue')

ax.set_xlabel('Year')
ax.set_ylabel('Proportion')
ax.set_title('Proportion of Respondents Supporting Abortion over Time')
ax.set_xticks(abortion_prop.index)
ax.tick_params(axis='x', which='major', labelsize=12, pad=10, rotation=45)
ax.grid(axis='x', linestyle='--', alpha=0.5)
ax.set_yticks([0.2, 0.4, 0.6, 0.8])
ax.tick_params(axis='y', which='major', labelsize=12, pad=10)
ax.grid(axis='y', linestyle='--', alpha=0.5)

avg_prop = abortion_prop.mean()
ax.axhline(avg_prop, linestyle='--', color='red', linewidth=1)
ax.text(abortion_prop.index[-1], avg_prop+0.02, f'Avg. Proportion: {avg_prop:.2f}', ha='right', fontsize=12, color='red')
plt.show()

#Support for abortion by party identification 
colors = ['#1f77b4', '#ff7f0e']
cross_tab = pd.crosstab(df['partyid'], df['abany'], normalize='index')
ax = cross_tab.plot(kind='bar', stacked=True, color=colors, figsize=(8,6))
ax.set_xlabel('Party Identification', fontsize=12)
ax.set_ylabel('Proportion', fontsize=12)
ax.set_title('Support for Abortion by Party Identification', fontsize=14)
ax.legend(title='Abortion Support', loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=12)
plt.xticks(rotation=45)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.7)
ax.set_ylim(0, 1)
for i in range(len(cross_tab)):
    for j in range(len(cross_tab.columns)):
        plt.text(i, cross_tab.iloc[i, :j+1].sum() - 0.05, str(round(cross_tab.iloc[i, j]*100,1)) + '%', ha='center', va='top', fontsize=12, fontweight='bold', color='white')
plt.show()

#Relationship between education and support for abortion 
plt.style.use('seaborn-whitegrid')
colors = ['#1f77b4']
educ_abany_prop = df.groupby('educ')['abany'].mean()
plt.scatter(educ_abany_prop.index, educ_abany_prop.values, color=colors, alpha=0.8)
z = np.polyfit(educ_abany_prop.index, educ_abany_prop, 1)
p = np.poly1d(z)
plt.plot(educ_abany_prop.index, p(educ_abany_prop.index), color=colors[0], linestyle='--')
plt.xlabel('Education (years)', fontsize=12)
plt.ylabel('Proportion supporting abortion', fontsize=12)
plt.title('Relationship between education and support for abortion', fontsize=14)
plt.xlim(0, 20)
plt.ylim(0, 1)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()

#Support for abortion by gender 
ct = pd.crosstab(df['sex'], df['abany'])
colors = ['#FFB6C1', '#87CEFA']
ax = ct.plot(kind='bar', stacked=True, color=colors)
ax.set_xlabel('Gender')
ax.set_ylabel('Count')
ax.set_title('Support for Abortion by Gender')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], title='Abortion Support', loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.xticks(rotation=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for i, row in ct.iterrows():
    for j, val in enumerate(row):
        if val > 0:
            ax.text(j, sum(row[:j+1])-0.9*val, f'{val:,}', ha='center', va='center')

plt.show()

#Support for abortion by race/ethnicity 
table = pd.crosstab(df.race, df.abany, normalize='index')
colors = ['#1f77b4', '#ff7f0e']
table.plot(kind='bar', stacked=True, color=colors, alpha=0.8)
plt.title('Support for Abortion by Race/Ethnicity', fontsize=14, fontweight='bold')
plt.xlabel('Race/Ethnicity', fontsize=12)
plt.ylabel('Proportion', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.legend(['Oppose', 'Support'], title='Abortion Support', loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)
plt.tight_layout()
plt.show()

#Support for abortion by level of religious activity 
abortion_by_religactiv = df.groupby('relactiv')['abany'].mean().reset_index()
palette = sns.color_palette('pastel')
sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(12, 4))
sns.boxplot(data=abortion_by_religactiv, x='relactiv', y='abany', palette=palette)
ax.set_xlabel('Religious Activity', fontsize=14, fontweight='bold')
ax.set_ylabel('Proportion Supporting Abortion', fontsize=14, fontweight='bold')
ax.set_title('Support for Abortion by Level of Religious Activity', fontsize=16, fontweight='bold')
sns.despine()
plt.show()