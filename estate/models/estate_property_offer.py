from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Model per estate.property.offer"
    
    price = fields.Integer('Preu')
    status = fields.Selection([('Accepted', 'Acceptada'), ('Refused', 'Rebutjada'), ('in progress', 'en tractament')], 
    default="in progress", copy=False)
    partner_id = fields.Many2one('res.partner', string='Comprador', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    comentaris = fields.Text('Comentaris')
