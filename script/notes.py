import jinja2
import markupsafe
import os.path

_note_type_lut = {
    "info": "Ⓘ",
    "warning": "Ⓦ",
    "error": "Ⓧ"
}

def _render_resource(full_ctx, res_ctx):
    # OWL-101: Throws jinja2.exceptions.TemplateNotFound:
    template = full_ctx.environment.get_template("notes/resource.html")

    ctx = {
        "config": full_ctx["config"],
        "res": res_ctx
    }

    return markupsafe.Markup(template.render(ctx))

_value_type_render_cb_lut = {
    "integer": lambda _, val: val,
    "string": lambda _, val: val,
    "resource": _render_resource
}


def _render_var_val(full_ctx, val_ctx):
    render_cb = _value_type_render_cb_lut.get(val_ctx["type"])

    if render_cb is None:
        # OWL-101: Proper error handling needed
        raise Exception(f"Invalid note value type: {val_ctx['type']}")

    return render_cb(full_ctx, val_ctx["value"])


@jinja2.pass_context
def render_note(full_ctx, note_ctx) -> markupsafe.Markup:
    type = _note_type_lut.get(note_ctx["type"], "")

    if type is None:
        # OWL-101: Proper error handling needed
        raise Exception(f"Invalid note type: {note_ctx['type']}")

    msg_fmt = type + " " + _(f"GEN-PERSON-NOTE_{note_ctx['id']}")

    rendered_vars = {
        name: _render_var_val(full_ctx, val_ctx)
        for name, val_ctx in note_ctx["vars"].items()
    }

    return markupsafe.Markup(msg_fmt.format(**rendered_vars))
