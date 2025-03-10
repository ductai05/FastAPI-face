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
    # Thêm các thư viện Python khác cần thiết
  ];
  shellHook = ''
    # Có thể đặt các biến môi trường ở đây nếu cần
    echo "FastAPI development environment activated"
    echo "$ uvicorn face_check:app --reload"
  '';
}