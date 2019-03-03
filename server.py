#!/usr/bin/env python
from flask import Flask


from OpenSSL import SSL
# context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt')

import urllib
import json
import os

import pdb,json
from random import randint
import ast
from flask import Flask
from flask import request
from flask import make_response
import pymysql, requests, json
import datetime
from pymemcache.client import base

# Flask app should start in global layout
app = Flask(__name__)
# db = pymysql.connect('localhost','root','','umd')
client = base.Client(('localhost', 11211))
days = {0:"%%M%", 1:"%Tu%", 2:"%%W%", 3:"%Th%", 4:"%%F%", 5:"%%Sa%", 6:"%%Su%"}
@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)

    res = makeWebhookResult(req)

    res = json.dumps(res)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def cthulhu():
    msg = "You walk for miles into what seems like an endless abyss.\n And then he presents himself. \n<emphasis level='strong'> The evil Cthulhu.</emphasis> \n He, it, or whatever - stares at you and you go insane. Do you flee for your life or Fight Cthulhu?"
    suggestion = [{"title": "Flee"},{"title": "Fight Cthulhu"}]
    return (msg,suggestion)

def prince():
    msg = "You have been walking for miles... and this is geting frustrating. Will this road ever end? A dagger falls from the skies above. What do you do?"
    suggestion = [{"title": "pick the dagger"}]
    return (msg,suggestion)

def dagger():
    msg = "lo and behold! A handsome prince stands before you. A diamond on the hilt of your dagger turns the color of his hair, Something seems wrong."
    msg += "\nDo you see the color?\n"
    suggestion = [{"title": "Yes, It looks like Blood."},{"title": "No, Its nothing."}]
    return (msg,suggestion)

def blood():
    msg = "You'll have to make a choice. You can either Flee or Attack him with your dagger. Which will it be?"
    suggestion = [{"title": "Flee"},{"title": "Fight Prince"}]
    return (msg,suggestion)

def dragon():
    msg = "You had to choose some direction and you chose West. You have been walking for miles.... and you're thirsty, and dehydrated."+"\n... you have just begun to feel you're walking into eternity when you see a T-junction.<break time='3s'/> But just then you hear a ROAR!!!"+"\nYou turn back to see a giant elder dragon, miles away, flying towards you at great speed. You just have time to react. What now?"
    suggestion = [{"title": "Duck under a nearby rock"},{"title": "Flee towards entrance"},{"title": "Fight Dragon"}]
    return (msg,suggestion)

def deadend():
    msg = "This seems like a dead end with a giant door blocking your way, you probably need a key to open it."
    suggestion = [{"title": "Go back to entrance"}]
    return (msg,suggestion)

def fight():
    msg = "You draw your weapon and slash at you enemy. Your fate now rests in the hands of Chance, Roll a 6 sided die and your success depends on getting a score of more than half."
    suggestion = [{"title": "Roll Die"}]
    return (msg,suggestion)

def RollDie():
    DEATH ="https://storage.googleapis.com/master-hoo.appspot.com/death.jpg"
    END = "https://storage.googleapis.com/master-hoo.appspot.com/end.png"
    score  = randint(1, 6)
    if(score>3):
        msg = "Lady Luck sides with you, as the die rolls "+ str(score) +" and you vanquish your enemy."
        suggestion = [{"title": "A portal opens infront!"}]
    else:
        msg = "How unfortunate! Lady Luck has eluded you as you land a score of "+ str(score) +" , You face defeat."
        suggestion = [{"title": "Andd..."}]
    return (msg,suggestion)

