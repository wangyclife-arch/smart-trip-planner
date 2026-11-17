"""临时诊断脚本：检查 amap MCP 工具发现失败的真实原因。

运行方式（在 backend 目录，激活 .venv 后）：
    python diagnose_mcp.py
"""

import asyncio
import os
import sys
import traceback

from dotenv import load_dotenv

load_dotenv()

from hello_agents.protocols.mcp.client import MCPClient


async def main():
    key = os.getenv("AMAP_API_KEY") or os.getenv("AMAP_MAPS_API_KEY")

    print("python:", sys.executable)
    print("cwd:", os.getcwd())
    print("AMAP key:", "set" if key else "MISSING")
    print("connecting...")

    try:
        async with MCPClient(
            [sys.executable, "-m", "amap_mcp_server"],
            env={"AMAP_MAPS_API_KEY": key},
        ) as client:
            tools = await client.list_tools()
            names = [
                t.get("name") if isinstance(t, dict) else getattr(t, "name", t)
                for t in tools
            ]
            print("TOOLS:", names)
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())