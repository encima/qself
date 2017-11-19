import todoist
import configparser

class TaskHandler:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') 
        self.t_api = todoist.TodoistAPI(self.config['todoist']['USER_TOKEN'])
        #user = t_api.user.login_with_google(config.GOOGLE_EMAIL, config.GOOGLE_ACCESS)

    def sync(self):        
        res = self.t_api.sync()
        print(res)
        print(self.t_api.items.sync())
        print(dir(self.t_api.items))
        print(res.keys())
        for project in res['projects']:
            print(project['name'])
