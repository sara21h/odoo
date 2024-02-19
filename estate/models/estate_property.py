from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    

    name = fields.Char('Propietat immobiliària', required=True)
    description = fields.Text('Descripció')
    postcode = fields.Char('Codi Postal', required=True)
    date_availability = fields.Date('Data de disponibilitat', copy=False, 
                                     default=fields.Date.today() + relativedelta(months=3))
    expected_selling_price = fields.Integer('Preu de venda esperat')                                 
    selling_price = fields.Integer('Preu de venda', copy=False, readonly=True)
    bedrooms = fields.Integer('Habitacions')
    active = fields.Boolean(default=True) 
    parking = fields.Boolean(default=False)
    renovat = fields.Boolean(default=False)
    bathrooms = fields.Integer('Banys')
    year_construction = fields.Integer('Any construcció')
    buyer_id = fields.Many2one('res.partner', string='Comprador', readonly=True)
    salesperson_id=fields.Many2one('res.users', string='Comercial', default=lambda self: self.env.user.id)
    certificat_energetic = fields.Char('Certificat energètic')
    tag_ids = fields.Many2many('estate.property.tag', string='Etiquetes')
    area = fields.Float('Superfície (m²)', required=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Ofertes')
    avgPrice = fields.Integer('Preu per m2',compute='_calcular_preu_per_metre')
    better_offer = fields.Integer('Millor oferta', compute='_compute_better_offer', store=True, readonly=True)

    state = fields.Selection([
        ('New','Nova'),
        ('Offer Received','Oferta Rebuda'),
        ('Offer Accepted','Oferta Acceptada'),
        ('Sold','Venuda'),
        ('Canceled','Cancel·lada')
    ], default='New', string="Estat")

    property_type = fields.Many2many('estate.property.type', string='Tipus')

    @api.depends('expected_selling_price','area')
    def _calcular_preu_per_metre(self):
        for record in self:
            if record.area > 0 :
                record.avgPrice = record.expected_selling_price/record.area
            else:
                record.avgPrice = None

    @api.depends('offer_ids', 'state')
    def _compute_better_offer(self):
        for record in self:
            valid_offers = record.offer_ids.filtered(lambda offer: offer.status != 'Refused')
            best_offer = max(valid_offers.mapped('price'), default=0)
            record.better_offer = best_offer


    @api.onchange('offer_ids')
    def _onchange_status(self):
        for property_record in self:
            for offer in property_record.offer_ids:
                if offer.status == 'Accepted':
                    property_record.write({
                        'buyer_id': offer.partner_id,
                        'selling_price': offer.price,
                        'state': 'Offer Accepted',
                    })



             
