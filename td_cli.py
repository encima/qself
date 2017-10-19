import todoist
import config 

t_api = todoist.TodoistAPI(config.todoist['USER_TOKEN'])
#user = t_api.user.login_with_google(config.GOOGLE_EMAIL, config.GOOGLE_ACCESS)
res = t_api.sync()
print(res)
print(t_api.items.sync())
print(dir(t_api.items))
print(res.keys())
for project in res['projects']:
    print(project['name'])
