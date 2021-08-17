import pandas as pd

months = ['january', 'february', 'march', 'april', 'may', 'june']

days = [1,2,3,4,5,6,7]

dayOfWeek = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']

City_Data = { 'chicago': 'chicago.csv',
          'new york city': 'new_york_city.csv',
          'washington': 'washington.csv' }

option = ['yes', 'no']


def get_filters():
    print("Welcome to explore US BikeShare Data program! \n")
    day = month = " "

    while True:
        print("Cities currently available:\n1-Chicago\n2-New york city\n3-Washington\n")             
        city=input("Enter the City name to Review its data: ")
        if city.lower() in City_Data.keys() :
            city = City_Data[city]
            break
        else:
            print("\n\nSorry Invalid input try again! \n")
            continue
    
    while True:
        print("\nWould Do you like to Filter the Record Month, Day, Both or None? \n")             
        filter=input("Enter type of filter to Review its data: ").lower()
        if filter in ['month', "day" ,"both" ,"none"] :
            if filter == 'month':
                day = "all"
            elif filter == "day":
                month = "all"
            elif filter == "none":
                day =  month ="all"
            break
        else:
            print("\n\nSorry Invalid input try again! \n")
            continue
    
    if month != "all":
        while True:
            print("The avaliable months are: \n1-January\n2-February\n3-March\n4-April\n5-May\n6-June\n")
            month=input("Enter Number of the month to Review its data: ")
            if month.lower() in months: 
                break
            else:
                print("\n\nSorry Invalid input try again! \n")
                continue
    
    if day != "all":
        while True:
            print("Number of days are:\nSunday:\t\t1\nMonday:\t\t2\nTuesday:\t3\nWednesday:\t4\nThursday:\t5\nFriday:\t\t6\nSaturday:\t7\n")
            try:
                 day=int(input("Enter number of day to Review its data: "))
            except ValueError:
                print("\n\nSorry Invalid input try again! \n")
                continue
            if day in days: 
                day =dayOfWeek[day-1]
                break
            else:
                print("\n\nSorry Invalid input try again! \n")
                continue
    return city ,month , day
          
def load_data(city, month, day):
    """
    input:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (int) day - number of the day of week to filter by, or "all" to apply no day filter
    output:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    
    """Displays analysis on the most common times of travel."""
    
    print('\nPopular times of travel:\n')
    
    # most common month
    common_month = df['month'].mode()[0]
    print('The most common month: {} \n'.format(months[common_month-1]))
    
    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('The most day of week: {} \n'.format(common_day_of_week))
    
    # most common start hour

    common_start_hour = df['hour'].mode()[0]

    
    print('The most common hour of day: {} \n'.format(common_start_hour))
    print('*'*50)
    
def station_stats(df):
    """
    Displays Analysis on the most popular stations and trip.
    """

    print('\nPopular stations and trip:\n')
    # commonly used start station
    Common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station: {}\n'.format(Common_start_station) )
    
    # commonly used end station
    Common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station: {} \n'.format(Common_end_station))
    
    # most frequent combination of start station and end station trip
    Common_Terminal_Stations = df.groupby(['Start Station','End Station']).size().sort_values().tail(1)
    
    print('Most frequent combination of start station and end station:\n\nStart station: {} \n\nEnd station: {}\n'.format(Common_Terminal_Stations.index[0][0],Common_Terminal_Stations.index[0][1]))

    print('*'*50)
    
    
def trip_duration_stats(df):
    """
    Displays Analysis on the total and average trip duration.
    """

    print('\nTrip duration: \n')


    # total travel time
    total_travel_time = "{:.2f}".format(df['Trip Duration'].sum())
    print('Total travel time: {}\n'.format(total_travel_time))
    
    # mean travel time
    average_travel_time = "{:.2f}".format(df['Trip Duration'].mean())
    print('Average travel time: {}\n'.format(average_travel_time))

    print('*'*50)
    
def user_stats(df, city):
    """Displays Analysis on bikeshare users."""

    print('\n User info\n')

    # counts of user types
    print("\nThe counts of various user types:\n\nSibscribe: {}\n\nCustomer: {}\n".format(df['User Type'].value_counts()[0] ,df['User Type'].value_counts()[1]))
    

    Subscriber_rate =df["User Type"].value_counts()[0]/(df["User Type"].value_counts()[0]+df["User Type"].value_counts()[1]) *100
    Subscriber_ratio = "{:.2f}%".format(Subscriber_rate)
    print("\nSubscriber ratio: {}\n".format(Subscriber_ratio))
   
    
    Customer_rate =df["User Type"].value_counts()[1]/(df["User Type"].value_counts()[0]+df["User Type"].value_counts()[1]) *100
    Customer_ratio = "{:.2f}%".format(Customer_rate)
    print("\nCustomer ratio is {}\n".format(Customer_ratio))
   
    

    if city != 'washington':
        # Display counts of gender
        print("The counts of gender:\n\nMale: {}\n\nFemale: {}".format(df['Gender'].value_counts()[0],df['Gender'].value_counts()[1]))
        male_rate =df["Gender"].value_counts()[0]/(df["Gender"].value_counts()[0]+df["Gender"].value_counts()[1]) *100
        male_ratio = "{:.2f}%".format(male_rate)
        print("\nMale ratio is {}\n".format(male_ratio))
   
        
        female_rate =df["Gender"].value_counts()[1]/(df["Gender"].value_counts()[0]+df["Gender"].value_counts()[1]) *100
        female_ratio = "{:.2f}%".format(female_rate)
        print("\nFemale ratio is {}\n".format(female_ratio))

        # earliest, most recent, and most common year of birth
        print("\nThe earliest birth year: {}\n".format(int(df['Birth Year'].min())))
        
        print("\nThe latest birth year: {}\n".format(int(df['Birth Year'].max())))
        
        print("\nThe most common birth year: {}\n".format(int(df['Birth Year'].mode().values[0])))


    print('*'*50)
    
def display_record(df):
    """
    Display contents of the CSV file to the display as requested by
    the user.
    """


    current_row = 0
    while True:
        display_option = input("Would do you like to see record of data? \"Yes\" or \"No\" : ").lower()
        if display_option in option:
            break
        else:
            print("/nSorry, invalid input try again\n")
            continue
        
    if display_option == 'yes':
        while current_row + 5 <= df.shape[0] - 1:

            print(df.iloc[current_row:current_row + 5,:])
            current_row += 5
            while True:
                display_option = input("Do you wanna continue? \"Yes\" or \"No\" :  ").lower()
                if display_option in option:
                    break
                else:
                    print("/nSorry, invalid input try again\n")
                    continue
            
            if display_option == 'no':
                break
            
def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_record(df)

        while True:
            restart = input('\nWould you like to Analysis again? Enter yes or no.\n').lower()
            if restart in option:
                break
            else:
                print("\nSorry, invalid input try again\n")
                continue
            
        if restart == 'no':
            break


if __name__ == "__main__":
	main()
