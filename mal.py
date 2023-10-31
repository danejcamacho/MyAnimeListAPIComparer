import json
import requests
import secrets


CLIENT_ID = 'c0708faac979da25a937fb76363d2b90'
##CLIENT_SECRET = PUT SECRET KEY HERE


# 1. Generate a new Code Verifier / Code Challenge.
def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]


# 2. Print the URL needed to authorise your application.
def print_new_authorisation_url(code_challenge: str):
    global CLIENT_ID

    url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&code_challenge={code_challenge}'
    print(f'Authorise your application by clicking here: {url}\n')


# 3. Once you've authorised your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
#    Code). You need to feed that code to the application.
def generate_new_token(authorisation_code: str, code_verifier: str) -> dict:
    global CLIENT_ID, CLIENT_SECRET

    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': authorisation_code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the request contains errors

    token = response.json()
    response.close()
    print('Token generated successfully!')

    with open('token.json', 'w') as file:
        json.dump(token, file, indent = 4)
        print('Token saved in "token.json"')

    return token


# 4. Test the API by requesting your profile information
def print_user_info(access_token: str):
    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers = {
        'Authorization': f'Bearer {access_token}'
        })
    
    response.raise_for_status()
    user = response.json()
    response.close()

    print(f"\n>>> Greetings {user['name']}! <<<")
    
def print_suggested_anime(access_token: str, how_many: str):
    url = 'https://api.myanimelist.net/v2/anime/suggestions?limit='
    url += how_many
    response = requests.get(url, headers = {
        'Authorization': f'Bearer {access_token}'
        })
    
    response.raise_for_status()
    user = response.json()
    response.close()
    for value in user['data']:
        print(value['node']['title'])
        
def print_other_user_list(user_name: str):
    
    are_more = True
    offset = 0
    loop_count = 0
    
    while(are_more):
        url = 'https://api.myanimelist.net/v2/users/' + user_name + '/animelist?limit=100&offset='
        url += str(offset)
        response = requests.get(url, headers = {
            'X-MAL-CLIENT-ID' : CLIENT_ID
            })
        
        response.raise_for_status()
        user = response.json()
        response.close()
        offset += 100
        loop_count += 1
        
        #print out
        for value in user['data']:
            print(value['node']['title'])
        
        
        if(not user['data'] or loop_count > 10):
            are_more = False
        
def print_my_list(access_token: str):
    
    are_more = True
    offset = 0
    loop_count = 0
    
    while(are_more):
        url = 'https://api.myanimelist.net/v2/users/@me/animelist?limit=100&offset='
        url += str(offset)
        response = requests.get(url, headers = {
            'Authorization': f'Bearer {access_token}'
            })
        
        response.raise_for_status()
        user = response.json()
        response.close()
        offset += 100
        loop_count += 1
        
        #print out
        for value in user['data']:
            print(value['node']['title'])
        
        
        if(not user['data'] or loop_count > 10):
            are_more = False
    
def print_ptw_in_common(user1: str, user2: str):
    
    def intersection(lst1, lst2):
        return [value for value in lst1 if value in lst2]
    
    ### USER 1 ###
    
    user1_list = []
    are_more = True
    offset = 0
    loop_count = 0
    
    while(are_more):
        url = 'https://api.myanimelist.net/v2/users/'+ user1 + '/animelist?status=plan_to_watch&limit=100&offset='
        url += str(offset)
        response = requests.get(url, headers = {
            'X-MAL-CLIENT-ID' : CLIENT_ID
            })
        
        response.raise_for_status()
        user = response.json()
        response.close()
        offset += 100
        loop_count += 1
        
        #append to user1 list
        for value in user['data']:
            user1_list.append(value['node']['title'])
        
        
        if(not user['data'] or loop_count > 10):
            are_more = False
            
    ### USER 2 ###
            
    user2_list = []
    are_more = True
    offset = 0
    loop_count = 0
    
    while(are_more):
        url = 'https://api.myanimelist.net/v2/users/'+ user2 + '/animelist?status=plan_to_watch&limit=100&offset='
        url += str(offset)
        response = requests.get(url, headers = {
            'X-MAL-CLIENT-ID' : CLIENT_ID
            })
        
        response.raise_for_status()
        user = response.json()
        response.close()
        offset += 100
        loop_count += 1
        
        #append to user2 list
        for value in user['data']:
            user2_list.append(value['node']['title'])
        
        
        if(not user['data'] or loop_count > 10):
            are_more = False
    
    print('\n***Plan To Watch in common***')
    for show in intersection(user1_list, user2_list):
        print(show)

    
