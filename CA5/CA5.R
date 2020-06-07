
library(dplyr) 
library(reshape2)
library(reshape)

#load file with Governement measures details

measures <- read.csv("C:\\Users\\Romina\\Desktop\\DBSCourse\\ProgrammingBigData\\CA5\\acaps_covid19_government_measures_dataset.csv", sep = ";", header = TRUE)

df_measures <- data.frame(measures)

str(df_measures)
head(df_measures, 5)

# Filter the measure and date implemented not null

df_measures <- subset(df_measures, LOG_TYPE == 'Introduction / extension of measures')

df_measures <- subset(df_measures, DATE_IMPLEMENTED != "")

# create the dataset with desired columns

measures_by_country <- select(df_measures, COUNTRY ,REGION, CATEGORY, DATE_IMPLEMENTED)

# modify two countries in order to avoid problem with the next joins
# some countries have a different definition on this file from the next ones

measures_by_country$COUNTRY <- as.character(measures_by_country$COUNTRY)
measures_by_country$COUNTRY[tolower(measures_by_country$COUNTRY) == "czech republic"] <- "Czechia"
measures_by_country$COUNTRY[tolower(measures_by_country$COUNTRY) == "moldova republic of"] <- "Moldova"
measures_by_country$COUNTRY[tolower(measures_by_country$COUNTRY) == "North Macedonia Republic Of"] <- "North Macedonia"
measures_by_country$COUNTRY[measures_by_country$COUNTRY == "Russian Federation"] <- "Russia"
measures_by_country$COUNTRY <- as.factor(measures_by_country$COUNTRY)

#write.csv(measures_by_country,"C:\\Users\\Romina\\Desktop\\DBSCourse\\ProgrammingBigData\\CA5\\measures.csv", row.names = FALSE)

#load files with time seires for cases and deaths registered in each country 

cases <- read.csv("C:\\Users\\Romina\\Desktop\\DBSCourse\\ProgrammingBigData\\CA5\\time_series_covid19_confirmed_global.csv", sep = ",", header = TRUE)

cases <- data.frame(cases)
str(cases)

# select the rows with Province/State empty. This column is used to specify data for overseas territorial
#collectivity that belong to the country
# exclude the column not required for the dataset

cases <- subset(cases, Province.State == "" )
cases <- select(cases, -Province.State ,-Lat, -Long)
str(cases)

# reshaping the dataset in order to bring the time series with a row structure.
# Dates are transposed in rows
cases <- melt(cases, id = "Country.Region")

# convert the column with dates in a date format
cases$variable <- as.Date(as.Date(cases$variable , format = "X%m.%d.%y"), format ="%d/%m/%y")

# rename the columns after the reshaping
colnames(cases)[2] <- "date"
colnames(cases)[3] <- "cases"

print(cases)

#write.csv(cases,"C:\\Users\\Romina\\Desktop\\DBSCourse\\ProgrammingBigData\\CA5\\cases.csv", row.names = FALSE)

deaths <- read.csv("C:\\Users\\Romina\\Desktop\\DBSCourse\\ProgrammingBigData\\CA4\\time_series_covid19_deaths_global.csv", sep = ",", header = TRUE)

deaths <- data.frame(deaths)
str(deaths)

deaths <- subset(deaths, Province.State == "" )
deaths <- select(deaths, -Province.State ,-Lat, -Long)

deaths <- melt(deaths, id = "Country.Region")

deaths$variable <- as.Date(as.Date(deaths$variable , format = "X%m.%d.%y"), format ="%d/%m/%y")

colnames(deaths)[2] <- "date"
colnames(deaths)[3] <- "deaths"

#write.csv(deaths,"C:\\Users\\Romina\\Desktop\\DBSCourse\\ProgrammingBigData\\CA5\\deaths.csv", row.names = FALSE)

# merge the two subset with covid data (cases and deaths)
# excluding the dates with cases and deaths = 0

covid_data <- merge(cases, deaths, by = c("Country.Region", "date"))
covid_data <- subset(covid_data, cases > 0 & deaths > 0)

# read the file with mapping country/region

mapping <- read.csv("C:\\Users\\Romina\\Desktop\\DBSCourse\\ProgrammingBigData\\CA5\\continents-according-to-our-world-in-data.csv", sep = ",", header = TRUE)


# merge the covid data with the mapping file for the region
# exclude the columns not used in the analysis

covid_data_region <- merge(covid_data, mapping, by.x = "Country.Region", by.y = "Entity", all.x = TRUE )
covid_data_region <- select(covid_data_region, -Code ,-Year)
colnames(covid_data_region)[5] <- "Region"

# modify the country Czech Republic to align with the definition in the measures dataset

covid_data_region$Country.Region <- as.character(covid_data_region$Country.Region)
covid_data_region$Country.Region[tolower(covid_data_region$Country.Region) == "czech republic"] <- "Czechia"
covid_data_region$Country.Region <- as.factor(covid_data_region$Country.Region)

