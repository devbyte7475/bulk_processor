"""
应用入口
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gui import BulkProcessorGUI


def main():
    """主函数"""
    app = BulkProcessorGUI()
    app.run()


if __name__ == "__main__":
    main()
