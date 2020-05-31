#!/usr/bin/env python
# coding: utf-8

# In[161]:


from functools import reduce
import pandas as pd
import calendar
import seaborn as sns
sns.set_style('whitegrid')
import matplotlib.pyplot as plt
plt.close('all')


# In[162]:


# I analyze some dataset about the COVID pandemic. 
# I want to understand if the trend of cases/deaths has been impacted by different government measures. 
# Particularly if the different time when they have been implemented had an impact on the trend in the different countries.
# I used three different dataset: 1- Measures governement dataset provided by ACAPS; 2- Time series of confirmed cases provided
# by CSSE (John Hopkins); 3- Time series of deaths provided by CSSE (John Hopkins)

# loading the 3 files in dataframe

measures = pd.read_csv('C:\\Users\\Romina\\Desktop\\DBSCourse\\ProgrammingBigData\\CA4\\acaps_covid19_government_measures_dataset.csv', sep = ';', encoding = 'latin1')
cases = pd.read_csv('C:\\Users\\Romina\\Desktop\\DBSCourse\\ProgrammingBigData\\CA4\\time_series_covid19_confirmed_global.csv')
deaths = pd.read_csv('C:\\Users\\Romina\\Desktop\\DBSCourse\\ProgrammingBigData\\CA4\\time_series_covid19_deaths_global.csv')


# In[163]:


# Let's have a look at the measures dataset
measures.info()


# In[164]:


# In the dataset there are two different types of measures (attribute LOG_TYPE): 1-'Introduction/extensions of measures' ,
# 2- Phase-out measures. I decided to analyze the first type because they are that ones implemented to stop/slow the spread

measures = measures[measures['LOG_TYPE'].isin(['Introduction / extension of measures'])]

# The measures falls in 6 different categories (attribute CATEGORY)
measures.CATEGORY.unique()


# In[165]:


# In the dataframe information I see that some rows have the 'Date Implemented' attribute empty (10924 non-null over 11200 total rows)
# I decided to filter out the rows with empty Date_implemented because this attribute is strategic for my analysis

measures = measures.dropna(axis=0, subset=['DATE_IMPLEMENTED'])


# In[166]:


# I isolate the attribute I'm interested in (country, region, date implementation, measure category)

measures_by_country = measures.filter(['COUNTRY','REGION','CATEGORY','DATE_IMPLEMENTED'], axis=1)
measures_by_country.head(5)


# In[167]:


# I calculate the measures frequency for each category, country and date_implemented
measures_by_country = measures_by_country.groupby(['COUNTRY','REGION','DATE_IMPLEMENTED','CATEGORY']).size().unstack(fill_value=0)


# In[168]:


measures_by_country.head(5)


# In[169]:


# I rename some columns and reset the index of dataframe

measures_by_country = measures_by_country.reset_index().rename_axis(None, axis=1)
measures_by_country = measures_by_country.rename(str.lower, axis='columns')
measures_by_country = measures_by_country.rename(columns={"date_implemented": "date"})


# In[170]:


# Let's have a look at the cases and deaths dataframe

cases.info()


# In[171]:


deaths.info()


# In[172]:


cases.head(5)


# In[173]:


deaths.head(5)


# In[174]:


# The dataframes are series with cumulative data organized in the columns. Each row represents a different country
# The attribute Province/State is used for the overseas territorial collectivity that belong to the Country.
# As I'm interested in the data for the main country, I filter out this Province/State

cases = cases[cases['Province/State'].isnull()]
deaths = deaths[deaths['Province/State'].isnull()]


# In[175]:


# I remove the unenecessary columns 

cases = cases.drop(['Province/State', 'Lat','Long'], axis=1)
deaths =  deaths.drop(['Province/State', 'Lat','Long'], axis=1)


# In[176]:


# Before joining the three dataframe , I reshape the Cases and Death dataframe in order to trasform the date and the figures
# as rows details
# Reshaping for the dataframe cases. I remove the dates with 0 cases/deaths

cases_n = (cases.set_index(["Country/Region"])
         .stack()
         .reset_index(name='Cases')
         .rename(columns={'level_1':'date'}))

cases_n = cases_n[cases_n['Cases'] > 0]

cases_n.head(5)


# In[177]:


# Reshaping for the dataframe deaths

deaths_n = (deaths.set_index(["Country/Region"])
         .stack()
         .reset_index(name='Deaths')
         .rename(columns={'level_1':'date'}))

deaths_n = deaths_n[deaths_n['Deaths'] > 0]

deaths_n.head(5)


# In[178]:


# The date attribute has a different format (m/d/yy) of the date attribute of measures_by_country (dd/mm/yyyy) dataframe
# I rename the column Country/Region before the join

cases_n['date'] = pd.to_datetime(cases_n['date']).dt.strftime('%d/%m/%Y')
cases_n = cases_n.rename(columns={"Country/Region": "country"})


# In[179]:


deaths_n['date'] = pd.to_datetime(deaths_n['date']).dt.strftime('%d/%m/%Y')
deaths_n = deaths_n.rename(columns={"Country/Region": "country"})


