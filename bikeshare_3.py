import random
import time


CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

# _________________________Control Panel_________________________
run_random = False
# run_cycle_thru = True
if_restart = True
# _______________________________________________________________


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Additional description: <Add some other words here>

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    #TODO add todo task 1 here
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    cities = ["chicago", "new york city", "washington"]
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December', "All"]
    dayOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "All"]

    if run_random == True:
        city = random.choice(cities)
        month = random.choice(months)
        day = random.choice(dayOfWeek)

        print(f"City: {city}")
        print(f"Month: {month}")
        print(f"Day: {day}")

    #___________________________________________________________
    #TODO: for dicsussion on error testing
    # if run_random == False and run_cycle_thru == True:
    #     for c in range(len(cities)):
    #         for m in range(len(months)):
    #             for d in range(len(dayOfWeek)):
    #                 city = cities[c]
    #                 month = months[m]
    #                 day = dayOfWeek[d]
    #                 print(f"c: {c}, city: {city}")
    #                 print(f"m: {m}, month: {month}")
    #                 print(f"d: {d}, dayOfWeek: {day}")
    #                 print("=" * 40)
    #                 return city, month, day
    # ___________________________________________________________

    else:
        while True:
            city = input(f"Enter a city from list:\n {cities}").title()
            print(f"city:{city}")

            if city.lower() in cities:
                break

        # get user input for month (all, january, february, ... , june)
        while True:
            month = input(f"filter from the following months:\n{months}").title()

            if month.title() in months:
                break

        # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            day = input(f"filter from the following days:\n{dayOfWeek}").title()

            if day.title() in dayOfWeek:
                break

    print('-'*40)
    return city, month, day

