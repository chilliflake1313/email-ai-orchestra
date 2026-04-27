import os
import sys
import requests
from dotenv import load_dotenv


def check_environment():
    load_dotenv()
    
    print("🔍 Checking environment configuration...\n")
    
    required_vars = [
        'EMAIL_ADDRESS',
        'EMAIL_PASSWORD',
        'IMAP_SERVER',
    ]
    
    optional_vars = {
        'IMAP_PORT': '993',
        'OLLAMA_BASE_URL': 'http://localhost:11434',
        'OLLAMA_MODEL': 'mistral',
    }
    
    all_valid = True
    
    print("Required variables:")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            masked = value[:3] + '*' * (len(value) - 3) if len(value) > 3 else '***'
            print(f"  ✓ {var}: {masked}")
        else:
            print(f"  ❌ {var}: NOT SET")
            all_valid = False
    
    print("\nOptional variables:")
    for var, default in optional_vars.items():
        value = os.getenv(var, default)
        print(f"  ✓ {var}: {value}")
    
    print("\n🔌 Checking Ollama connection...")
    ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"  ✓ Ollama is running")
            print(f"  ✓ Available models: {len(models)}")
            
            required_model = os.getenv('OLLAMA_MODEL', 'mistral')
            model_names = [m['name'] for m in models]
            
            if any(required_model in name for name in model_names):
                print(f"  ✓ Model '{required_model}' is available")
            else:
                print(f"  ⚠️  Model '{required_model}' not found")
                print(f"     Run: ollama pull {required_model}")
                all_valid = False
        else:
            print(f"  ❌ Ollama returned status {response.status_code}")
            all_valid = False
    except requests.exceptions.ConnectionError:
        print(f"  ❌ Cannot connect to Ollama at {ollama_url}")
        print(f"     Run: ollama serve")
        all_valid = False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        all_valid = False
    
    print("\n" + "="*50)
    if all_valid:
        print("✓ Environment is ready")
        return True
    else:
        print("❌ Please fix the issues above")
        return False


if __name__ == '__main__':
    success = check_environment()
    sys.exit(0 if success else 1)
