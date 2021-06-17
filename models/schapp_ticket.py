from odoo import models, fields, api

class schappTicketClase(models.Model):
    _name = 'schapp.ticket.clase'
    _description = 'Clase'

    name = fields.Char()
    seleccion_ids = fields.Many2many(
        comodel_name='schapp.ticket',
        relation='schapp_ticket_class_rel',
        column1='clase_id',
        column2='ticket_id',
        string='Clase') 

class schappTicketTagsTipo(models.Model):
    _name = 'schapp.ticket.tag'
    _description = 'Tipo de usuario'

    name = fields.Char()
    ticket_ids = fields.Many2many(
        comodel_name='schapp.ticket',
        relation='schapp_ticket_tag_rel',
        column1='tag_id',
        column2='ticket_id',
        string='Tags')

class schappTicket(models.Model):
    _name = 'schapp.ticket' 
    _description = 'Ticket'

    name = fields.Char(
        string="Nombre",
        required=True)

    description = fields.Text(
        string="Description",
        translate=True)

    date = fields.Date(
        string='Fecha Inicio')

    sexo = fields.Selection(
        [('masculino','Masculino'),
         ('femenino', 'Femenino'),
         ('otro', 'Otro'),],
        string='Sexo')
    
    
    tlf = fields.Integer(
        string='Telefono Movil',
        default='',
    )

    tlf_fijo = fields.Integer(
        string='Telefono Fijo',
        default='',
    )

    dni = fields.Char(
        string="DNI",
        required=True)

    
    user_id = fields.Many2one(
        comodel_name='res.user',
        string='Tipo de usuario: ')

    tag_ids = fields.Many2many(
        comodel_name='schapp.ticket.tag',
        relation='schapp_ticket_tag_rel',
        column1='ticket_id',
        column2='tag_id',
        string='Tipo de usuario')

    clase_ids = fields.Many2many(
        comodel_name='schapp.ticket.clase',
        relation='schapp_ticket_class_rel',
        column1='ticket_id',
        column2='clase_id',
        string='Clase')   
    
    user_id = fields.Many2one(
        comodel_name='res.users',
        srting='Asigned to')
    

    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            record.assigned = self.user_id and True or False
             
            
    
    #Crear campo calculado que indique, dentro de un ticket
    # la cantidad de tiquets asociados al mismo usuario.
    ticket_qty = fields.Integer(
        string='Ticket Qty',
        compute='_compute_ticket_qty')

    @api.depends('user_id')
    def _compute_ticket_qty(self):
        for record in self:
            other_tickets = self.env['schapp.ticket'].search([('user_id','=', record.user_id.id)])
            record.ticket_qty = len(other_tickets)

    # Creamos un campo nombre de etiqueta, y hacer un boton que cree la nueva etiqueta con ese nombre
    # y lo asocie al ticket.

    tag_name = fields.Char(
        string='Tag Name')

    def create_tag(self):
        self.ensure_one()
        self.write({
            'tag_ids': [(0,0, {'name': self.tag_name})]
        })


    clase_name = fields.Char(
        string='Clase')

    def create_tag(self):
        self.ensure_one()
        self.write({
            'clase_id': [(0,0, {'name': self.clase_name})]
        })
        
        