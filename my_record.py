"""
Assignment 4 - Final Coding Challenge
1.s3961136 - Benjaporn Wongmayura
2.The highest part I have attempted: DI level
3.Any problem of your code and requirements that you have not met: -

Reflection:
1. Need to name the variables differently since there are many times
Python did not know which variable I referred to
2. Should learn more about command line arguments
3. Should learn more about getter setter
4. Should learn more about how to write code in Object-oriented programming style

"""
import sys


# create User class to store user
class User:
    def __init__(self, username, firstname, lastname):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.spent = 0
        # Note: first for Standard, second for Premium
        self.service_no = [0, 0]

    def compute_nservice(self, service_type):
        if service_type == "Standard":
            self.service_no[0] += 1
        elif service_type == "Premium":
            self.service_no[1] += 1


class FreeUser(User):

    user_type = "Free"

    def __init__(self, username, firstname, lastname):
        """ Initialize the attributes from the parent class"""
        super().__init__(username, firstname, lastname)

    def compute_spent(self, service, usage):
        if service.service_type == "Standard":
            self.spent += float(service.price) * float(usage)
        elif service.service_type == "Premium":
            self.spent += float(service.price1) * float(usage)


class PersonalUser(User):
    user_type = "Personal"

    def __init__(self, username, firstname, lastname):
        """ Initialize the attributes from the parent class"""
        super().__init__(username, firstname, lastname)

    def compute_spent(self, service, usage):
        if service.service_type == "Premium":
            self.spent += float(service.price1) * float(usage)


class CorporateUser(User):
    user_type = "Corporate"

    def __init__(self, username, firstname, lastname):
        """ Initialize the attributes from the parent class"""
        super().__init__(username, firstname, lastname)

    def compute_spent(self, service, usage):
        if service.service_type == "Premium":
            self.spent += float(service.price2) * float(usage)

# create Service class to store service
class Service:

    def __init__(self, service_id, service_name):
        self.id = service_id
        self.name = service_name
        self.no_of_users = 0
        self.usage = 0

    def compute_nuser(self, service_id):
        if self.id == service_id:
            self.no_of_users += 1

    def compute_usage(self, service_id, usage):
        if self.id == service_id:
            self.usage += usage


class StandardService(Service):

    service_type = "Standard"

    def __init__(self, service_id, service_name, service_price):
        """ Initialize the attributes from the parent class"""
        super().__init__(service_id, service_name)
        self.price = service_price


class PremiumService(Service):
    service_fee_rate = 0.8
    service_type = "Premium"

    def __init__(self, service_id, service_name, service_price):
        """ Initialize the attributes from the parent class"""
        super().__init__(service_id, service_name)
        self.price1 = service_price
        self.price2 = round(float(service_price) * float(self.service_fee_rate), 1)

    # use normal getter setter
    # getter # use getter to read the value
    def get_service_fee_rate(self):
        return self.service_fee_rate

    # setter # use setter to update the value
    @staticmethod
    def set_service_fee_rate(self, service_fee_rate):
        self.service_fee_rate = service_fee_rate


