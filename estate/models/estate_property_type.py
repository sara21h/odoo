from odoo import fields, models
class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Model per estate.property.type"
    name = fields.Char('Tipus', required=True)