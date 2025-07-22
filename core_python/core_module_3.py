def evaluate_token_health(token, 
                          open_mint_penalty=30, 
                          owner_change_penalty=20, 
                          liquidity_penalty=25, 
                          blacklist_penalty=50):
    """
    Calculate health score for a single token, applying penalties as configured.
    """
    score = 100
    if token.get('mint_authority') == 'open':
        score -= open_mint_penalty
    if token.get('owner_changed_recently'):
        score -= owner_change_penalty
    if not token.get('liquidity_locked', True):
        score -= liquidity_penalty
    if token.get('blacklisted'):
        score -= blacklist_penalty
    return max(score, 0)

def scan_token_batch(token_list, **penalties):
    """
    Scan a batch of tokens and return dict of id → score.
    Penalties can be overridden by passing keyword args.
    """
    return {
        token['id']: evaluate_token_health(token, **penalties)
        for token in token_list
    }

def rank_tokens(batch_scores, top_n=None):
    """
    Return a list of (token_id, score) sorted descending.
    Optionally limit to top_n results.
    """
    ranked = sorted(batch_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked if top_n is None else ranked[:top_n]

# configurable flag thresholds
_FLAG_THRESHOLDS = {
    'safe': 90,
    'caution': 60,
}

def generate_token_flags(score, thresholds=None):
    """
    Generate risk flag based on thresholds dict:
      thresholds = {'safe': 90, 'caution': 60}
    """
    th = thresholds or _FLAG_THRESHOLDS
    if score >= th['safe']:
        return "🟢 Safe"
    if score >= th['caution']:
        return "🟡 Caution"
    return "🔴 High Risk"

def batch_with_flags(token_list, penalties=None, thresholds=None, top_n=None):
    """
    Process tokens to return id → {score, flag}, optionally limit to top_n.
    """
    scores = scan_token_batch(token_list, **(penalties or {}))
    ranked = rank_tokens(scores, top_n=top_n)
    return {
        tid: {
            "score": score,
            "flag": generate_token_flags(score, thresholds)
        }
        for tid, score in ranked
    }
