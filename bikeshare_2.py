import time
import datetime
import pandas as pd
import numpy as np

"""
bikeshare_2.py 
Author: Joachim Kallenbach
Project for Udacity Nanodegree "Data Science with Python"
Submitted: July, 23rd 2023
"""


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = {'january': 1,
          'february': 2,
          'march': 3,
          'april': 4,
          'may': 5,
          'june': 6,
          'all': 0}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
       city = input("Enter the city (one of Chicago, New York City, Washington): ")
       if city.lower() in CITY_DATA:
          print("City {} is chosen".format(city.title()))
          break
       else:
          print("Sorry - city {} is not a valid city!".format(city.title()))

    while True:
       month = input("Would you like to filter by month? Please enter the name of the month to filter by, or ""all"" to apply no month filter: ")
       if month.lower() in MONTHS:
          print("Month {} is chosen".format(month.title()))
          break
       else:
          print("Sorry - {} is not a month city!".format(month.title()))


    while True:
       try:
          day = int(input("Please enter day as an integer (Monday = 1), 0 if you don't want to filter by day: "))
       except ValueError:
          print("Invalid integer (0-7!")
       if day in (0,1,2,3,4,5,6,7):
          print('-'*40)
          return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    try:
        df = pd.read_csv('{}.csv'.format(city.title().replace(" ", "_")))
        #print('df is of type:', type(df))
        #print('df has shape:', df.shape)
        #print(df['User Type'].value_counts())        
    except:
        print('df went wrong:')
        exit()
        
    """" 
     filter 
     To let Monday be day 1 of the week, we need to decrease var day by one, because in Paython the Monday is a 0
    """
    if month != "all":
       print("Filter by month {}".format(month.title()))
       df['Start Time'] = pd.to_datetime(df['Start Time'])
       df = df[df['Start Time'].dt.month == MONTHS[month]] 
       #print(df)
    if day != 0:
       print("Filter by day ", day)
       df['Start Time'] = pd.to_datetime(df['Start Time'])
       df['day_of_week'] = df['Start Time'].dt.day_name()
       df = df[df['Start Time'].dt.dayofweek == day-1] 
       #print(df)
    return df

def display_raw_data(df):
    """ displays raw data if the userwants to see some of them """
    
    display_data = input("Before showing some statistics - are you interested in viewing the raw data Enter yes or no.?\n")
    data_index = 0
    
    while display_data.lower() == 'yes':
       print('Row {} to {} '.format(data_index, data_index+5))
       print(df[data_index:data_index+5])
       data_index = data_index+5
       display_data = input("Do you want to see next five rows? Enter yes or no.\n")

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    popular_month = df['month'].mode()[0]
    print('Most Popular day of the week: ', popular_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_weekday = df['day_of_week'].mode()[0]
    print('Most Popular day of the week: ', popular_weekday)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour: ', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    usages_start_station = df['Start Station'].value_counts(dropna=False).max()
    comm_start_station = df['Start Station'].mode().iloc[0]
    print("Most commonly used start station: {} used {} times".format(comm_start_station.title(), usages_start_station))

    # display most commonly used end station
    usages_end_station = df['End Station'].value_counts(dropna=False).max()
    comm_end_station = df['End Station'].mode().iloc[0]
    print("Most commonly used end station: {} used {} times".format(comm_end_station.title(), usages_end_station))

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station']+" - "+df['End Station']
    most_freq_trip = df['trip'].mode().iloc[0]
    print("Most frequent combination of start station and end station trip", most_freq_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = int(df['Trip Duration'].sum())
    mi, sec = divmod(total_duration, 60)
    hour, mi = divmod(mi, 60)
    day, hour = divmod(hour, 24)
    print('\nTotal travel time: {:d} days, {:02d} hours, {:02d} minutes, {:02d} seconds'.format(day, hour, mi, sec))

    # display mean travel time - skipping fractions of seconds
    mean_duration = int(df['Trip Duration'].mean())
    mi, sec = divmod(mean_duration, 60)
    hour, mi = divmod(mi, 60)
    day, hour = divmod(hour, 24)
    print('\nMean travel time: {:d} days, {:02d} hours, {:02d} minutes, {:02d} seconds'.format(day, hour, mi, sec))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts(dropna=False)
    print("\nThese are the counts of user types:\n\n ", user_type_counts) 
    
    # Display counts of gender
    try:
       gender_counts = df['Gender'].value_counts(dropna=False)
       print("\nThese are the counts of genders:\n\n ", gender_counts) 
    except:
       print("\nNo information about gender found in data") 


    # Display earliest, most recent, and most common year of birth

    try:
       common_yob = str(df['Birth Year'].mode()[0])
       recent_yob = str(df['Birth Year'].min())
       early_yob = str(df['Birth Year'].max())
       print("\nMost common year of birth: ", common_yob[:4])
       print("Earliest year of birth: ", recent_yob[:4])
       print("Most recent year of birth: ", early_yob[:4])
    except:
       print("\nNo information about year of birth found in data") 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    print("This is start of main!")
    while True:
        city, month, day = get_filters()
        print("Loading...{}",format(city.title().replace(" ", "_")))
        df = load_data(city, month, day)
        print("Loading done")
        
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
