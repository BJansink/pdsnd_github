import time
import pandas as pd
import numpy as np
import calendar

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
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nWhat city do you want to look into? [chicago, new york city, washington?]: \n')
    while city.lower() not in CITY_DATA.keys():
        city = input('\nPlease fill out a correct city from the list: \n')
    print("\n Nice! We will ride our bikes to {}!\n".format(city))

          # TO DO: get user input for month (all, january, february, ... , june)
    month = input("\nTell me, do you want to look into a specific month of the year or all?: \n")
    months = ['all','january','february','march','april','may','june']
    while month.lower() not in months:
        month = input("\nPlease write down all or a monthname between january and june in lower cases! \n")
    if month != 'all':
        print("\nOkay then, let\'s look at the month {}!\n".format(month.title()))
    else:
        print("No need to be picky, were going to look at all months!")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nIs there a day of the week you want to look into or all? \n")
    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    while day.lower() not in days:
        day = input("Please write down a day of the week (e.g. monday) or all in lower cases: ")
    if day != 'all':
        print("Let\'s dive into {} then!".format(day.title()))
    else:
        print("All days of the week it is!")

    print('-'*40)
    return city.lower(), month.lower(), day.lower()

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour
    df['Trip Time'] = df['End Time'] - df['Start Time']
    df['Combo Trip'] = 'Start: ' + df['Start Station'] + " - " + "End: " + df['End Station']
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    commonmonth = df['month'].mode()[0]
    print("\nThe most common month to share bikes is: {}\n".format(calendar.month_name[commonmonth]))
    # TO DO: display the most common day of week
    commonday = df['day_of_week'].mode()[0]
    print("\nThe most common day to bike is: {}\n".format(commonday))

    # TO DO: display the most common start hour
    if (df['Start Hour'].mode()[0]) >= 12:
        commonstarthour = str(((df['Start Hour'].mode()[0])-12)) + 'PM'
    else:
        commonstarthour = str((df['Start Hour'].mode()[0])) + 'AM'
    print("\nThe hour most people start to bike is: {}\n".format(commonstarthour))
    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most popular station to start at is {}.".format(df["Start Station"].mode()[0]))

    # TO DO: display most commonly used end station
    print("The most popular station to end at is {}.".format(df["End Station"].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    print("The most frequently combined start and end station are: {}".format(df['Combo Trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*38)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # NOTE: variables split trip time in days, hours, minutes, seconds
    sumtravel = df['Trip Time'].sum()
    tripdays, seconds = sumtravel.days, sumtravel.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    print("People travelled for {} day(s), {} hour(s) {} minute(s) and {} second(s)".format(tripdays,hours,minutes,seconds))

    # TO DO: display mean travel time
    # Note: variables split trip time in days, hours, minutes, seconds
    meantravel = df["Trip Time"].mean()
    days, seconds = meantravel.days, meantravel.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    print("The average travel time is {} day(s), {} hour(s), {} minute(s) and {} second(s)".format(days,hours,minutes,seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*38)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    usertypescount = df['User Type'].value_counts()
    print("\nThe user types and their number of users are: \n {}".format(usertypescount))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gendercount = df['Gender'].value_counts(dropna=False)
        print("\n The different genders and the number of users belonging to them are: \n {}".format(gendercount))
    else:
        print('\n Unfortunately, gender data is not available for this city\n')
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliestyear = int(df['Birth Year'].min())
        latestyear = int(df['Birth Year'].max())
        frequentyear = int(df['Birth Year'].mode())
        print("\nThe oldest user is born in {}.\nThe youngest user is born in {}. \nMost users are born in the year {}\n".format(earliestyear,latestyear,frequentyear))
    else:
        print('\nUnfortunately this city does not keep information on users\' birthday\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*38)


def main():
    while True:
        city, month, day = get_filters()
        #Sanity check to see if user really wanted to view this city/month/day combination
        sureondata = input('Just to be sure, you want to see data for {} for month {} and day {}.\n Are you sure you like to see data for these filters? [yes/no]: '.format(city,month,day))
        if sureondata != 'yes':
            city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
