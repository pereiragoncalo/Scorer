"""Build identity. The World preview is a separate test APK, never a save unlock."""
WORLD_PREVIEW = False


class WorldPreviewAccess:
    def has_world_access(self):
        return WORLD_PREVIEW
    def restore_world_access(self):
        return WORLD_PREVIEW


def entitlement_provider():
    return WorldPreviewAccess() if WORLD_PREVIEW else None