# In[180]:


# I join the three dataframe with a right inner join because the date field. The deaths and cases dataframe contains daily information
# The measures datframe is based on measure date implementation. If at least one measure is not implemented for each day, 
# some dates cannot be available for each country. In order to avoid loosing data for deaths and cases dataframe the right join
# has been implemented

dfs = [measures_by_country, cases_n, deaths_n]

data = reduce(lambda left,right: pd.merge(left,right, how = 'right', on=['country','date']), dfs)


# In[181]:


# Let's have a look at the new dataframe

data.head(5)


# In[182]:


# I want to analyze data for the European countries and I remove the redundant column Region

data = data[data['region'].isin(['Europe'])]

data =  data.drop(['region'], axis=1)


# In[183]:


# I add a new column with the total of measures for each country and date
col_list= list(data)

col_list.remove('Cases')
col_list.remove('Deaths')


data['measures_tot'] = data[col_list].sum(axis=1)


# In[184]:


# I add a column with the month extracted from date attribute (I will use the month in the plots)

data['date'] = pd.to_datetime(data['date'], format= '%d/%m/%Y')
data['month_date'] = pd.DatetimeIndex(data['date']).month

data['month_date'] = data['month_date'].apply(lambda x: calendar.month_abbr[x])


# In[185]:


data.head(5)


# In[186]:


# I want to plot the # of measures implemented by each countries in the different months
# I make a new dataframe in which the deaths, cases and measures are aggregated by country and month
# As the deaths and cases are cumulated on month base, I decide to take the max value for each month

data_country_month = data.groupby(['country', 'month_date']).agg({'Deaths':'max','Cases' : 'max', 'measures_tot' : 'sum'})
data_country_month = data_country_month.reset_index()
data_country_month.head(5)


# In[187]:


plt.figure(figsize=(15,8), dpi= 80)
bx = sns.barplot(x='country', y='measures_tot', hue = 'month_date', data=data_country_month, hue_order = ['Feb','Mar','Apr','May'])
bx.set_xticklabels(bx.get_xticklabels(), rotation=40, ha="right")
plt.xlabel("European countries")
plt.ylabel("# Government measures")
plt.legend(loc='upper left')
plt.title("Tot government measures by month (Europe)") 
plt.show(bx)


# In[188]:


# There are some countries with peaks in April (switzerland, Portugal, Germany), 
# some other instead with peak of measures on March (Denmark, Hungary, Italy)
# I want to analyze a subset of countries. I decided to isolate the top 10 countries by measures (the top 10 countries for 
# the total of measures implemented)

# the dataframe below contains the total measures for each country
measures_by_country = data.groupby(['country']).agg({'measures_tot' : 'sum'})
measures_by_country = measures_by_country.reset_index()

# I create a new dataframe with the top 10 countries
top10_countries = measures_by_country.sort_values('measures_tot', ascending = False).head(10)

# I cretae a new dataframe with the granularity of original 'data' dataframe containing only the top 10 countries
data_top10country_month = data_country_month[data_country_month['country'].isin(top10_countries['country'])]


# In[189]:


# I want to plot the #measures, deaths and cases for the top 10 countries
# To plot the deaths and cases as trend lines I create two new subset and reshape them ( bring the countries as columns)

top10_deaths = data_top10country_month.filter(['month_date','country', 'Deaths'])
top10_deaths = pd.pivot_table(top10_deaths, values = 'Deaths', index = 'month_date', columns = 'country').reset_index()
top10_deaths.head(5)


# In[190]:


top10_cases = data_top10country_month.filter(['month_date','country','Cases'])
top10_cases = pd.pivot_table(top10_cases, values = 'Cases', index = 'month_date', columns = 'country').reset_index()
top10_cases.head(5)


# In[191]:


fig, (ax1, ax2, ax3 ) = plt.subplots(3, 1,figsize=(10,18), dpi= 80)
bx = sns.barplot(x='month_date', y='measures_tot', hue = 'country', data=data_top10country_month, order = ['Feb','Mar','Apr','May'], ax = ax1)
bx.set_xticklabels(bx.get_xticklabels(), rotation=40, ha="right")
ax1.set_ylabel ('')
ax1.set_xlabel ('')
ax1.title.set_text('Tot government measures by month (Top 10 countries)')
bx.legend(loc='upper left')

field = 'month_date'
month_ordered = ['Feb','Mar','Apr','May']
dx = top10_deaths.set_index(field).loc[month_ordered].plot(marker = "o", ax = ax2)
ax2.set_xlabel ('')
ax2.title.set_text('Deaths by month (incremental)')

cx = top10_cases.set_index(field).loc[month_ordered].plot(marker = "o", ax = ax3)
ax3.set_xlabel ('')
ax3.title.set_text('Cases by month (incremental)')


# In[192]:


# I think that measures implemented during the month had delayed effects on deaths/cases confirmed
# I can see that countries as Portugal, Germany, Switzerland, Finland had a big jump of measures implemented between 
# March and April. 
# As measures implemented in April could have impact on deaths/cases during May, I can suppose that the increase
# of these measures have helped to flatten the death/cases curve for these countries.

