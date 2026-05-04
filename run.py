import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from streamlit.web import cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "app/main.py", "--server.headless=false"]
    sys.exit(stcli.main())
