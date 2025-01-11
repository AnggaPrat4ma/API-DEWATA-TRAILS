# helper/functionRead.py

def create_access_token(identity, additional_claims=None):
    """
    Membuat token akses untuk autentikasi pengguna.

    Parameters:
    identity (dict): Identitas pengguna yang mencakup ID pengguna.
    additional_claims (dict): Klaim tambahan yang ingin ditambahkan ke token.

    Returns:
    str: Token akses yang telah dibuat.
    """
    # Proses pembuatan token (placeholder logic)
    token = f"token_for_{identity['id_user']}"
    if additional_claims:
        token += f"_with_roles_{additional_claims['roles']}"
    
    return token
