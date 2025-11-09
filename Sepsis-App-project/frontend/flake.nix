{
  description = "Sepsis Frontend dev environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python311;

        pythonEnv = python.withPackages (ps: []);
      in
      {
        devShells.default = pkgs.mkShell {
          name = "sepsis-python-env";

          buildInputs = [
            pythonEnv
            pkgs.uv
          ];

          shellHook = ''
            if [ ! -d ".venv" ]; then
              echo "🐍 Creating virtual environment..."
              ${python}/bin/python -m venv .venv
              
              .venv/bin/pip install --upgrade pip
              .venv/bin/pip install uv

              echo "📦 Installing dependencies from requirements.txt..."
              .venv/bin/uv pip install -r requirements.txt --strict
            fi

            source .venv/bin/activate

            echo "✅ Ready! Python $(python --version)"
            echo "   Run: uvicorn main:app --reload"
            echo "   Or: python main.py"
          '';
        };
      });
}
