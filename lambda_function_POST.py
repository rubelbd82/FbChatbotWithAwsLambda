import json
from botocore.vendored import requests
from datetime import datetime
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr

ACCESS_TOKEN = 'EAAHqrQP4GJ4BAOI0epWHSp2lURfiSyLG39MMBrHARMDODURl9rwS575YsRC7CARv5fkq9qTpY9JXZApR6k06urq7srgEbk0bilX3Kb1sDZBZB2zyfKyZCZATGcYh3njsl6apDxwDdxWZCqDeBzFZC3BPIgyAM48EhWDYrEZA5y1PY6DPSyaWAuvZB'
URL = 'https://graph.facebook.com/v2.6/me/messages?access_token='+ACCESS_TOKEN
dynamodb = boto3.resource('dynamodb') 
table = dynamodb.Table('ShoppingBot')

def lambda_handler(req, context):
    x = req['body'].rstrip()
    output = json.loads(x)
    resp = ''
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    # get_message()
                    sender_request = message['message'].get('text') 
                    resp = sender_request + recipient_id
                    resp = process_message(recipient_id)
                    ###send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    #response_sent_nontext = get_message()
                    #send_message(recipient_id, response_sent_nontext)
                    resp = 'attachment... '
            if message.get('postback'):
                recipient_id = message['sender']['id']
                payload = message['postback'].get('payload')
                title = message['postback'].get('title')
                resp = process_message(recipient_id, payload, title)
    return {
        'statusCode': 200,
        'body': resp
    }
    
def process_message(sender_psid, payload = '', title = ''):
  if title == 'FOOD':
      request_body = food_menu(sender_psid)
  elif title == 'FASHION':
      request_body = fashion_menu(sender_psid)
  elif title == 'ADD TO CART':
      add_to_cart(sender_psid, payload)
      request_body = text_messsage(sender_psid, 'Added to cart')
  elif title == 'SHOW CART':
      response = show_cart(sender_psid)
      request_body = text_messsage(sender_psid, response)
  elif title == 'CONFIRM ORDER':
      request_body = confirm_order(sender_psid)
  elif title == 'EMPTY CART':
      request_body = empty_cart(sender_psid)
  else:
      request_body = welcome_menu(sender_psid)
  return send_message(request_body)

def send_message(request_body):
  headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
  resp =  requests.post(URL, data=request_body, headers=headers)
  return resp.text + "\n\n" + request_body

def welcome_menu(sender_psid):
    message_body = """
    {
     "recipient":{
    "id":"%s"
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
           {
            "title":"AI Shopping Bot!",
            "image_url":"https://miro.medium.com/max/580/0*wU1Pt8z5tmxG5gmg.jpg",
            "subtitle":"New way to shop!!!",
            "default_action": {
              "type": "web_url",
              "url": "https://miro.medium.com/max/580/0*wU1Pt8z5tmxG5gmg.jpg",
              "webview_height_ratio": "tall"
            },
            "buttons":[
              {
                "type":"postback",
                "title":"FOOD",
                "payload":"food_menu"
              },
              {
                "type":"postback",
                "title":"FASHION",
                "payload":"fashion_menu"
              }
            ]      
          }
        ]
      }
    }
  }
}
"""
    return message_body % (sender_psid)