#write.csv(covid_data_region,"C:\\Users\\Romina\\Desktop\\DBSCourse\\ProgrammingBigData\\CA5\\covid.csv", row.names = FALSE)

# convert the date column to the desired date format (same format of covid_data_region dataset)
measures_by_country$DATE_IMPLEMENTED <- as.Date(measures_by_country$DATE_IMPLEMENTED , format = "%d/%m/%y")

# merge the measures dataset with covid dataset. 
# Full outer join 

dataset <- merge(measures_by_country, covid_data_region, by.x = c("COUNTRY","DATE_IMPLEMENTED","REGION"), by.y = c("Country.Region","date","Region"), all = TRUE)

#write.csv(dataset,"C:\\Users\\Romina\\Desktop\\DBSCourse\\ProgrammingBigData\\CA5\\output.csv", row.names = FALSE)

# select only the dataset with region = Europe
Europe_df <- subset(dataset, REGION == "Europe" )


library(ggplot2)

# find the top 10 countries in Europe for cases and deaths

# As the data are cumulative I will find for each country the maximum value of cases
# I order the dataset with decreasing logic in order to have the first top 10 countries

Europe_cases_max <- Europe_df %>% group_by(COUNTRY) %>% summarise_at(vars(cases), ~ max(., na.rm = TRUE)) 
Europe_cases_max

top10_Europe_cases <- Europe_cases_max$COUNTRY [order (Europe_cases_max$cases,  decreasing = TRUE)]
top10_Europe_cases

Europe_deaths_max <- Europe_df %>% group_by(COUNTRY) %>% summarise_at(vars(deaths), ~ max(., na.rm = TRUE))
Europe_deaths_max

top10_Europe_deaths <- Europe_deaths_max$COUNTRY [order (Europe_deaths_max$deaths,  decreasing = TRUE)]
top10_Europe_deaths

# plot the cases and deaths trend in the three months available for the top 10 countries

ggplot(data = subset(Europe_df, COUNTRY %in% top10_Europe_cases [1 : 10] & !(is.na(Europe_df$cases))), aes(x=DATE_IMPLEMENTED, y=cases, group=COUNTRY)) +
  geom_line(aes(color=COUNTRY))+
  geom_point(aes(color=COUNTRY))+
  xlab("")+
  ylab("# case confirmed")+
  theme(legend.position="top")

ggplot(data = subset(Europe_df, COUNTRY %in% top10_Europe_deaths [1 : 10] & !(is.na(Europe_df$deaths))), aes(x=DATE_IMPLEMENTED, y=deaths, group=COUNTRY)) +
  geom_line(aes(color=COUNTRY))+
  geom_point(aes(color=COUNTRY))+
  xlab("")+
  ylab("# deaths")+
  theme(legend.position="top")

# Prepare data to build the scatter plot with the deaths and # of measures implemented

#First dataframe contains for each country the max deaths and the max cases
first_df <- Europe_df %>% group_by(COUNTRY) %>% summarise(max(deaths, na.rm = TRUE), max(cases, na.rm = TRUE))
#Second dataframe contains for each country the # of measures
second_df <- subset(Europe_df, !(is.na(Europe_df$CATEGORY))) %>% group_by(COUNTRY) %>% count()
# Merge the two dataframe and renames the columns 
scatter_df <- merge(first_df, second_df)

colnames(scatter_df)[2] <- "deaths"
colnames(scatter_df)[3] <- "cases"
colnames(scatter_df)[4] <- "measures"

# I create a subset includign only the top 10 countries for deaths cases
scatter_df <- subset(scatter_df, COUNTRY %in% top10_Europe_deaths [1 : 10])

ggplot(scatter_df, aes(x=measures, y = deaths, color = COUNTRY)) +
  geom_point() +
  geom_text(
    label = scatter_df$COUNTRY,
    nudge_x = 0.25, nudge_y = -0.25,
    check_overlap = T
  )+
  xlab("# measures implemented (Mar, Apr, May)")+
  ylab("# deaths reached in May")+
  theme(legend.position = "none")

# I create a dataframe containing for each country the # of measures by category
measures_by_category <- subset(Europe_df, !(is.na(Europe_df$CATEGORY))) %>% group_by(COUNTRY, CATEGORY) %>% count() 
colnames(measures_by_category)[3] <- "measures"

measures_by_category

ggplot(data = subset(measures_by_country, COUNTRY %in% list('Russia','United Kingdom','Italy','Spain','Germany')), aes(x=CATEGORY, fill = COUNTRY )) +
  geom_bar(position = position_dodge(width = 0.9))+
  xlab("")+
  ylab("# measures implemented (Mar, Apr, May")+
  theme(legend.position = "top")