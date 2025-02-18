from werkzeug.exceptions import NotFound

from odoo.http import request, route, Controller

from odoo.addons.child_compassion.models.compassion_hold import HoldType

LANG_MAPPING = {
    "ENG": "en_US",
    "SVE": "sv_SE",
    "NOR": "nb_NO",
    "DAK": "da_DK"
}


class ApiController(Controller):

    @route("/wapi/consignment", auth="public", methods=["GET"], type="json")
    def get_consigned_children(self, **params):
        lang = LANG_MAPPING.get(params.get("LanguageCode", "ENG"))
        limit = int(params.get("limit", 0))
        offset = int(params.get("offset", 0))
        count = request.env["compassion.child"].sudo().search_count([
            ("state", "=", "N"), ("hold_channel", "=", "web"), ("hold_type", "=", HoldType.E_COMMERCE_HOLD.value)
        ])
        children = request.env["compassion.child"].sudo().with_context(lang=lang).search([
            ("state", "=", "N"), ("hold_channel", "=", "web"), ("hold_type", "=", HoldType.E_COMMERCE_HOLD.value)
        ], limit=limit, offset=offset)
        data = children.data_to_json("Wordpress Consignment Child")
        for child_vals in data:
            child_vals["localSociatySituated"] = child_vals["localSociatySituated"] + ", " + child_vals.pop(
                "country_name")
            member_ids = child_vals["householdMember"]
            caregivers = children.env["compassion.household.member"].browse(member_ids).filtered("is_caregiver")
            child_vals["householdMember"] = caregivers.get_list("role")
        return {
            "ChildList": {
                "count": count,
                "range": f"{offset}-{offset + (limit-1)}" if limit else "ALL",
                "children": data
            }
        }

    @route("/wapi/consignment/<string:global_id>/sponsor", auth="public", methods=["GET"], type="json")
    def sponsor_child(self, global_id, **params):
        wordpress_user = request.env.ref("wordpress_api.user_wordpress")
        child = request.env["compassion.child"].with_user(wordpress_user).search([("global_id", "=", global_id)])
        if not child:
            raise NotFound
        child.hold_id.write({
            "type": HoldType.NO_MONEY_HOLD.value,
            "expiration_date": child.hold_id.get_default_hold_expiration(HoldType.NO_MONEY_HOLD)
        })
        return f"Child {global_id} is sponsored"