def food_menu(sender_psid):
    message_body = """
    {
     "recipient":{
    "id":"%s"
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
           {
            "title":"Delicious Pizza",
            "image_url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Supreme_pizza.jpg/800px-Supreme_pizza.jpg",
            "subtitle":"3 euro / kg ",
            "default_action": {
              "type": "web_url",
              "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Supreme_pizza.jpg/800px-Supreme_pizza.jpg",
              "webview_height_ratio": "tall"
            },
            "buttons":[
              {
                "type":"postback",
                "title":"ADD TO CART",
                "payload":"Delicious Pizza[^]3[^]https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Supreme_pizza.jpg/800px-Supreme_pizza.jpg"
              }
            ]      
          },
          
          
          
          
           {
            "title":"Crunchy Chicken",
            "image_url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/KFC_(Malaysia),_Hot_Wings_fried_chicken.jpg/800px-KFC_(Malaysia),_Hot_Wings_fried_chicken.jpg",
            "subtitle":"3 euro / kpl",
            "default_action": {
              "type": "web_url",
              "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/KFC_(Malaysia),_Hot_Wings_fried_chicken.jpg/800px-KFC_(Malaysia),_Hot_Wings_fried_chicken.jpg",
              "webview_height_ratio": "tall"
            },
            "buttons":[
              {
                "type":"postback",
                "payload":"Crunchy Chicken[^]3[^]https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/KFC_(Malaysia),_Hot_Wings_fried_chicken.jpg/800px-KFC_(Malaysia),_Hot_Wings_fried_chicken.jpg",
                "title":"ADD TO CART"
              }            
            ]      
          },
          
          
          
          
           {
            "title":"Spicy Pasta",
            "image_url":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Asian_Style_Italian_Pasta.jpg/400px-Asian_Style_Italian_Pasta.jpg",
            "subtitle":"1.95 euro / kpl",
            "default_action": {
              "type": "web_url",
              "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Asian_Style_Italian_Pasta.jpg/400px-Asian_Style_Italian_Pasta.jpg",
              "webview_height_ratio": "tall"
            },
            "buttons":[
              {
                "type":"postback",
                "title":"ADD TO CART",
                "payload":"Spicy Pasta[^]1.95[^]https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Asian_Style_Italian_Pasta.jpg/400px-Asian_Style_Italian_Pasta.jpg"
              }              
            ]      
          },
          
          
           {
            "title":"Menu",
            "image_url":"https://live.staticflickr.com/7270/7008318683_6d30de9082_b.jpg",
            "subtitle":"We have the right hat for everyone.",
            "default_action": {
              "type": "web_url",
              "url": "https://live.staticflickr.com/7270/7008318683_6d30de9082_b.jpg",
              "webview_height_ratio": "tall"
            },
            "buttons":[
            	{
                "type":"postback",
                "payload":"welcome_menu",
                "title":"Main Menu"
              },
            	{
                "type":"postback",
                "title":"SHOW CART",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              },
            	{
                "type":"postback",
                "title":"CONFIRM ORDER",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              }
            ]      
          }
          
          
        ]
      }
    }
  }
}
"""
    return message_body % (sender_psid)

def fashion_menu(sender_psid):
    message_body = """
   {
     "recipient":{
    "id":"%s"
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
           {
            "title":"Woman's Trendy Coat",
            "image_url":"http://webindream.com/wp-content/uploads/2019/10/fashion-model-4156.jpg",
            "subtitle":"30 euro / kpl ",
            "default_action": {
              "type": "web_url",
              "url": "http://webindream.com/wp-content/uploads/2019/10/fashion-model-4156.jpg",
              "webview_height_ratio": "tall"
            },
            "buttons":[
              {
                "type":"postback",
                "title":"ADD TO CART",
                "payload":"Woman's Trendy Coat[^]30[^]http://webindream.com/wp-content/uploads/2019/10/fashion-model-4156.jpg"
              }
            ]      
          },
          
          
          
          
           {
            "title":"Formal Shirt",
            "image_url":"http://webindream.com/wp-content/uploads/2019/10/blue-businessman-1043474.jpg",
            "subtitle":"20 euro / kpl",
            "default_action": {
                "type":"web_url",
                "url":"http://webindream.com/wp-content/uploads/2019/10/blue-businessman-1043474.jpg",
                "webview_height_ratio": "tall"
            },
            "buttons":[
              {
                "type":"postback",
                "payload":"Formal Shirt[^]20[^]http://webindream.com/wp-content/uploads/2019/10/blue-businessman-1043474.jpg",
                "title":"ADD TO CART"
              }            
            ]      
          },
          
          
          
           {
            "title":"Black Long Sleeve Shirt",
            "image_url":"https://images.pexels.com/photos/1021693/pexels-photo-1021693.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
            "subtitle":"25 euro / kpl",
            "default_action": {
              "type": "web_url",
              "url": "https://images.pexels.com/photos/1021693/pexels-photo-1021693.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
              "webview_height_ratio": "tall"
            },
            "buttons":[
              {
                "type":"postback",
                "title":"ADD TO CART",
                "payload":"Black Long Sleeve Shirt[^]25[^]https://images.pexels.com/photos/1021693/pexels-photo-1021693.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
              }              
            ]      
          },
          
          
           {
            "title":"Menu",
            "image_url":"https://live.staticflickr.com/7270/7008318683_6d30de9082_b.jpg",
            "subtitle":"We have the right hat for everyone.",
            "default_action": {
              "type": "web_url",
              "url": "https://live.staticflickr.com/5635/23770942120_d26f12fe92_b.jpg",
              "webview_height_ratio": "tall"
            },
            "buttons":[
            	{
                "type":"postback",
                "payload":"welcome_menu",
                "title":"Main Menu"
              },
              {
                "type":"postback",
                "title":"SHOW CART",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              },
            	{
                "type":"postback",
                "title":"CONFIRM ORDER",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              }
            ]       
          }

        ]
      }
    }
  }
}
"""
    return message_body % (sender_psid)

