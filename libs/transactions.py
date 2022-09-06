from collections import defaultdict

TOKEN_PROGRAM = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'


def is_token_related(transaction):
    try:
        return (
            TOKEN_PROGRAM in transaction['transaction']['message']['accountKeys']
        )
    except KeyError:
        return False


def has_inner_instructions(transaction):
    return bool(transaction['meta']['innerInstructions'])


def split_on_instructions_with_logs(transaction):
    instruction_ind_to_logs = defaultdict(list)
    instructions = transaction['transaction']['message']['instructions']
    logs = transaction['meta']['logMessages']
    current_ind = 0
    for log in logs:
        if 'compute units' in log:
            current_ind += 1
            continue
        if 'invoke' in log or 'success' in log:
            continue
        instruction_ind_to_logs[current_ind].append(log)
    return {
        **transaction,
        'instructions_with_logs': [
            {**instruction, 'logs': instruction_ind_to_logs[i]}
            for i, instruction in enumerate(instructions)
        ]
    }


def get_token_transfer_receivers(transaction):
    account_keys = transaction['transaction']['message']['accountKeys']
    receivers = []
    for instruction in transaction['instructions_with_logs']:
        is_token_program = account_keys[instruction['programIdIndex']] == TOKEN_PROGRAM
        if not is_token_program:
            continue
        is_transfer = 'Program log: Instruction: Transfer' in instruction['logs']
        is_transfer_checked = 'Program log: Instruction: TransferChecked' in instruction['logs']
        if is_transfer:
            receivers.append(account_keys[instruction['accounts'][1]])
            continue
        if is_transfer_checked:
            receivers.append(account_keys[instruction['accounts'][2]])
            continue
    return receivers
