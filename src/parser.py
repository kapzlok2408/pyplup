import json

"""
A collection of parsing functions to parse Server-to-Client messages.
As a battle bot, user messages can be ignored. Of particular interest
are messages pertaining to starting battles and logins.
"""

def parse(roomid: str, message: str) -> dict:
    tokens = message.split('|')
    #remove empty first token
    tokens = tokens[1:]
    type = tokens[0]
    parse_func = {
        "init" : init,
        "title" : title,
        "users" : users,
        "join" : join,
        "j" : join,
        "J" : join,
        "leave" : leave,
        "l" : leave,
        "L" : leave,
        "battle" : battle,
        "b" : battle,
        "usercount" : usercount,
        "nametaken" : nametaken,
        "challstr" : challstr,
        "updateuser" : updateuser,
        "formats" : formats,
        "updatesearch" : updatesearch,
        "updatechallenges" : updatechallenges,
        "queryresponse" : queryresponse
    }.get(type, unrecognized)
    parsed = parse_func(tokens)
    parsed["ROOMID"] = roomid
    return parsed

def unrecognized(tokens: [str]) -> dict:
    return {
        "TYPE" : "unrecognized",
    }

"""
Room initialization
"""

#|init|ROOMTYPE
def init(tokens: [str]) -> dict:
    return {
        "TYPE" : "init",
        "ROOMTYPE" : tokens[1]
    }

#|title|TITLE
def title(tokens: [str]) -> dict:
    return {
        "TYPE" : "title",
        "TITLE" : tokens[1]
    }

#|users|USERLIST
def users(tokens: [str]) -> dict:
    return {
        "TYPE" : "users",
        "TITLE" : json.loads(tokens[1])
    }

"""
Room messages
"""
#|join|USER or |j|USER or |J|USER
def join(tokens: [str]) -> dict:
    return {
        "TYPE" : "join",
        "USER" : tokens[1]
    }

#|leave|USER or |l|USER or |L|USER
def leave(tokens: [str]) -> dict:
    return {
        "TYPE" : "leave",
        "USER" : tokens[1]
    }

#|battle|ROOMID|USER1|USER2 or |b|ROOMID|USER1|USER2
def battle(tokens: [str]) -> dict:
    return {
        "TYPE" : "battle",
        "ROOMID" : tokens[1],
        "USER1" : tokens[2],
        "USER2" : tokens[3]
    }

"""
Global messages
"""

#|usercount|USERCOUNT
def usercount(tokens: [str]) -> dict:
    return {
        "TYPE" : "usercount",
        "USERCOUNT" : int(tokens[1])
    }

#|nametaken|USERNAME|MESSAGE
def nametaken(tokens: [str]) -> dict:
    return {
        "TYPE" : "nametaken",
        "USERNAME" : tokens[1],
        "MESSAGE" : tokens[2]
    }

#|challstr|CHALLSTR
def challstr(tokens: [str]) -> dict:
    #CHALLSTR contains '|' characters
    #so it might have been tokenized wrongly
    challstr = ""
    for token in tokens[1:-1]:
        challstr += token + "|"
    challstr += tokens[-1]
    return {
        "TYPE" : "challstr",
        "CHALLSTR" : challstr
    }

#|updateuser|USER|NAMED|AVATAR|SETTINGS
def updateuser(tokens: [str]) -> dict:
    return {
        "TYPE"     : "updateuser",
        "USER"     : tokens[1],
        "NAMED"    : int(tokens[2]),
        "AVATAR"   : int(tokens[3]),
        "SETTINGS" : json.loads(tokens[4])
    }

#|formats|FORMATSLIST
def formats(tokens: [str]) -> dict:
    #group formats by section headers
    format_sections = {}
    new_section = False
    for token in tokens[1:]:
        if new_section:
            current_section = token
            format_sections[current_section] = []
            new_section = False
        elif token[0] == ',':
            new_section = True
        else:
            format_sections[current_section].append(token)
    return {
        "TYPE" : "formats",
        "FORMATSLIST" : format_sections
    }

#|updatesearch|JSON
def updatesearch(tokens: [str]) -> dict:
    return {
        "TYPE" : "updatesearch",
        "JSON" : json.loads(tokens[1])
    }

#|updatechallenges|JSON
def updatechallenges(tokens: [str]) -> dict:
    return {
        "TYPE" : "updatechallenges",
        "JSON" : json.loads(tokens[1])
    }

#|queryresponse|QUERYTYPE|JSON
def queryresponse(tokens: [str]) -> dict:
    return {
        "TYPE" : "queryresponse",
        "QUERYTYPE" : tokens[1],
        "JSON" : json.loads(tokens[2])
    }