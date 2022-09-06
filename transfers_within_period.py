from collections import defaultdict
import os
import json
import time
from threading import Thread, Event
from solana.rpc.api import Client
from libs.accounts import get_token_accounts_info
from libs.transactions import (
    is_token_related,
    has_inner_instructions,
    get_token_transfer_receivers,
    split_on_instructions_with_logs,
)

period = 86400 * 30
slot_step = 1000
workers = 10

event = Event()

def _pk_to_string(pk):
    return pk.to_base58().decode('utf-8')


def worker(
    rpc_client,
    last_slot,
    slot_step,
    stop_at,
    stats,
    receivers_by_mint,
    receivers_with_no_sol_by_mint,
    worker_ind,
    worker_count
):
    for slot in range(last_slot, 0, -slot_step):
        if slot % worker_count != worker_ind:
            continue
        if event.is_set():
            break

        stats[('slots')] += 1
        try:
            rpc_result = rpc_client.get_confirmed_block(slot)
        except:
            stats['confirmed_block_error'] += 1
            continue
        if 'result' not in rpc_result or not rpc_result['result']:
            stats['no_result_error'] += 1
            continue
        confirmed_block = rpc_result['result']

        if confirmed_block['blockTime'] < stop_at:
            break

        if not confirmed_block['transactions']:
            continue
        stats[('slots_with_transactions')] += 1

        token_related = list(filter(
            lambda t: is_token_related(t) and not has_inner_instructions(t),
            confirmed_block['transactions']
        ))
        token_related_with_logs = list(map(split_on_instructions_with_logs, token_related))
        receivers_nested = list(map(get_token_transfer_receivers, token_related_with_logs))
        receivers = [item for nested in receivers_nested for item in nested]

        try:
            receiver_accounts = list(filter(None, get_token_accounts_info(rpc_client, receivers)))
        except:
            stats['receiver_accounts_error'] += 1
            continue
        try:
            owner_accounts = rpc_client.get_multiple_accounts(
                [account.owner for account in receiver_accounts]
            )['result']['value']
        except:
            stats['owner_accounts_error'] += 1
            continue

        for receiver, owner in zip(receiver_accounts, owner_accounts):
            owner_pk = _pk_to_string(receiver.owner)
            mint = _pk_to_string(receiver.mint)
            stats[('received_token', mint)] += 1
            if owner_pk not in receivers_by_mint[mint]:
                receivers_by_mint[mint].add(owner_pk)
                stats[('received_token_unique', mint)] += 1
                stats[('received_token_total_value', mint)] += receiver.amount

            if not owner:
                stats[('received_token_no_sol', mint)] += 1
                if owner_pk not in receivers_with_no_sol_by_mint[mint]:
                    receivers_with_no_sol_by_mint[mint].add(owner_pk)
                    stats[('received_token_no_sol_unique', mint)] += 1
                    stats[('received_token_no_sol_total_value', mint)] += receiver.amount

# group by mint + unique receivers + total value in tokens of these receivers
# not created, less than transaction fee, less than account cost
def main():
    rpc_client = Client(os.environ['RPC_URL'])
    last_slot = rpc_client.get_slot()['result']

    start_time = time.time()
    stats = defaultdict(int)
    receivers_by_mint = defaultdict(set)
    receivers_with_no_sol_by_mint = defaultdict(set)

    threads = []
    for worker_ind in range(workers):
        t = Thread(target=worker, args=(
            rpc_client,
            last_slot,
            slot_step,
            start_time - period,
            stats,
            receivers_by_mint,
            receivers_with_no_sol_by_mint,
            worker_ind,
            workers,
        ))
        t.start()
        threads.append(t)

    while True:
        try:
            print(stats, end='\n' * 3)
            all_stopped = all([not t.is_alive() for t in threads])
            if all_stopped:
                break
            time.sleep(3)
        except KeyboardInterrupt:
            event.set()


if __name__ == '__main__':
    main()
