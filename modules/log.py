def find(msg):
    msg = msg['body'][6:]
    with open('chatlog.log', 'r') as chatlog:
        chatlog = chatlog.read()
    chatlog = chatlog.split('\n')
    for line in chatlog:
        if msg in line:
            return line
    return ''