odoo.define('pos_branch_in_receipt.models',function(require){
    "use strict";
    var pos_models = require('point_of_sale.models');

    var pos_order_prototype = pos_models.Order.prototype;

    pos_models.Order = pos_models.Order.extend({
        export_for_printing: function(){
            var receipt = pos_order_prototype.export_for_printing.call(this);

            receipt.company.contact_address = this.pos.config.company_address_street;

            return receipt;
        }
    });

});