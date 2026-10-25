"""Two independent Android products. Identity is fixed when staging the build."""
WORLD_BUILD = False
WORLD_PREVIEW = False  # Historical test hook; always false in distributable staging.
FREE_PACKAGE = 'com.clemir.striker'
WORLD_PACKAGE = 'com.clemir.scorerworld'


class BuildAccess:
    def has_world_access(self):
        return is_world()

    def restore_world_access(self):
        return is_world()


def is_world():
    return WORLD_BUILD is True or WORLD_PREVIEW is True


def product_mode():
    return 'world' if is_world() else 'free'


def entitlement_provider():
    # World functionality belongs to the separate World binary, not a save flag,
    # installed-package query, ad reward or in-app billing result in Free.
    return BuildAccess()
