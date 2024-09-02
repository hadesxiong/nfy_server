# coding=utf8
import json,requests

def send_ntfy_nfy(**kwargs):

    defaults = {
        'topic': None,
        'message': None,
        'title': None,
        'priority': 3,
        'click': None,
        'icon': None
    }

    for k,v in defaults.items():
        defaults[k] = kwargs.get(k,v)

    cleaned_data = {k: v for k, v in defaults.items() if v}

    if cleaned_data['topic'] and cleaned_data['message']:

        try:
            url = kwargs.get('chnl_host',None) + '/'
            headers = {"Authorization": kwargs.get('ntfy_auth',None)}
            json_data = json.dumps(cleaned_data)
            response = requests.request('POST',url,headers=headers,data=json_data)
            return {"res": "success","code": response.status_code}
        
        except requests.RequestException as e:
            return {'res': 'request exception:' + str(e), 'code': 40001}
        except Exception as e:
            return {'res': 'fail to request:' + str(e), 'code':40002}
        
    else:
        return {'res': 'err topic or message', 'code': 40003}