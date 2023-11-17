import requests, json, random

def gettime():
    r = requests.get('http://worldtimeapi.org/api/timezone/Pacific/Auckland')
    data = json.loads(r.text)
    current_time = data['datetime']
    start = current_time.find('T') + 1  # find() returns the index of 'T', we add 1 to start from the next character
    end = current_time.find('.')  # find() returns the index of '.'
    return current_time[start:end]


def random_color():
    colors = [(186, 44, 115), (109, 59, 71), (69, 58, 73), (40, 47, 68), (25, 29, 50)]
    selected_color_tuple = random.choice(colors)
    #selected_color = selected_color_tuple
    return selected_color_tuple
    