class Fairsem < Formula
  include Language::Python::Shebang

  desc "Fair, observable semaphore for local Linux commands"
  homepage "https://github.com/korovin-aa97/fairsem"
  url "https://github.com/korovin-aa97/fairsem/releases/download/v0.1.3/fairsem-v0.1.3.tar.gz"
  sha256 "a99a01fdfdceb110ff383a316079ebdbbefb0026ae93979045d2c25fc843a9cf"
  license "MIT"

  depends_on :linux
  depends_on "python@3.13"

  def install
    rewrite_shebang detected_python_shebang, "bin/fairsem"
    bin.install "bin/fairsem"
    man1.install "man/fairsem.1"
  end

  test do
    assert_match "fairsem 0.1.3", shell_output("#{bin}/fairsem --version")
    ENV["FAIRSEM_STATE_DIR"] = testpath/"state"
    system bin/"fairsem", "run", "--name", "homebrew", "--", "true"
    assert_match '"slots":1', shell_output("#{bin}/fairsem status --name homebrew --json")
  end
end
