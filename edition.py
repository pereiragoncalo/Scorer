"""Single-app entitlement: Play verifies World; preview remains test-only."""
WORLD_PREVIEW = False


class WorldPreviewAccess:
    def has_world_access(self):
        return WORLD_PREVIEW
    def restore_world_access(self):
        return WORLD_PREVIEW


def is_world():
    # Build identity only. Live paid access belongs to CareerMode.entitlements.
    return WORLD_PREVIEW


def entitlement_provider():
    if WORLD_PREVIEW:
        return WorldPreviewAccess()
    from billing import PlayWorldAccess
    return PlayWorldAccess()
