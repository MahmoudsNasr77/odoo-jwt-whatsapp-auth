from odoo import http
from odoo.http import request,Response
import requests
from ..utils.jwt_token import verify_token, generate_token
import json
from twilio.rest import Client
import logging
_logger = logging.getLogger(__name__)
class WhatsAppAPI(http.Controller):

    @http.route('/api/login', type='http', auth='public', csrf=False)
    def login(self):
        try:
            data = json.loads(request.httprequest.data)
            login = data.get('login')
            password = data.get('password')
            if not login or not password:
                return Response(json.dumps({'Message': "Missing email or password"}),content_type='application/json',status=400)
                 
            uid = request.session.authenticate(request.db, login, password)
            if uid:
                return Response(json.dumps({'Message':"Success",'token': generate_token(uid)}),content_type='application/json',status=200)
            
        except Exception as error:
            return Response(json.dumps({'Message':str(error)}),content_type='application/json',status=500)
        
    @http.route('/v1/api/send-whatsapp', type='http', auth='public', csrf=False)
    def send_whatsapp_with_callmebot(self):
        try:
            auth = request.httprequest.headers.get('Authorization')
            if not auth or not auth.startswith("Bearer "):
                return Response(json.dumps({'Message': "Authorization header missing"}), content_type='application/json', status=401)

            token = auth.split(" ")[1]
            payload = verify_token(token)
            if not payload:
                return Response(json.dumps({'Message': "Invalid or expired token"}), content_type='application/json', status=401)
            
            data = json.loads(request.httprequest.data)
            message = str(data.get('message'))
            name = str(data.get('name'))
            
            if not name or not message:
                return Response(json.dumps({'Message': "Missing name or message"}), content_type='application/json', status=400)

            phone = request.env['ir.config_parameter'].sudo().get_param('callmebot_phone')
            api_key = request.env['ir.config_parameter'].sudo().get_param('callmebot_api_key')

            if not phone or not api_key:
                return Response(json.dumps({'Message': "Missing CallMeBot configuration"}), content_type='application/json', status=500)

            response = requests.get(
                "https://api.callmebot.com/whatsapp.php",
                params={
                    "phone": phone,
                    "text": f"{name}: {message}",
                    "apikey": api_key
                }
            )
            status = 'sent' if response.status_code == 200 else 'pending'

            request.env['whatsapp.message'].sudo().create({
                'sender_name': name,
                'sender_phone': phone,
                'message_body': message,
                'status': status
            })

            return Response(json.dumps({'Message': "Success", 'status': status}), content_type='application/json', status=200)

        except Exception as error:
            return Response(json.dumps({'Message': str(error)}), content_type='application/json', status=500)

                

    @http.route('/v2/api/send-whatsapp', type='http', auth='public', csrf=False)
    def send_whatsapp_twilio(self):
        try:
            auth = request.httprequest.headers.get('Authorization')
            if not auth or not auth.startswith("Bearer "):
                return Response(json.dumps({'Message': "Authorization header missing"}), content_type='application/json', status=401)

            token = auth.split(" ")[1]
            payload = verify_token(token)
            if not payload:
                return Response(json.dumps({'Message': "Invalid or expired token"}), content_type='application/json', status=401)

            data = json.loads(request.httprequest.data)
            name = str(data.get('name'))
            message = str(data.get('message'))

            if not name or not message:
                return Response(json.dumps({'Message': "Missing name or message"}), content_type='application/json', status=400)

            account_sid = request.env['ir.config_parameter'].sudo().get_param('twilio_account_sid')
            auth_token = request.env['ir.config_parameter'].sudo().get_param('twilio_auth_token')
            whatsapp_from = request.env['ir.config_parameter'].sudo().get_param('twilio_whatsapp_from')
            company_phone = request.env['ir.config_parameter'].sudo().get_param('twilio_company_number')  

            if not account_sid or not auth_token or not whatsapp_from or not company_phone:
                return Response(json.dumps({'Message': "Missing Twilio configuration"}), content_type='application/json', status=500)

            client = Client(account_sid, auth_token)
            twilio_message = client.messages.create(
            body=f'{name} : {message}',
            from_=f'whatsapp:{whatsapp_from}',     
            to=f'whatsapp:{company_phone}' )


            request.env['whatsapp.message'].sudo().create({
                'sender_name': name,
                'sender_phone': company_phone,
                'message_body': message,
                'status': 'sent' if twilio_message.sid else 'failed'
            })

            return Response(json.dumps({
                'Message': "Success",
                'status': 'sent',
                'sid': twilio_message.sid
            }), content_type='application/json', status=200)

        except Exception as error:
            return Response(json.dumps({'Message': str(error)}), content_type='application/json', status=500)
