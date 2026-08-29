class Fairsem < Formula
  include Language::Python::Shebang

  desc "Fair, observable semaphore for local Linux commands"
  homepage "https://github.com/korovin-aa97/fairsem"
  url "https://github.com/korovin-aa97/fairsem/releases/download/v0.1.2/fairsem-v0.1.2.tar.gz"
  sha256 "2d994fe3687f663d5902761525506c8d9ed2594b0cc1c3b4509908646cb27b75"
  license "MIT"

  depends_on :linux
  depends_on "python@3.13"

  def install
    rewrite_shebang detected_python_shebang, "bin/fairsem"
    bin.install "bin/fairsem"
    man1.install "man/fairsem.1"
  end

  test do
    assert_match "fairsem 0.1.2", shell_output("#{bin}/fairsem --version")
    ENV["FAIRSEM_STATE_DIR"] = testpath/"state"
    system bin/"fairsem", "run", "--name", "homebrew", "--", "true"
    assert_match '"slots":1', shell_output("#{bin}/fairsem status --name homebrew --json")
  end
end
