def validate_patch_with_proto(patch, proto):
    if not patch:
        raise ValueError("Patch cannot be empty.")
    for patch_key in patch:
        try:
            proto.DESCRIPTOR.fields_by_name[patch_key]
        except KeyError as e:
            raise KeyError(f"There is no {e} field in the config.")
        proto_field = proto.DESCRIPTOR.fields_by_name[patch_key]
        proto_value = getattr(proto, patch_key)
        if proto_field.type == proto_field.TYPE_MESSAGE:
            validate_patch_with_proto(patch[patch_key], proto_value)
        elif type(patch[patch_key]) is not type(proto_value):
            raise ValueError(
                f"The {patch_key} field stores the incorrect data type "
                f"{type(patch[patch_key])}, it should be {type(proto_value)}."
            )
