# modulo para heredar sale.order y agregar campos
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from num2words import num2words
from datetime import date
import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'
  
    # Campos para el presupuesto
    acesor_id = fields.Many2one('sale.order.acesor', string="Acesor", required=False)
    
    acesor_phone = fields.Char(related='acesor_id.phone', string="Telefono", readonly=True)
    acesor_email = fields.Char(related='acesor_id.email', string="Correo", readonly=True)

    # fecha de entrega
    delivery_date_presupuesto = fields.Date(string='Fecha de entrega', required=False, store=True, readonly=False)
                
    # "account.payment.term"
    garantia = fields.Many2one('sale.order.garantia', string="Garantia", required=False)
    #Contado, Crédito, 50% de anticipo y saldo contra entrega.
    forma_de_pago = fields.Selection([
        ('contado', 'Contado'),
        ('credito', 'Crédito'),
        ('anticipo', '50% de anticipo y saldo contra entrega'),
    ], string='Forma de pago', default='contado', required=True)

    def to_word(self, number):
        return str(num2words(number, lang='es')).upper()

    def num_a_letras(self,num, completo=True):
        en_letras = {
            '0': 'cero',
            '1': 'uno',
            '2': 'dos',
            '3': 'tres',
            '4': 'cuatro',
            '5': 'cinco',
            '6': 'seis',
            '7': 'siete',
            '8': 'ocho',
            '9': 'nueve',
            '10': 'diez',
            '11': 'once',
            '12': 'doce',
            '13': 'trece',
            '14': 'catorce',
            '15': 'quince',
            '16': 'dieciseis',
            '17': 'diecisiete',
            '18': 'dieciocho',
            '19': 'diecinueve',
            '20': 'veinte',
            '21': 'veintiuno',
            '22': 'veintidos',
            '23': 'veintitres',
            '24': 'veinticuatro',
            '25': 'veinticinco',
            '26': 'veintiseis',
            '27': 'veintisiete',
            '28': 'veintiocho',
            '29': 'veintinueve',
            '3x': 'treinta',
            '4x': 'cuarenta',
            '5x': 'cincuenta',
            '6x': 'sesenta',
            '7x': 'setenta',
            '8x': 'ochenta',
            '9x': 'noventa',
            '100': 'cien',
            '1xx': 'ciento',
            '2xx': 'doscientos',
            '3xx': 'trescientos',
            '4xx': 'cuatrocientos',
            '5xx': 'quinientos',
            '6xx': 'seiscientos',
            '7xx': 'setecientos',
            '8xx': 'ochocientos',
            '9xx': 'novecientos',
            '1xxx': 'un mil',
            'xxxxxx': 'mil',
            '1xxxxxx': 'un millón',
            'x:x': 'millones'
        }

        num_limpio = str(num).replace(',','')
        partes = num_limpio.split('.')

        entero = 0
        decimal = 0
        if partes[0]:
            entero = str(int(partes[0]))
        if len(partes) > 1 and partes[1]:
            # Los decimales no pueden tener mas de dos digitos
            decimal = partes[1][0:2].ljust(2,'0')

        num_en_letras = 'ERROR'
        if int(entero) < 30:
            num_en_letras = en_letras[entero]
        elif int(entero) < 100:
            num_en_letras = en_letras[entero[0] + 'x']
            if entero[1] != '0':
                num_en_letras = num_en_letras + ' y ' + en_letras[entero[1]]
        elif int(entero) < 101:
            num_en_letras = en_letras[entero]
        elif int(entero) < 1000:
            num_en_letras = en_letras[entero[0] + 'xx']
            if entero[1:3] != '00':
                num_en_letras = num_en_letras + ' ' + self.num_a_letras(entero[1:3], False)
        elif int(entero) < 2000:
            num_en_letras = en_letras[entero[0] + 'xxx']
            if entero[1:4] != '000':
                num_en_letras = num_en_letras + ' ' + self.num_a_letras(entero[1:4], False)
        elif int(entero) < 1000000:
            miles = int(entero.rjust(6)[0:3])
            cientos = entero.rjust(6)[3:7]
            num_en_letras = self.num_a_letras(str(miles), False) + ' ' + en_letras['xxxxxx']
            if cientos != '000':
                num_en_letras = num_en_letras + ' ' + self.num_a_letras(cientos, False)
        elif int(entero) < 2000000:
            num_en_letras = en_letras[entero[0] + 'xxxxxx']
            if entero[1:7] != '000000':
                num_en_letras = num_en_letras + ' ' + self.num_a_letras(entero[1:7], False)
        elif int(entero) < 1000000000000:
            millones = int(entero.rjust(12)[0:6])
            miles = entero.rjust(12)[6:12]
            num_en_letras = self.num_a_letras(str(millones), False) + ' ' + en_letras['x:x']
            if miles != '000000':
                num_en_letras = num_en_letras + ' ' + self.num_a_letras(miles, False)

        if not completo:
            return num_en_letras

        if decimal == 0:
            letras = '%s' % num_en_letras
        else:
            letras = '%s con %s' % (num_en_letras, self.num_a_letras(decimal))

        return letras
class AccesorSaleOrder(models.Model):
    _ihnerit = 'res.partner'
    _name = "sale.order.acesor"
    _description = "Accesores para el presupuesto"

    # Campos para el presupuesto
    name = fields.Char(string="Accesor", required=True)
    phone = fields.Char(string="Tel.")
    email = fields.Char(string="Correo")

class SaleOrderGarantia(models.Model):
    _inherit = 'account.payment.term'
    _name = "sale.order.garantia"
    # Campos para el presupuesto
    name = fields.Char(string="Garantia", required=True)
    active = fields.Boolean(string="Estado", default=True, help="El campo activo le permite ocultar la categoría sin eliminarla.")
