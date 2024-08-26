odoo.define('userguide.FileViewer', function (require) {
    "use strict";
    
    var core = require('web.core');
    var FormWidget = require('web.FormWidget');
    
    var _t = core._t;
    
    var FileViewer = FormWidget.extend({
        template: 'FileViewer',
        
        init: function (parent, options) {
            this._super(parent, options);
            this.file_url = options.file_url;
        },
        
        start: function () {
            var self = this;
            this.$el.html('<iframe src="' + this.file_url + '" style="width:100%; height:500px;" frameborder="0"></iframe>');
            return this._super.apply(this, arguments);
        }
    });
    
    core.form_widget_registry.add('file_viewer', FileViewer);
});
