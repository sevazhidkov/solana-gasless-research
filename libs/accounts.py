from solana.publickey import PublicKey
from spl.token.core import AccountInfo
from solana.utils.helpers import decode_byte_string
from spl.token._layouts import ACCOUNT_LAYOUT


# Extracted from spl.token. The original version didn't support loading
# arbitrary bytes strings without specifying their mint.
def create_account_info(bytes_string):
    bytes_data = decode_byte_string(bytes_string)
    try:
        decoded_data = ACCOUNT_LAYOUT.parse(bytes_data)
    except:
        return None

    mint = PublicKey(decoded_data.mint)
    owner = PublicKey(decoded_data.owner)
    amount = decoded_data.amount

    if decoded_data.delegate_option == 0:
        delegate = None
        delegated_amount = 0
    else:
        delegate = PublicKey(decoded_data.delegate)
        delegated_amount = decoded_data.delegated_amount

    is_initialized = decoded_data.state != 0
    is_frozen = decoded_data.state == 2

    if decoded_data.is_native_option == 1:
        rent_exempt_reserve = decoded_data.is_native
        is_native = True
    else:
        rent_exempt_reserve = None
        is_native = False

    if decoded_data.close_authority_option == 0:
        close_authority = None
    else:
        close_authority = PublicKey(decoded_data.owner)

    return AccountInfo(
        mint,
        owner,
        amount,
        delegate,
        delegated_amount,
        is_initialized,
        is_frozen,
        is_native,
        rent_exempt_reserve,
        close_authority,
    )


def get_token_accounts_info(conn, accounts):
    return [
        create_account_info(item['data'][0])
        if item is not None else None
        for item in conn.get_multiple_accounts(accounts)['result']['value']
    ]
