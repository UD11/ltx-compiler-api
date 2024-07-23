from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import subprocess
from pathlib import Path
import uuid
app = FastAPI()


@app.post("/compile/")
async def compile_tex(file: UploadFile = File(...)):
    upload_dir = Path("/tmp/uploads")
    output_dir = Path("/tmp/outputs")
    upload_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    unique_id = str(uuid.uuid4())
    tex_filename = f"{unique_id}_{file.filename}"
    tex_path = upload_dir / tex_filename
    pdf_path = output_dir / (tex_filename.replace(".tex", ".pdf"))

    with tex_path.open("wb") as f:
        f.write(file.file.read())

    compile_command = ["pdflatex", "-output-directory", str(output_dir), str(tex_path)]
    result = subprocess.run(compile_command, capture_output=True)

    if result.returncode != 0:
        return {"error": result.stderr.decode()}

    return FileResponse(pdf_path, media_type="application/pdf")

@app.get("/")
def read_root():
    return {"message": "Welcome to the LaTeX compiler API"}
