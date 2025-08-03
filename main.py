# main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import importlib.util
import os
import traceback

app = FastAPI()

SKILLS_DIR = "skills"

@app.post("/run_tool")
async def run_tool(request: Request):
    try:
        data = await request.json()
        tool_name = data.get("tool_name")
        args = data.get("args", {})

        if not tool_name:
            raise HTTPException(status_code=400, detail="Missing 'tool_name'")

        skill_path = os.path.join(SKILLS_DIR, f"{tool_name}.py")

        if not os.path.exists(skill_path):
            raise HTTPException(status_code=404, detail=f"No skill script found for '{tool_name}'")

        # Load the script dynamically
        spec = importlib.util.spec_from_file_location(tool_name, skill_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Call the main() function in the skill file
        if not hasattr(module, "main"):
            raise HTTPException(status_code=500, detail=f"'main' function not found in {tool_name}.py")

        result = module.main(**args)
        return {"status": "success", "output": result}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e), "trace": traceback.format_exc()}
        )