def makeWebhookResult(req):
    suggestion=[]
    ImageURL = ""
    msg=""
    media = ""
    display_text = ""
    hints = client.get('hints', False)
    TREE = "https://storage.googleapis.com/master-hoo.appspot.com/deadTree.png"
    FOREST = "https://storage.googleapis.com/master-hoo.appspot.com/forest.png"
    CTHULU = "https://storage.googleapis.com/master-hoo.appspot.com/cthulu.png"
    DAGGER = "https://storage.googleapis.com/master-hoo.appspot.com/dagger.png"
    DEATH ="https://storage.googleapis.com/master-hoo.appspot.com/death.jpg"
    DEADEND = "https://storage.googleapis.com/master-hoo.appspot.com/download.jpeg"
    DRAGON = "https://storage.googleapis.com/master-hoo.appspot.com/dragon.gif"
    DRAGON_FIRE = "https://storage.googleapis.com/master-hoo.appspot.com/dragon_fire.gif"
    ATTACK = "https://storage.googleapis.com/master-hoo.appspot.com/attack.gif"
    DICE = "https://storage.googleapis.com/master-hoo.appspot.com/dice.jpg"
    END = "https://storage.googleapis.com/master-hoo.appspot.com/end.png"
    print(hints)
    prev_intent = client.get('prev_intent', "").lower()
    expectUserResponse = True
    parameters = req.get("queryResult")
    # print hints
    userId =  req.get("originalDetectIntentRequest", {}).get("payload", {}).get("user", {}).get("userId", "")
    # cur = db.cursor(pymysql.cursors.DictCursor)
    intent = parameters.get("queryText","").lower()
    if intent == "google_assistant_welcome":
        ImageURL = FOREST
        msg ="You have awakened Dungeon Master Hoo!<break time='0.5'/>Welcome to the terrifying world of the imagination.\n"
        msg += "You are walking through an enchanted forest with gigantic trees as tall as mountains and as thick as large lakes.\n"+"You see one such tree with a cave-like structure at its base. What do you do?"
        suggestion = [{"title": "Enter Cave"},{"title": "Run Away"}] 
    elif "run" in intent and "welcome" in prev_intent:
        msg = "You have no choice but to enter the cave. Now let's start over"
        suggestion = [{"title": "Enter Cave"}] 
    elif "cave" in intent or "flee" in intent or "go back" in intent:
        ImageURL = TREE
        msg = "You enter  the dark hollow of an ancient tree that has had earthlings like you in the past. \n\
            This tree is called the tree of the undying, where death won't touch you. \n\
            On the other hand, pain can - if you don't make the right moves. And then you have to live with the pain for eternity. \n\
            You are suddenly sucked into a vortex, finding yourself at crossroads of sorts.\n\
            From here, you can go north, south, east or west."
        suggestion = [{"title": "North"},{"title": "South"},{"title": "East"},{"title": "West"}] 
    elif "north" in intent and ("cave" in prev_intent or "flee" in prev_intent or "go back" in prev_intent):
        ImageURL = CTHULU
        (msg,suggestion) = cthulhu()
    elif "south" in intent and ("cave" in prev_intent or "flee" in prev_intent or "go back" in prev_intent):
        ImageURL = DAGGER
        (msg,suggestion) = prince()
    elif "east" in intent and ("cave" in prev_intent or "flee" in prev_intent or "go back" in prev_intent):
        ImageURL = DEADEND
        (msg,suggestion) = deadend()
    elif "west" in intent and ("cave" in prev_intent or "flee" in prev_intent or "go back" in prev_intent):
        (msg,suggestion) = dragon()
        media = "<media begin='15s' soundLevel='9db'> <audio src='https://storage.googleapis.com/master-hoo.appspot.com/dragon1.wav'/></media>"
        ImageURL = DRAGON
    elif "dagger" in intent and "south" in prev_intent:
        (msg,suggestion) = dagger()
    elif "portal" in intent and "roll" in prev_intent:
        msg = "You have made excellent choices and your journey is complete as You are magically transported out of the forest." 
        ImageURL = END
        expectUserResponse = False
    elif "fight cthulhu" in intent:
        msg = "</prosody></speak><media end='1s'> NONE SHALL SURVIVE! TIME TO DIE!\n THIS IS THE END OF YOUR WORLD! \n WITNESS MY POWER!!</media><speak><prosody>"
        ImageURL = CTHULU
        media = "<media begin='1s'> <audio src='https://storage.googleapis.com/master-hoo.appspot.com/cthulu.ogg'/></media>"
        display_text = "NONE SHALL SURVIVE! TIME TO DIE!\n THIS IS THE END OF YOUR WORLD! \n WITNESS MY POWER!!"
        suggestion = [{"title": "Andd..."}]
    elif "exit" in intent or "andd..." in intent:
        ImageURL = DEATH
        msg = "Wrong move friend, You stood no chance. You shall be lost forever into the infinite abyss of the tree of the undead."
        suggestion = [{"title": "Restart and Enter Cave"}]
        # expectUserResponse = False
    elif "blood" in intent and "dagger" in prev_intent:
        (msg,suggestion) = blood()
    elif "duck" in intent and "west" in prev_intent:
        ImageURL = DRAGON_FIRE
        msg = "Wrong move friend, the dragon breathes fire and burns you to a crisp.\n You shall be lost forever into the infinite abyss of the tree of the undead."
        suggestion = [{"title": "Restart and Enter Cave"}]
    elif "fight" in intent:
        ImageURL = ATTACK
        (msg,suggestion) = fight()
    elif "nothing" in intent:
        msg = "Before you could utter a word, the prince attacks you with a hidden dagger!"
        suggestion = [{"title": "Andd..."}]
    elif "roll" in intent and "fight" in prev_intent:
        ImageURL = DICE
        (msg,suggestion) = RollDie()
    elif "hints" in intent:
        hints = True
        client.set('hints',hints)
        msg = "Hints Enabled"
        suggestion = [{"title": "Restart and Enter Cave"},{"title": "Exit"}]
        if "welcome" not in prev_intent:
            suggestion.append({"title": prev_intent})
    else:
        msg = "None of your actions work.Let's Try Again.\n\n\n" + str(client.get('msg')) if "None of your" not in str(client.get('msg')) else str(client.get('msg'))
        suggestion = ast.literal_eval(client.get('suggestion'))
    suggestion = suggestion if str(hints)=='True' else []
    # print hints, suggestion
    display_text = msg if not display_text else display_text
    basicCard = {} if not ImageURL else {"image": {"url": ImageURL,"accessibilityText": ""},"imageDisplayOptions": "DEFAULT"}
    print(display_text)
    client.set('suggestion', suggestion)
    client.set('msg', msg)
    client.set('prev_intent', intent)
    return {
      "payload": {
        "google": {
          "expectUserResponse": str(expectUserResponse),
          "richResponse": {
            "items": [
              {
                "simpleResponse": {
                  "display_text": str(display_text),
                  "ssml": "<speak><par>\
                  <media xml:id='question' begin='0.5s'><speak><prosody rate='slow' pitch='-1st'>"+ str(msg) +"</prosody></speak></media>"+ media +
                    "<media soundLevel='+2.28dB' fadeInDur='2s' fadeOutDur='0.2s'><audio src='https://storage.googleapis.com/master-hoo.appspot.com/forest_short.ogg'/></media>\
                  </par></speak>"
                },

              },{
              "basicCard": {
                  "image": {
                    "url": ImageURL,
                    "accessibilityText": "Image alternate text"
                  },
                  "imageDisplayOptions": "DEFAULT"
                }
              }
            ],
            "suggestions": suggestion
          }
           
        }
      }
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    client.set('hints', False)
    print ("Starting app on port %d" %(port))
    suggestion=[]
    app.run(debug=True, port=port, host='0.0.0.0')