def text_messsage(sender_psid, message):
    message_body = """
    { "recipient": { "id": "%s"  }, "message": {"text" : "%s" } }
    """
    return message_body % (sender_psid, message)
    
def receipt(sender_psid):
    message_body = """
    {
  "recipient":{
    "id":"%s"
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"receipt",
        "recipient_name":"Stephane Crozatier",
        "order_number":"12345678902",
        "currency":"USD",
        "payment_method":"Visa 2345",        
        "order_url":"http://petersapparel.parseapp.com/order?order_id=123456",
        "timestamp":"1428444852",         
        "address":{
          "street_1":"1 Hacker Way",
          "street_2":"",
          "city":"Menlo Park",
          "postal_code":"94025",
          "state":"CA",
          "country":"US"
        },
        "summary":{
          "subtotal":75.00,
          "shipping_cost":4.95,
          "total_tax":6.19,
          "total_cost":56.14
        },
        "adjustments":[
          {
            "name":"New Customer Discount",
            "amount":20
          },
          {
            "name":"$10 Off Coupon",
            "amount":10
          }
        ],
        "elements":[
          {
            "title":"Classic White T-Shirt",
            "subtitle":"100% Soft and Luxurious Cotton",
            "quantity":2,
            "price":50,
            "currency":"USD",
            "image_url":"https://i2.wp.com/webindream.com/wp-content/uploads/2019/03/samsung-galaxy-s10-5g-1.jpg?zoom=1.25&resize=378%2C385"
          },
          {
            "title":"Classic Gray T-Shirt",
            "subtitle":"100% Soft and Luxurious Cotton",
            "quantity":1,
            "price":25,
            "currency":"USD",
            "image_url":"https://i2.wp.com/webindream.com/wp-content/uploads/2019/03/samsung-galaxy-s10-5g-1.jpg?zoom=1.25&resize=378%2C385"
          }
        ]
      }
    }
  }
}
"""
    return message_body % (sender_psid)


def add_to_cart(sender_psid, payload):
  result = [x.strip() for x in payload.split('[^]')]
  item_name = result[0]
  item_price = result[1]
  item_url = result[2]
# result is ["blah", "lots", "of", "spaces", "here"]

  now = datetime.now()
  id = now.strftime("%m%d%Y%H%M%S")
  id = id + sender_psid
  response = table.put_item(
    Item = {
            'id' : id,
           'sender_psid': sender_psid,
           'item_url': item_url,
           'item_name':item_name,
           'item_price' : item_price
           } 
    )
  return response

def empty_cart(sender_psid):
    #with delete_item function we delete the data from table
    response = table.delete_item(
        FilterExpression=Attr('sender_psid').eq(sender_psid)
        )
    return response['Item']
    
def show_cart(sender_psid):
  response = table.scan(
    FilterExpression=Attr('sender_psid').eq(sender_psid)
  )

  tr = ''
  for i in response['Items']:
    tr = tr + i['item_name'] + ' (EUR '+i['item_price']+'); '
  return tr
    
def confirm_order(sender_psid):
  response = table.scan(
    FilterExpression=Attr('sender_psid').eq(sender_psid)
  )
  text_response = ''
  for i in response['Items']:
    text_response = text_response +  '{"title":"'+i['item_name']+'", "subtitle":"","quantity":1,"price":'+i['item_price']+',"currency":"EUR","image_url":"'+i['item_url']+'"},'

  text_response =  text_response.rstrip(',')
  message_body = """
    {
  "recipient":{
    "id":"%s"
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"receipt",
        "recipient_name":"Stephane Crozatier",
        "order_number":"12345678902",
        "currency":"EUR",
        "payment_method":"Visa 2345",        
        "order_url":"http://petersapparel.parseapp.com/order?order_id=123456",
        "timestamp":"1428444852",         
        "address":{
          "street_1":"1 Hacker Way",
          "street_2":"",
          "city":"Menlo Park",
          "postal_code":"94025",
          "state":"CA",
          "country":"US"
        },
        "summary":{
          "subtotal":75.00,
          "shipping_cost":4.95,
          "total_tax":6.19,
          "total_cost":56.14
        },
        "adjustments":[
          {
            "name":"New Customer Discount",
            "amount":20
          },
          {
            "name":"EUR 10 Off Coupon",
            "amount":10
          }
        ],
        "elements":[
          %s
        ]
      }
    }
  }
}
"""
  return message_body % (sender_psid, text_response)