import time
import random
import os
import base64
import json
import yaml
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait



with open('var/config.yaml', 'r') as f:
    config = yaml.load(f)
    app_creds = config['app']

client_id = app_creds['client_id']
client_secret = app_creds['client_secret']
encoded_client_cred = base64.b64encode(bytes(f'{client_id}:{client_secret}', 'utf'))


with open('var/users.yaml', 'r') as f:
    users = yaml.load(f)








def login(email, password):
    """Login Fitbit User Accounts
    """

    # Open the login page.
    browser = Firefox()
    login_url = f"https://www.fitbit.com/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000&scope=sleep%20heartrate&expires_in=604800"
    browser.get(login_url)

    # Type in email ID.
    email_input = WebDriverWait(browser, 5).until(lambda x: x.find_element_by_css_selector('input#ember644'))
    # email_input = browser.find_element_by_css_selector('input#ember653')
    for l in email:
        email_input.send_keys(l)
        time.sleep(random.random()/4)
    time.sleep(1)

    # Type in password.
    password_input = browser.find_element_by_css_selector('input#ember645')
    for l in password:
        password_input.send_keys(l)
        time.sleep(random.random()/3)
    time.sleep(1.2)

    # Click login button.
    browser.find_element_by_css_selector('button#ember685').click()

    # Check AllScope box if not already selected
    try:
        WebDriverWait(browser, 5).until(lambda x: x.find_element_by_css_selector('input#selectAllScope'))
        browser.find_element_by_css_selector('input#selectAllScope').click()
        browser.find_element_by_css_selector('button#allow-button').click()
        time.sleep(5)
    except:
        pass
        
    browser.quit()












class AuthAppServer:
    """Auth Server that handles Code and Tokens.
    """
    @classmethod    
    def prop(self):
        os.system('netstat -anv | grep 127.0.0.1.5000 > var/ps.txt')
        server_ps = open('var/ps.txt').read()

        if '127.0.0.1.5000' not in server_ps: 
            os.system('flask run &')
            
        else:
            raise Exception
            
    
    @classmethod
    def shut(self):
        os.system('netstat -anv | grep 127.0.0.1.5000 > var/ps.txt')
        server_ps = open('var/ps.txt').read()
        server_pid = server_ps.split(' ')[-7]
        # server_pid = server_ps.replace(" ", "")[-7:-2]
        
        if '127.0.0.1.5000' in server_ps: 
            os.system(f'kill {server_pid}')
            
        else: 
            raise Exception












if __name__ == "__main__":
    # Start the Server
    try: 
        print('> starting the server...')
        AuthAppServer.prop()
    except: 
        print('> server running')
    time.sleep(3)








    # # Log in
    # for user in users:
    #     email = user['email']
    #     password = user['password']
    #     try: 
    #         print(f"> logging in: {email}")
    #         login(email, password)
    #     except: 
    #         print("> something went wrong, please try again.")


    for user_id in users.keys():
        account_id = users[user_id]['accountID']
        password = users[user_id]['password']
        try: 
            with open('var/user_id.txt', 'w+') as f:
                f.write(user_id)
            print(f"> logging in: {account_id}")
            login(account_id, password)
            
        except: 
            print("> something went wrong, please try again.")










    # end the server
    try: 
        print('> shutting down the server...')
        AuthAppServer.shut()
    except: 
        print('> server not found')