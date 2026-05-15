import sys, json
sys.path.insert(0, 'pipeline')
import core, parser_utils

config = json.load(open('pipeline/config.json'))
result = core.parse_file('pipeline/test_calib.txt', config)

print(f"WTS lines found: {len([l for l in result.lines if 'wts' in l.message.lower()])}")
for line in result.lines[:20]:
    if "wts" in line.message.lower():
        id_info = parser_utils.resolve_item_identity(line.message, config)
        price = parser_utils.normalize_price(line.message)
        ql, qty = parser_utils.extract_ql_and_qty(line.message)
        rarity = parser_utils.extract_rarity(line.message)
        print(f"RAW: {line.message}")
        print(f"--> ID: {id_info['id']}, Name: {id_info['name']}, Price: {price}, QL: {ql}, QTY: {qty}, Rarity: {rarity}")
        print("-" * 40)
