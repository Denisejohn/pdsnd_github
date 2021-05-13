import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
        try:
            city=input("Which city would you like to look at: Chicago, New York City or Washington? ").lower()
            if city in CITY_DATA.keys():
            # if city  == 'washington' or city == 'chicago' or city == 'new york city':
                break
            else:
                print('That\'s not a valid city, please try again')
        except:
            print('\nInvalid value\n')


    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Which month would you like to see data for: January, February, March, April, May, June or all? ").lower()
            if month in ['january', 'february','march', 'april', 'may','june','all']:
                break
            else:
                print('That\'s not a valid month, please try again')
        except:
            print('\nInvalid value\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Which day of the week would you like to look at? (type \"all\" to see all days) ").lower()
            if day in ['monday', 'tuesday','wednesday', 'thursday', 'friday','saturday','sunday','all']:
                break
            else:
                print('That\'s not a valid day, please try again')
        except:
            print('\nInvalid value\n')
    print('-'*80)
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
      # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    common_month =df['month'].mode()[0]
    datetime_object = datetime.datetime.strptime(str(common_month), "%m")
    month_name = datetime_object.strftime("%B")
    print('The most popular month is:', common_month, '(', month_name,')')


    # display the most common day of week
    common_dow =df['day_of_week'].mode()[0]
    print('The most popular day of the week is:', common_dow)

    # display the most common start hour
    common_hour =df['month'].mode()[0]
    print('The most popular start hour is:', common_hour)
    print("\nThe Time stats calculations took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station =df['Start Station'].mode()[0]
    print('The most popular start station is:', common_start_station)

    # display most commonly used end station
    common_end_station =df['End Station'].mode()[0]
    print('The most popular end station is:', common_end_station)

    # display most frequent combination of start station and end station trip
    combo =df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('\nThe most popular Start and End combination is:\n\t', combo)



    print("\nThe Station Stats calculations took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print('The total travel time in seconds is:', total_travel_time)
    #conv_time = dt.timedelta(seconds =total_travel_time)
    conv_time=time.strftime("%H:%M:%S", time.gmtime(total_travel_time))
    print('\t(.....Which in hours, minutes, seconds is:',conv_time, ')\n')

    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print('The average trip duration in seconds is:', mean_travel_time)
    conv_mean=time.strftime("%H:%M:%S", time.gmtime(mean_travel_time))
    print('\t(.....Which in hours, minutes, seconds is:',conv_mean ,')')

    print("\nThe Trip Duration calculations took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts(),'\n')

    # Display counts of gender
    if "Gender" in df.columns:
        print(df['Gender'].value_counts(),'\n')
    else:
        print('Gender data for Washington is not available')

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print("The eldest user was born in: " ,int(df['Birth Year'].min()))
        print("The youngest user was born in: " ,int(df['Birth Year'].max()))
        print("The most common year of birth was: " ,int(df['Birth Year'].mode()[0]))
    else:
        print('Birth Year data for Washington is not available')


    print("\nThe User Stats calculations took %s seconds." % (time.time() - start_time))
    print('-'*80)

def display_data(df):
    """Displays data at the request of the user, 5 rows at a time"""
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    end_loc = 5
    x=len(df.index)
    while start_loc < x:
        print(df.iloc[start_loc:end_loc])
        start_loc += 5
        end_loc += 5
        view_display = input('Would you like to see 5 more rows?:  ').lower()
        if view_display.lower() != 'yes':
            break
    print('-'*80)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        keep_looking = input('\nWould you like to continue looking at more bikeshare data? (Enter yes or no).\n')
        if keep_looking.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
