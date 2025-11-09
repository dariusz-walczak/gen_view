import jinja2
import markupsafe
from markupsafe import Markup

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
        raise ValueError(f"Invalid note value type: {val_ctx['type']}")

    return render_cb(full_ctx, val_ctx["value"])


_NOTE_EXTRA_CLASS = {
    "info": "person-notes__note--info",
    "warning": "person-notes__note--warning",
    "error": "person-notes__note--error"
}


@jinja2.pass_context
def render_note(full_ctx, note_ctx) -> Markup:
    msg_fmt = _(f"GEN-PERSON-NOTE_{note_ctx['id']}")
    rendered_vars = {
        name: _render_var_val(full_ctx, val_ctx)
        for name, val_ctx in note_ctx["vars"].items()
    }
    message = msg_fmt.format(**rendered_vars)

    extra_class = _NOTE_EXTRA_CLASS.get(note_ctx.get("type", "info"), _NOTE_EXTRA_CLASS["info"])

    ctx = {
        "config": full_ctx["config"],
        "note": {
            "extra_class": extra_class,
            "message": markupsafe.Markup(message)
        }
    }

    # OWL-101: Throws jinja2.exceptions.TemplateNotFound:
    template = full_ctx.environment.get_template("notes/note.html")
    return markupsafe.Markup(template.render(ctx))
