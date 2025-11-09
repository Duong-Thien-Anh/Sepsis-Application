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

      in
      {
        devShells.default = pkgs.mkShell {
          name = "sepsis-frontend-env";

          buildInputs = [
            python
            pkgs.uv
            pkgs.tcl
            pkgs.tk
            pkgs.git
          ];

          # Critical: Make Nix's tk/tcl libs visible to Python
          LD_LIBRARY_PATH = "${pkgs.tcl}/lib:${pkgs.tk}/lib";

          shellHook = ''
            export VENV=".venv"
            export PYTHON="${python}/bin/python"

            # These MUST run every shell entry
            export TCL_LIBRARY="${pkgs.tcl}/lib/tcl${pkgs.tcl.version}"
            export TK_LIBRARY="${pkgs.tk}/lib/tk${pkgs.tk.version}"

            echo "Sepsis Frontend Dev Environment"
            echo "Python: $($PYTHON --version)"
            echo "uv:     $(${pkgs.uv}/bin/uv --version)"
            echo "Tk:     ${pkgs.tk.version} (fixed paths)"

            if [ ! -d "$VENV" ]; then
              echo "Creating virtual environment with uv..."
              ${pkgs.uv}/bin/uv venv $VENV --python $PYTHON --seed

              echo "Installing dependencies..."
              if [ -f "requirements.txt" ]; then
                ${pkgs.uv}/bin/uv pip install -r requirements.txt --strict
              else
                echo "No requirements.txt → installing customtkinter + GUI essentials"
                ${pkgs.uv}/bin/uv pip install customtkinter pillow matplotlib seaborn pandas
              fi
            fi

            source $VENV/bin/activate

            echo "   Ready! Tkinter fully fixed."
            echo ""
            echo "   Run: python main.py"
            echo "   or: uvicorn main:app --reload"
            echo ""
          '';
        };
      });
}
