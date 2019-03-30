import os
os.getcwd()
from Handlers.menus import Menu, global_menu


def main():
    """
    Master menu that allows user to select which functions they'd like to run
    """
    menu_instance = Menu(global_menu)
    user_input = input(global_menu)
    while user_input != 'q':
        if user_input == 'm':
            menu_instance.sms()
        elif user_input == 'e':
            menu_instance.emails()

        print('\n')
        menu_again = input('Would you like to see the menu again? (y/n): ')
        if menu_again == 'y':
            user_input = input(global_menu)
        elif menu_again == 'n':
            break
        else:
            print('Unknown command.')
            user_input = input(global_menu)


if __name__ == '__main__':
    main()