class Records:
    """create class to record the user and service"""
    # create custom list to store user
    user_list = []
    # create custom list to store service
    service_list = []
    # create list to store service_id for looping
    service_id_list = []
    # create list to store usage for looping. key:service_id, value: usage
    total_usage = {}

    def read_records(self):
        file_name = sys.argv[1]
        input_file = open(file_name, "r")
        line_from_file = input_file.readline()
        while line_from_file:
            fields_from_line = line_from_file.split(",")
            username = fields_from_line[0].strip()
            self.total_usage[username] = {}
            for n in range(1, len(fields_from_line), 2):
                service_id = fields_from_line[n].strip()
                if service_id not in self.service_id_list:
                    self.service_id_list.append(service_id)
                usage = float(fields_from_line[n + 1].strip())
                self.total_usage[username][service_id] = usage
            line_from_file = input_file.readline()
        input_file.close()

    def display_records(self):
        usage_count = 0
        print("RECORDS")
        service_id_list = []
        # loop trough service_list to append to service_id_list then populate
        # each service_id to get row for ServiceID header S01  S02  S03...
        for service in self.service_list:
            service_id_list.append(service.id)
        print("-"*125)
        print(f"{'Username':<15}", end='')
        for service in self.service_id_list:
            print("{:>15}".format(service), end='')
        print()
        print("-"*125)
        # loop through user to get the username
        for user in self.total_usage:
            print("{:<27}".format(user), end='')
            # add value to dictionary by using key
            services = self.total_usage[user]
            usage_count += len(services)
            for service_id in self.service_id_list:
                if service_id in services:
                    # use the key(service_id) of dictionary(services) to access
                    # value(usage)
                    print("{:<15}".format(services[service_id]), end='')
                else:
                    print(f"{'--':<15}", end='')
            print()
        no_users = len(self.total_usage)
        no_services = len(self.service_id_list)
        total_usage_count = no_users * no_services
        usage_percentage = (usage_count/total_usage_count)*100

        print("\nRECORDS SUMMARY")
        print(f'There are {no_users} users and {no_services} services')
        print(f'The usage percentage is {usage_percentage:.2f}%')

    def read_services(self):
        file_name = sys.argv[2]
        input_file = open(file_name, "r")
        line_from_file = input_file.readline()
        while line_from_file:
            fields_from_line = line_from_file.split(",")
            service_id = fields_from_line[0].strip()
            service_name = fields_from_line[1].strip()
            service_price = float(fields_from_line[3].strip())
            service_type = fields_from_line[2].strip()
            if service_type == "Standard":
                service = StandardService(service_id, service_name, service_price)
            if service_type == "Premium":
                service = PremiumService(service_id, service_name, service_price)
            # loop through total_usage to get key(usernames) and value(services)
            for usernames, services in self.total_usage.items():
            # loop again since this case is the dictionary inside dictionary
            # loop through dictionary(services) to get key(service_id) and value(usage)
                for service_id, usage in services.items():
                    # call method from service class to calculate
                    service.compute_nuser(service_id)
                    service.compute_usage(service_id, usage)
            self.service_list.append(service)
            line_from_file = input_file.readline()
        input_file.close()

    def display_services(self):
        print("SERVICE INFORMATION")
        print("-" * 125)
        print(f"{'ServiceID':<15}{'Name':<15}{'Type':<15}{'Price':>16}{'Nuser':>15}{'Usage':>15}")
        print("-" * 125)
        max_no_users = 0
        most_expensive = 0
        most_popular_service = " "
        most_expensive_service_name = " "
        most_expensive_service_id = 0
        compared_price = 0
        # print the attributes of by calling service object
        for service in self.service_list:
            if service.service_type == "Standard":
                print("{:<15}{:<15}{:<15}{:>16}{:>15}{:>15.1f}  ".format(service.id, service.name, service.service_type,
                                                             service.price, service.no_of_users, service.usage))
                compared_price = float(service.price)
            if service.service_type == "Premium":
                print("{:<15}{:<15}{:<15}{:>10} / {}{:>15}{:>15.1f} ".format(service.id, service.name, service.service_type,
                                                                   service.price1, service.price2, service.no_of_users
                                                                    , service.usage))
                compared_price = float(service.price1)
            number_of_users = service.no_of_users
            if number_of_users > max_no_users:
                max_no_users = number_of_users
                most_popular_service = service.name
            if compared_price > most_expensive:
                most_expensive = compared_price
                most_expensive_service_id = service.id
                most_expensive_service_name = service.name
        print()
        print("SERVICE SUMMARY")
        print(f'There most popular service is {max_no_users} {most_popular_service}')
        print(f'The most expensive service (per unit) is {most_expensive_service_id}'
              f' {most_expensive_service_name}.')

    def read_users(self):
        file_name = sys.argv[3]
        input_file = open(file_name, "r")
        line_from_file = input_file.readline()
        while line_from_file:
            fields_from_line = line_from_file.split(",")
            user_name = fields_from_line[0].strip()
            user_firstname = fields_from_line[1].strip()
            user_lastname = fields_from_line[2].strip()
            user_type = fields_from_line[3].strip()
            #create user object according to different type of user
            if user_type == "Free":
                user = FreeUser(user_name, user_firstname, user_lastname) ## review here
            if user_type == "Personal":
                user = PersonalUser(user_name, user_firstname, user_lastname)
            if user_type == "Corporate":
                user = CorporateUser(user_name, user_firstname, user_lastname)

            for username, services in self.total_usage.items():
                if username == user.username:
                    for service_id, usage in services.items():
                        print('compute works')
                        # call service object from the find_service method below
                        service = self.find_service(service_id)
                        # compute
                        print(service.service_type)
                        user.compute_spent(service, usage)
                        user.compute_nservice(service.service_type)
            self.user_list.append(user)
            line_from_file = input_file.readline()
        print(self.user_list)
        input_file.close()

    def find_service(self, service_id):
        for service in self.service_list:
            if service_id == service.id:
                return service



    def display_users(self):
        print(self.user_list)
        print("USER INFORMATION")
        print("-" * 125)
        print(f"{'Username':<20}{'First name':<15}{'Last Name':<15}{'Type':>16}{'Spent':>15}{'Nservice':>22}")
        print("-" * 125)
        max_spending = 0
        most_valuable_user = " "
        most_used_user = " "
        max_services_count = 0
        # loop through user to get the username
        for user in self.user_list:

            if user.user_type == "Free":
                print("{:<20}{:<15}{:<15}{:>16}{:>15.2f} {:>15}S +{:>2}P ".format(user.username, user.firstname,
                                                                         user.lastname, user.user_type, user.spent,
                                                                            user.service_no[0], user.service_no[1]
                                                                            ))
            if user.user_type == "Personal":
                print("{:<20}{:<15}{:<15}{:>16}{:>15.2f} {:>15}S +{:>2}P ".format(user.username, user.firstname,
                                                          user.lastname, user.user_type, user.spent,
                                                        user.service_no[0], user.service_no[1]
                                                                           ))
            if user.user_type == "Corporate":
                print("{:<20}{:<15}{:<15}{:>16}{:>15.2f} {:>15}S +{:>2}P ".format(user.username, user.firstname,
                                                          user.lastname, user.user_type, user.spent,
                                                                     user.service_no[0], user.service_no[1]))
            user_spending = user.spent
            if user_spending > max_spending:
                max_spending = user_spending
                most_valuable_user = user.username
            service_count = int(user.service_no[0]) + int(user.service_no[1])
            if service_count > max_services_count:
                max_services_count = service_count
                most_used_user = user.username
        print()
        print("USER SUMMARY")
        print(f'The most valuable user is {most_valuable_user}')
        print(f'The user that used services the most was {most_used_user} ')

        print()


