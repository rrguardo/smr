
Feature: Basic User Tests
    Testing user login and signup
    
    Scenario Outline: User signup
        Given I go to "http://127.0.0.1:5000/user/register/"
            When I fill in "username" with "<user_name>"
                And I fill in "email" with "<user_email>"
                And I fill in "password" with "<user_passw>"
                And I fill in "confirm" with "<user_pconfirm>"
                And I check "accept_tos"
                And I press "Register"
            Then I should see "Thanks for registering"
                And The browser's URL should contain "/user/login/"
    
    Examples:
        | user_name | user_passw | user_pconfirm | user_email                        | 
        | admin      | 1234567      | 1234567          | admin@flaskapp.com | 
        | guest        | 1234567      | 1234567          | quest@flaskapp.com   |
    
    Scenario Outline: User login
        Given I go to "http://127.0.0.1:5000/user/login/"
            When I fill in "username" with "<user_name>"
                And I fill in "password" with "<user_passw>"
                And I press "Login"
            Then I should see "Username: <user_name>"
                And The browser's URL should contain "/user/panel/"
    
    Examples:
        | user_name | user_passw |
        | admin      | 1234567      |
        | guest        | 1234567      |
    
    Scenario Outline: Unauthorized login
        Given I go to "http://127.0.0.1:5000/user/login/"
            When I fill in "username" with "<user_name>"
                And I fill in "password" with "<user_passw>"
                And I press "Login"
            Then I should see "Incorrect username or password"
                And The browser's URL should contain "/user/login/"
                And I should not see "Username: <user_name>"
                And The browser's URL should not contain "/user/panel/"
    
    Examples:
        | user_name | user_passw |
        | admin      | E23456E      |
        | guest        | E23456E      |
        | hacker      | HK3456E    |
    

