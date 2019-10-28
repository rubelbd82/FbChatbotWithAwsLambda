import json

ACCESS_TOKEN = 'EAAHqrQP4GJ4BAN0tiEJEIIEmPFr4RBNGkNcdRVhRPqKDMG5EkeBztLHj6JGFraFmHXZA7ZCEG8G8694CiZBBuPiknCwDLWmotZArWPryjQALY4xcL0H8oFpP7PxlrdEZB8lFHCZBezvSsjcrtTZAxvSAA80YoQxIqLfXrYsixgSd0rCaVOQsRdR'
VERIFY_TOKEN = 'ArtificialIntelligenceShoppingBot'

def lambda_handler(event, context):
    token_sent = event['queryStringParameters']['hub.verify_token']
    challenge = event['queryStringParameters']['hub.challenge']
    payload = verify_fb_token(token_sent, challenge)
    return {
        'statusCode': 200,
        'body': payload
    }
    # token_sent = event['queryStringParameters']['hub.verify_token']
    # return verify_fb_token(token_sent)



def verify_fb_token(token_sent, challenge):
    if token_sent == VERIFY_TOKEN:
        return challenge
    return 'Invalid verification token'