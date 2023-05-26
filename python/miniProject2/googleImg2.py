from apiclient.discovery import build

service = build("customsearch", "v1",
                developerKey="")

res = service.cse().list(
    q='일본',
    cx='',
    searchType='image',
    num=10,
    imgType='clipart',
    fileType='png',
    safe='off'
).execute()

if not 'items' in res:
    print('No result !!\nres is: {}').format(res)
else:
    for item in res['items']:
        print('=================================================')
        print(item['title'])
        print(item['link'])
