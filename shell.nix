with import <nixpkgs> {};
pkgs.mkShell {
  buildInputs = [
    python3
    python3Packages.pip
    python3Packages.fastapi
    python3Packages.uvicorn
    python3Packages.face-recognition
    python3Packages.python-multipart
    python3Packages.numpy
    # add other python libs
  ];
  shellHook = ''
    # add environment variable
    echo "FastAPI development environment activated"
    echo "$ uvicorn face_check:app --reload --host 127.0.0.1 --port 8000"
  '';
}