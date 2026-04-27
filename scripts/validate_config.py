import json
import sys


def validate_config(config_path='config.json'):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"❌ Config file not found: {config_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    
    errors = []
    
    if 'whitelist' not in config:
        errors.append("Missing 'whitelist' key")
    elif not isinstance(config['whitelist'], list):
        errors.append("'whitelist' must be a list")
    
    if 'rules' not in config:
        errors.append("Missing 'rules' key")
    elif not isinstance(config['rules'], list):
        errors.append("'rules' must be a list")
    else:
        for idx, rule in enumerate(config['rules']):
            if 'condition' not in rule:
                errors.append(f"Rule {idx}: missing 'condition'")
            
            if 'action' not in rule:
                errors.append(f"Rule {idx}: missing 'action'")
            elif rule['action'] not in ['delete', 'archive', 'keep']:
                errors.append(f"Rule {idx}: invalid action '{rule['action']}'")
    
    if errors:
        print("❌ Configuration validation failed:\n")
        for error in errors:
            print(f"  • {error}")
        return False
    
    print("✓ Configuration is valid")
    print(f"  • {len(config['whitelist'])} whitelisted senders")
    print(f"  • {len(config['rules'])} rules configured")
    
    return True


if __name__ == '__main__':
    success = validate_config()
    sys.exit(0 if success else 1)