# get_filters()

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
    # import libraries
    import pandas as pd

    # load data file into a dataframe
    city = city.lower()
    df = pd.read_csv(CITY_DATA[city])

    ## Have to drop the rows containing any NaN to reduce the number of error handlings in the code
    #TODO for discussion: why does the error occur in the following functions if the NaNs have been dropped
    # (cannot convert float NaN to integer is not in this city's data set)?
    df.dropna(how='any', inplace=True)
    no_nan = df.isna().any().sum()

    print("="*40)
    print(f"Number of NaN is {no_nan}")
    print("="*40)



    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df["Start Time"].dt.month_name()
    df['day_of_week'] = df["Start Time"].dt.day_name()

    # months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
    #           'november', 'december', "all"]

    # month = input(f"Filter by or 'all', or choose from list of months:\n{months}")

    # filter by month if applicable
    if month != 'All':

        # filter by month to create the new dataframe
        month = month.title()
        #TODO Discuss: df_by_month = df[df['month'] == month]
        df = df[df['month'] == month]

        # filter by day of week if applicable
        if day != 'All':
        # filter by day of week to create the new dataframe
            day = day.title()
            #TODO Discuss: df_by_day = df[df['day_of_week'] == day]
            df = df[df['day_of_week'] == day]
        else:
            pass
    else:
        pass
    print("="*80)
    print(df)
    print("="*80)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    try:
        common_month_df = df['month'].value_counts().head(1)
        common_month = common_month_df.index[0]
        comm_month_count = common_month_df.iloc[0]
        print(common_month)
        print(f"The most common month is {common_month} with {comm_month_count} records")
    except Exception as e:
        # TODO if month filter on, calculation not applicable
        print(f"Data set filtered,{e} most common month on a filtered df not applicable")
        pass

    # display the most common day of week
    try:

        common_day_df = df["day_of_week"].value_counts().head(1)
        common_day = common_day_df.index[0]
        common_day_count = common_day_df.iloc[0]
        print(common_day_df)
        print(f"The most common day of the week is {common_day} with {common_day_count} records")

    except Exception as e:
        # TODO discuss: if month filter on, calculation not applicable
        print(f"Data set filtered,{e} most common day on a filtered df not applicable")
        pass

    # display the most common start hour
    try:
        df["start_hour"] = df["Start Time"].dt.hour
        common_hour_df = df["start_hour"].value_counts().head(1)
        common_hour = common_hour_df.index[0]
        common_hour_count = common_hour_df.iloc[0]
        print(common_hour_df)
        print(f"The most common start hour is {common_hour}hrs with {common_hour_count} records")
    except Exception as e:
        print(f"Data set filtered,error:{e}")
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        comm_start_st_df = df["Start Station"].value_counts().head(1)
        comm_start_st = comm_start_st_df.index[0]
        comm_start_st_count = comm_start_st_df.iloc[0]
        print(f"Most common start station is {comm_start_st} with {comm_start_st_count} records")
    except Exception as e:
        print(f"There are no no commonly used start stations on the day's filtered,\nerror: {e}")
        pass

    # display most commonly used end station
    try:
        comm_end_st_df = df["End Station"].value_counts().head(1)
        comm_end_st = comm_end_st_df.index[0]
        comm_end_st_count = comm_end_st_df.iloc[0]
        print(f"Most common end station is {comm_end_st} with {comm_end_st_count} records")
    except Exception as e:
        print(f"There are no no commonly used end stations on the day's filtered,\nerror: {e}")
        pass



    # display most frequent combination of start station and end station trip
    run_this = True

    if run_this == True:
        try:
            # Finding the value counts from Start Station
            start_st_df_val = df["Start Station"].value_counts()

            # Finding the value counts from End Station
            end_st_df_val = df["End Station"].value_counts()

            # Finding the common values between the two series based on highest counts
            comm_start_end_vals = start_st_df_val.index.intersection(end_st_df_val.index)

            # Sorting the common values by their count in column A in descending order
            sorted_common_vals = start_st_df_val.loc[comm_start_end_vals].sort_values(ascending=False).index

            # Getting the highest count value in both Start and End Station
            intersection_point_highest = sorted_common_vals[0]
            print(f"The most frequent combination of Start and End Station is {intersection_point_highest}")
        except Exception as e:
            print(f"There are is no most frequent combination of start station and end station trip,\nerror: {e}")
            pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    try:
        travel_time_sc = df["Trip Duration"].sum()
        travel_time_min = round(travel_time_sc / 60, 1)
        travel_time_years = round(((travel_time_min / 60) / 24) / 365.25, 1)
        trave_time_sec_rem = travel_time_sc % 60
        print(f"Total travel time is {travel_time_sc:,} seconds, or approx. {travel_time_years:,} years")
    except Exception as e:
        print(f"Error: {e}")
        pass

    # display mean travel time
    try:
        travel_time_sc_avg = round(df["Trip Duration"].mean(),2)
        travel_time_min_avg = round(travel_time_sc_avg / 60, 1)
        print(f"Mean travel is is {travel_time_sc_avg:,} seconds, or approx. {travel_time_min_avg:,} minutes")
    except Exception as e:
        print(f"Error: {e}")
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_df = df["User Type"].value_counts()
    print(f"Counts of user types:\n{user_type_df}")

    # Display counts of gender
    try:
        gender_df = df["Gender"].value_counts()
        print(gender_df)
    except Exception as e:
        print(f"Error: {e}, 'Gender' is not in this city's data set")
        pass

    # Display earliest, most recent, and most common year of birth
    try:
        birth_year_min = int(df["Birth Year"].min())
        birth_year_max = int(df["Birth Year"].max())
        birth_year_freq_df = df["Birth Year"].value_counts().head(1)
        birth_year_freq_indx = int(birth_year_freq_df.index[0])
        birth_year_freq_value = birth_year_freq_df.iloc[0]

        print(
            f"The earliest year of birth is {birth_year_min:},\nThe most recent birth year of birth is {birth_year_max:},"
            f"\nThe most common birth year of birth is {birth_year_freq_indx} with {birth_year_freq_value:,} records")

    except Exception as e:
        print(f"Error: {e}, 'Birth Year' is not in this city's data set")
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def func_display_data(df):

    see_first_rows = input("Would you like to see the first 5 rows of data? yes/no").lower()
    view_data = True
    start_loc = 0
    end_loc = start_loc + 5

    if see_first_rows == "yes":
        while view_data == True:

            print(f"start_loc: {start_loc}")
            print(f"end_loc: {end_loc}")
            print(df.iloc[start_loc:end_loc, :])
            view_data = input("Do you wish to see the next 5 rows? yes/no").lower()

            if view_data == "yes":
                view_data = True
                start_loc += 5
                end_loc += 5
            else:
                break


def func_combined():
    city, month, day = get_filters()
    df = load_data(city, month, day)

    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
    func_display_data(df)


def main():
    if run_random == True:
        for i in range(2):
            func_combined()

    #TODO: How do I cycle through every permutation?
    # elif run_random == False and run_cycle_thru == True:
    #     func_combined()

    if if_restart == True:
        while True:
            func_combined()

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                print("Your analysis is concluded.\nThank you!")
                break


if __name__ == "__main__":
    main()