def print_watched_watching_in_common(user1: str, user2: str):
    
    def intersection(lst1, lst2):
        return [value for value in lst1 if value in lst2]
    
    ### USER 1 ###
    
    user1_list = []
    are_more = True
    offset = 0
    loop_count = 0
    
    while(are_more):
        url = 'https://api.myanimelist.net/v2/users/'+ user1 + '/animelist?status=plan_to_watch&limit=100&offset='
        url += str(offset)
        response = requests.get(url, headers = {
            'X-MAL-CLIENT-ID' : CLIENT_ID
            })
        
        response.raise_for_status()
        user = response.json()
        response.close()
        offset += 100
        loop_count += 1
        
        #append to user1 list
        for value in user['data']:
            user1_list.append(value['node']['title'])
        
        
        if(not user['data'] or loop_count > 10):
            are_more = False
            
    ### USER 2 ###
            
    user2_list = []
    are_more = True
    offset = 0
    loop_count = 0
    
    while(are_more):
        url = 'https://api.myanimelist.net/v2/users/'+ user2 + '/animelist?status=plan_to_watch&limit=100&offset='
        url += str(offset)
        response = requests.get(url, headers = {
            'X-MAL-CLIENT-ID' : CLIENT_ID
            })
        
        response.raise_for_status()
        user = response.json()
        response.close()
        offset += 100
        loop_count += 1
        
        #append to user2 list
        for value in user['data']:
            user2_list.append(value['node']['title'])
        
        
        if(not user['data'] or loop_count > 10):
            are_more = False
    
    print('\n***Plan To Watch in common***')
    for show in intersection(user1_list, user2_list):
        print(show)
    


if __name__ == '__main__':
    #####OPTIONAL TOKEN GENERATION#####
    
    # code_verifier = code_challenge = get_new_code_verifier()
    # print_new_authorisation_url(code_challenge)

    # authorisation_code = input('Copy-paste the Authorisation Code: ').strip()
    # token = generate_new_token(authorisation_code, code_verifier)

    # print_user_info(token['access_token'])
    
    
    is_running = True
    
    while(is_running):
        print("""
              *** MAL API MAIN MENU ***
              1. Print My Info ***NEEDS TOKEN***
              2. Print My Suggested Anime ***NEEDS TOKEN***
              3. Print Another User's Animelist[ALL]
              4. Print My Animelist[ALL] ***NEEDS TOKEN***
              5. Compare two plan to watch lists
              
              type 'quit' to exit...
              
              """)
        choice = input("Enter menu choice: ")
        match choice:
            case '1': 
                pass
                #print_user_info(token['access_token'])
            case '2':
                how_many_input = input('How many suggestions: ')
                #print_suggested_anime(token['access_token'],how_many_input)
            case '3':
                user_name = input('Input a user: ')
                try:
                    print_other_user_list(user_name)
                except:
                    print("***ERROR***: A valid user!")
            case '4':
                pass
                #print_my_list(token['access_token'])
            case '5':
                user1_name = input('Input a username: ')
                user2_name = input('Input another username: ')
                print_ptw_in_common(user1_name, user2_name)
                
                
                
            case 'quit':
                is_running = False
                print('Quitting Application...')
            
