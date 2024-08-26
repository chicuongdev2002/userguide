/** @odoo-module **/
import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";
import { _t } from "@web/core/l10n/translation";
import { session } from "@web/session";

const userMenuRegistry = registry.category("user_menuitems");

// Ghi đè lên mục "documentation"
function customDocumentationItem(env) {
    return {
        type: "item",
        id: "documentation",
        description: _t("Documentation"),
        callback: async () => {
            try {
//Gọi hành động action_user_guide để mở trang hướng dẫn
                env.services.action.doAction('userguide.action_user_guide');
            } catch (error) {
                console.error("Error opening user guide view:", error);
                env.services.notification.notify({
                    title: _t("Error"),
                    message: _t("Unable to open user guide view."),
                    type: 'danger',
                });
            }
        },
        sequence: 10,
    };
}

// Ghi đè lên mục "documentation" trong registry
userMenuRegistry.add("documentation", customDocumentationItem, { force: true });
//Xóa mục item muốn ẩn
userMenuRegistry.remove("support");
userMenuRegistry.remove("shortcuts");
userMenuRegistry.remove("odoo_account");