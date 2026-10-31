"""Explicit operator assertions; this gate is not legal or Google approval."""
def validate_publication(data):
    if not isinstance(data,dict):return ['Publication review configuration is required']
    errors=[]
    for flag in ('automatic_usage_legal_review','children_social_review','moderation_operator_ready','public_policy_live','cloudflare_practices_reviewed'):
        if data.get(flag) is not True:errors.append('Publication review pending: '+flag)
    if not isinstance(data.get('legal_basis'),str) or len(data['legal_basis'].strip())<20:errors.append('Document the reviewed legal basis; do not infer consent from Continue')
    return errors
