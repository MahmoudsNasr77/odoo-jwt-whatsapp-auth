from odoo import models, fields
from odoo import api
import requests
import logging

_logger = logging.getLogger(__name__)
class WhatsAppMessage(models.Model):
    _name = 'whatsapp.message'
    _description = 'WhatsApp Message'

    sender_name = fields.Char()
    sender_phone = fields.Char()
    message_body = fields.Text()
    status = fields.Selection([
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed')
    ], default='pending')

    date_sent = fields.Datetime(default=fields.Datetime.now)
    
    @api.model
    def retry_pending_messages(self):
        messages = self.search([('status', '=', 'pending')])
        for msg in messages:
            try:
                apikey = self.env['ir.config_parameter'].sudo().get_param('callmebot_api_key')
                response = requests.get(
                    "https://api.callmebot.com/whatsapp.php",
                    params={
                        "phone": msg.sender_phone,
                        "text": f"{msg.sender_name}: {msg.message_body}",
                        "apikey": apikey
                    }
                )
                _logger.info("Retry WhatsApp message: %s => %s", msg.id, response.text)
                if response.status_code == 200:
                    msg.status = 'sent'
                else:
                    msg.status = 'failed'
            except Exception as e:
                _logger.error("Failed to send message %s: %s", msg.id, str(e))
                msg.status = 'failed'
                
            
            
    def excel_report(self):
        return {
            "type": "ir.actions.act_url",
            "url": f'/whatsapp_message/report/excel/{self.env.context.get("active_ids")}',
            "target": "new",
        }