class Operations:

    def run_operations(self):
        try:
            # This message is shown when no record file is passed in as a command line argument
            if len(sys.argv) == 1:
                print('[Usage:] python my_record.py <records file> <services file> <users file>')
            # case when only one file passed in via the command line
            if len(sys.argv) == 2:
                record = Records()
                record.read_records()
                while True:
                    choice = self.get_menu_choice()
                    print(choice)
                    if choice == 1:
                        # record.read_records()
                        record.display_records()
                    if choice == 0:
                        exit()
            # case when only two files passed in via the command line
            if len(sys.argv) == 3:
                record = Records()
                record.read_records()
                record.read_services()
                while True:
                    choice = self.get_menu_choice()
                    print(choice)
                    if choice == 1:
                        # record.read_records()
                        record.display_records()
                    if choice == 2:
                        # record.read_services()
                        record.display_services()
                    if choice == 0:
                        exit()
            # case when only three files passed in via the command line
            if len(sys.argv) == 4:
                record = Records()
                record.read_records()
                record.read_services()
                record.read_users()
                while True:
                    choice = self.get_menu_choice()
                    print(choice)
                    if choice == 1:
                        # record.read_records()
                        record.display_records()
                    if choice == 2:
                        # record.read_services()
                        record.display_services()
                    if choice == 3:
                        # record.read_users()
                        record.display_users()
                    if choice == 0:
                        exit()


        except FileNotFoundError:
            print('Can not find the file!')

    def get_menu_choice(self):
        menu = "\nWelcome to the RMIT Service Provider Dashboard!\n"
        menu += "\n#################################################################\n"
        menu += "You can choose from the following options: \n"
        menu += "1: Display records\n"
        if len(sys.argv) == 3:
            menu += "2: Display services\n"
        if len(sys.argv) == 4:
            menu += "2: Display services\n"
            menu += "3: Display users\n"
        menu += "0: Exit the program\n"
        menu += "\n#################################################################\n"

        print(menu)
        return int(input("Enter your choices: ").strip())


service_operation_manager = Operations()
service_operation_manager.run_operations()