# On the other side countries as Italy, Spain and France had not a big jump on measures implemented between March and April.
# For these countries the variance of deaths/cases between months has been huge.
# Germany is the country that could contradict my previous sentence because the huge increment of confirmed cases 
# between March and April despite the big jump of measures.
# For this reason I want to investigate the distribution of measures categories for this country.

data_Germany = data[data['country'].isin(['Germany'])]
data_Germany = data_Germany.drop(['country','date', 'measures_tot','Cases','Deaths'], axis=1)
data_Germany = data_Germany.groupby(['month_date']).sum()
data_Germany = data_Germany.T

fig, (ax1, ax2 ) = plt.subplots(1, 2,figsize=(12,18), dpi= 80)
pie_1 = data_Germany['Mar'].plot(kind = 'pie', autopct='%1.0f%%', pctdistance=0.6, ax = ax1)
ax1.set_ylabel ('')
ax1.title.set_text("Germany Government measures - March")

pie_2 = data_Germany['Apr'].plot(kind = 'pie', autopct='%1.0f%%', pctdistance=0.6, ax = ax2)
ax2.set_ylabel ('')
ax2.title.set_text("Germany Government measures - April")


# In[193]:


# The increase of German measures between March and April has to be attributed to two main categories: governance and socio-economic, 
# public health measures.
# In the 'Public health measures' category are included measures such as 'strenghtening the public health policy' and 'Testing policy'
# (attribute 'MEASURE' in the first dataset)
# This could be explain the huge increase of cases confirmed between March and April and instead a less variance
# on deaths for the German country.
# I investigate if the distribution of the categories is similar in other countries with low cases/deaths figures.
# I analyze the Switzerland situation

data_Switz = data[data['country'].isin(['Switzerland'])]
data_Switz = data_Switz.drop(['country','date', 'measures_tot','Cases','Deaths'], axis=1)
data_Switz = data_Switz.groupby(['month_date']).sum()
data_Switz = data_Switz.T

fig, (ax1, ax2 ) = plt.subplots(1, 2,figsize=(13,20), dpi= 80)
pie_1 = data_Switz['Mar'].plot(kind = 'pie', autopct='%1.0f%%', pctdistance=0.6, ax = ax1)
ax1.set_ylabel ('')
ax1.title.set_text("Switzerland Government measures - March")

pie_2 = data_Switz['Apr'].plot(kind = 'pie', autopct='%1.0f%%', pctdistance=0.6, ax = ax2)
ax2.set_ylabel ('')
ax2.title.set_text("Switzerland Government measures - April")


# In[194]:


# For Switzerland the 'governance and socio-economic category' measures were the 50% of all the measures implemented
# As in Germany they seem , together the poublic health measures, the main important measures categories

# let's have a look at the countries with bigger case/deaths increase. I take the Italian example

data_Italy = data[data['country'].isin(['Italy'])]
data_Italy = data_Italy.drop(['country','date', 'measures_tot','Cases','Deaths'], axis=1)
data_Italy = data_Italy.groupby(['month_date']).sum()
data_Italy = data_Italy.T

fig, (ax1, ax2 ) = plt.subplots(1, 2,figsize=(12,20), dpi= 80)
pie_1 = data_Italy['Mar'].plot(kind = 'pie', autopct='%1.0f%%', pctdistance=0.6, ax = ax1)
ax1.set_ylabel ('')
ax1.title.set_text("Italy Government measures - March")

pie_2 = data_Italy['Apr'].plot(kind = 'pie', autopct='%1.0f%%', pctdistance=0.6, ax = ax2)
ax2.set_ylabel ('')
ax2.title.set_text("Italy Government measures - April")


# In[196]:


# In Italy the governance and socio-economic measures seem to be a lower proportion in the total measures and compared
# with Germany and Switzerland.
# Let's have a look at the Spanish situation

data_Spain = data[data['country'].isin(['Spain'])]
data_Spain = data_Spain.drop(['country','date', 'measures_tot','Cases','Deaths'], axis=1)
data_Spain = data_Spain.groupby(['month_date']).sum()
data_Spain = data_Spain.T

fig, (ax1, ax2 ) = plt.subplots(1, 2,figsize=(12,20), dpi= 80)
pie_1 = data_Spain['Mar'].plot(kind = 'pie', autopct='%1.0f%%', pctdistance=0.6, ax = ax1)
ax1.set_ylabel ('')
ax1.title.set_text("Spain Government measures - March")

pie_2 = data_Spain['Apr'].plot(kind = 'pie', autopct='%1.0f%%', pctdistance=0.6, ax = ax2)
ax2.set_ylabel ('')
ax2.title.set_text("Spain Government measures - April")


# In[160]:


# Again the governance and socio-economic measures are lower than the first two countries analyzed.
# I note, moreover that the % of them has slightly decreased from March to April for Italy and Spain.
# For Germany and Switzerland, instead, the proportion has increased from March to April

# This suggests to me that a more deep analysis of measures implemented could suggest some winner measure that had
# a positive impact to slow-down the spread and the deaths cases.

